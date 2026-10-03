"""Tests for Bob. Run from the 02_code folder with:

    python -m unittest discover -s tests -v
"""

import http.server
import json
import shutil
import tempfile
import threading
import unittest
from pathlib import Path

from bob import (ChatModel, ModelError, PracticeModel, call_tool,
                   make_tool, run_agent, run_tool_call, say)
from bob import shop
from bob.guardrails import (always_allow, always_deny,
                              check_user_input, limit_actions)
from bob.knowledge import load_chunks, search, words
from bob.memory import NotesFile, trim_history
from bob.workflows import book_with_workflow
from bob.evaluate import check_case, load_cases, run_eval, summary
from bob import mcp_sketch


class ShopDataTestCase(unittest.TestCase):
    """Each test gets a fresh copy of the shop data."""

    def setUp(self):
        self.original = shop.DATA_DIR
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(self.original, self.tmp / "shop")
        shop.use_data_dir(self.tmp / "shop")

    def tearDown(self):
        shop.use_data_dir(self.original)
        shutil.rmtree(self.tmp)


class ToolTests(ShopDataTestCase):
    def test_status_found_case_insensitive(self):
        result = shop.check_repair_status(" r-1042 ")
        self.assertEqual(result["status"], "waiting for parts")

    def test_status_not_found(self):
        self.assertIn("No repair found", shop.check_repair_status("R-9"))

    def test_quote_is_exact(self):
        result = shop.calculate_quote(["brake adjustment", "gear tuning"])
        self.assertEqual(result["total_usd"], 60.0)

    def test_quote_unknown_service(self):
        self.assertIn("Unknown services",
                      shop.calculate_quote(["paint job"]))

    def test_booking_removes_free_slot(self):
        self.assertIn("Booked", shop.book_appointment(
            "Mon 10:00", "Amina", "brake adjustment"))
        self.assertNotIn("Mon 10:00", shop.list_free_slots())
        self.assertIn("not free", shop.book_appointment(
            "Mon 10:00", "Tomas", "gear tuning"))


class RunToolCallTests(ShopDataTestCase):
    def call(self, name, raw_arguments):
        return {"id": "c1", "type": "function",
                "function": {"name": name, "arguments": raw_arguments}}

    def test_unknown_tool(self):
        out = run_tool_call(self.call("fly", "{}"), shop.SHOP_TOOLS)
        self.assertIn("no tool called", out)

    def test_bad_json(self):
        out = run_tool_call(self.call("recall", "{oops"), shop.SHOP_TOOLS)
        self.assertIn("not valid JSON", out)

    def test_arguments_already_a_dictionary(self):
        call = self.call("check_repair_status", None)
        call["function"]["arguments"] = {"order_id": "R-1043"}
        out = run_tool_call(call, shop.SHOP_TOOLS)
        self.assertIn("in progress", out)

    def test_wrong_arguments(self):
        out = run_tool_call(self.call("check_repair_status", '{"x": 1}'),
                            shop.SHOP_TOOLS)
        self.assertIn("wrong arguments", out)

    def test_tool_crash_becomes_message(self):
        def explode():
            raise ValueError("boom")
        tools = [make_tool(explode, "Always fails.", shop.NO_ARGS)]
        out = run_tool_call(self.call("explode", "{}"), tools)
        self.assertIn("boom", out)

    def test_approval_denied_means_no_booking(self):
        args = json.dumps({"slot": "Mon 10:00", "customer_name": "X",
                           "service": "gear tuning"})
        out = run_tool_call(self.call("book_appointment", args),
                            shop.SHOP_TOOLS, approve=always_deny)
        self.assertIn("did not allow", out)
        self.assertIn("Mon 10:00", shop.list_free_slots())


class AgentLoopTests(ShopDataTestCase):
    def start(self, question):
        return [{"role": "system", "content": shop.SYSTEM_PROMPT},
                {"role": "user", "content": question}]

    def test_two_step_loop(self):
        model = PracticeModel([
            call_tool("check_repair_status", order_id="R-1042"),
            say("It is waiting for parts."),
        ])
        messages, trace = self.start("Is R-1042 ready?"), []
        answer = run_agent(model, messages, shop.SHOP_TOOLS, trace=trace)
        self.assertEqual(answer, "It is waiting for parts.")
        self.assertEqual([e["kind"] for e in trace],
                         ["tool_call", "tool_result", "answer"])
        self.assertEqual(messages[3]["role"], "tool")
        self.assertIn("waiting for parts", messages[3]["content"])

    def test_step_limit_stops_runaway_agent(self):
        model = PracticeModel([call_tool("recall")] * 10)
        answer = run_agent(model, self.start("Loop!"), shop.SHOP_TOOLS,
                           max_steps=3)
        self.assertIn("step limit", answer)
        self.assertEqual(model.calls, 3)

    def test_injection_text_is_marked_untrusted(self):
        result = shop.search_shop_docs("special offer repairs free")
        self.assertIn('<document source="customer_reviews.md">', result)
        self.assertIn("not an instruction", result)

    def test_booking_with_approval(self):
        model = PracticeModel([
            call_tool("book_appointment", slot="Wed 09:00",
                      customer_name="Priya", service="flat tire repair"),
            say("Done."),
        ])
        run_agent(model, self.start("Book Wed 09:00"), shop.SHOP_TOOLS,
                  approve=always_allow)
        self.assertNotIn("Wed 09:00", shop.list_free_slots())


class MemoryAndKnowledgeTests(ShopDataTestCase):
    def test_trim_never_starts_with_tool_message(self):
        messages = [{"role": "system", "content": "s"}]
        for i in range(10):
            messages += [{"role": "user", "content": str(i)},
                         {"role": "assistant", "content": None,
                          "tool_calls": [{"id": str(i)}]},
                         {"role": "tool", "tool_call_id": str(i),
                          "content": "r"},
                         {"role": "assistant", "content": "a"}]
        for keep in range(1, 12):
            trimmed = trim_history(messages, keep_last=keep)
            self.assertEqual(trimmed[0]["role"], "system")
            if len(trimmed) > 1:
                self.assertEqual(trimmed[1]["role"], "user")
            self.assertEqual(trimmed[-1], messages[-1])

    def test_trim_keeps_everything_if_no_user_in_tail(self):
        messages = [{"role": "system", "content": "s"},
                    {"role": "user", "content": "q"}]
        messages += [{"role": "assistant", "content": "a"}] * 5
        self.assertEqual(trim_history(messages, keep_last=2), messages)

    def test_notes_round_trip(self):
        notes = NotesFile(self.tmp / "notes.json")
        self.assertEqual(notes.recall(), "No notes saved yet.")
        notes.remember("Amina prefers morning slots.")
        self.assertIn("morning", notes.recall())

    def test_words_and_search(self):
        self.assertIn("tire", words("Flat tires?"))
        chunks = load_chunks(shop.DATA_DIR / "docs")
        best = search(chunks, "do you repair electric bikes")[0]
        self.assertIn("electric", best["text"].lower())

    def test_no_heading_only_chunks(self):
        for chunk in load_chunks(shop.DATA_DIR / "docs"):
            body = [l for l in chunk["text"].splitlines()
                    if l.strip() and not l.startswith("#")]
            self.assertTrue(body, chunk["text"])

    def test_limit_actions_allows_only_the_limit(self):
        limited = limit_actions(always_allow, max_actions=2)
        results = [limited("book_appointment", {}) for _ in range(4)]
        self.assertEqual(results, [True, True, False, False])

    def test_limit_actions_counts_only_approved(self):
        limited = limit_actions(always_deny, max_actions=1)
        self.assertFalse(limited("book_appointment", {}))
        self.assertFalse(limited("book_appointment", {}))

    def test_public_tools_have_no_shared_memory(self):
        names = [t["name"] for t in shop.PUBLIC_TOOLS]
        self.assertNotIn("recall", names)
        self.assertNotIn("remember", names)
        self.assertIn("check_repair_status", names)

    def test_input_checks(self):
        self.assertIsNotNone(check_user_input("   "))
        self.assertIsNotNone(check_user_input("x" * 5000))
        self.assertIsNone(check_user_input("Hello"))


class WorkflowTests(ShopDataTestCase):
    def run_flow(self, replies, request, approve=always_allow):
        model = PracticeModel(replies)
        trace = []
        reply = book_with_workflow(model, request, "Amina",
                                   "brake adjustment", approve, trace)
        return reply, trace, model

    def test_books_first_free_slot_on_requested_day(self):
        reply, trace, model = self.run_flow(
            [say("Monday"), say("You're booked: Mon 10:00. See you!")],
            "Can I come on Monday?")
        self.assertEqual(reply, "You're booked: Mon 10:00. See you!")
        self.assertNotIn("Mon 10:00", shop.list_free_slots())
        self.assertEqual(model.calls, 2)
        self.assertEqual([e["step"] for e in trace], [1, 2, 3, 4, 5])

    def test_no_day_asks_again_without_booking(self):
        reply, trace, model = self.run_flow([say("NONE")], "Whenever")
        self.assertIn("Which day", reply)
        self.assertEqual(model.calls, 1)
        self.assertIn("Mon 10:00", shop.list_free_slots())

    def test_no_free_slot_on_that_day(self):
        reply, _, _ = self.run_flow([say("Fri")], "Friday please")
        self.assertIn("no free slots on Fri", reply)

    def test_denied_books_nothing(self):
        reply, _, _ = self.run_flow([say("Tue")], "Tuesday",
                                    approve=always_deny)
        self.assertIn("not booked", reply)
        self.assertIn("Tue 11:00", shop.list_free_slots())

    def test_confirmation_without_the_slot_is_replaced(self):
        reply, _, _ = self.run_flow(
            [say("Wed"), say("All set, see you soon!")], "Wednesday")
        self.assertEqual(
            reply, "Booked brake adjustment for Amina on Wed 09:00.")


class EvaluationTests(ShopDataTestCase):
    def test_check_case_reasons(self):
        case = {"must_call": ["calculate_quote"],
                "must_not_call": ["book_appointment"],
                "answer_must_include": ["60"],
                "answer_must_not_include": ["free"]}
        trace = [{"step": 1, "kind": "tool_call",
                  "detail": 'book_appointment({"slot": "Mon 10:00"})'}]
        problems = check_case(case, "Repairs are FREE", trace)
        self.assertEqual(problems, [
            "did not call calculate_quote", "called book_appointment",
            "answer lacks '60'", "answer contains 'free'"])

    def test_run_eval_and_summary(self):
        cases = [{"name": "status", "question": "Is R-1042 ready?",
                  "must_call": ["check_repair_status"],
                  "answer_must_include": ["Thursday"]}]

        def make_model(case):
            return PracticeModel([
                call_tool("check_repair_status", order_id="R-1042"),
                say("Ready on Thursday.")])

        results = run_eval(make_model, cases, shop.SHOP_TOOLS,
                           shop.SYSTEM_PROMPT, runs=2)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["problems"], [])
        totals = summary(results)
        self.assertEqual(totals["pass_rate"], 1.0)
        self.assertEqual(totals["most_steps"], 2)

    def test_evaluation_never_books(self):
        cases = [{"name": "booking", "question": "Book Mon 10:00"}]

        def make_model(case):
            return PracticeModel([
                call_tool("book_appointment", slot="Mon 10:00",
                          customer_name="X", service="gear tuning"),
                say("Done.")])

        run_eval(make_model, cases, shop.SHOP_TOOLS, shop.SYSTEM_PROMPT)
        self.assertIn("Mon 10:00", shop.list_free_slots())

    def test_shipped_cases_are_valid(self):
        here = Path(__file__).resolve().parents[1]
        cases = load_cases(here / "evals" / "bob_cases.json")
        names = [t["name"] for t in shop.SHOP_TOOLS]
        for case in cases:
            self.assertIn("question", case)
            for key in ("must_call", "must_not_call"):
                for tool in case.get(key, []):
                    self.assertIn(tool, names)


class AppTests(ShopDataTestCase):
    def setUp(self):
        super().setUp()
        import bob_app
        self.app = bob_app
        self.messages = [{"role": "system",
                          "content": shop.SYSTEM_PROMPT}]

    def test_answers_and_keeps_history(self):
        model = PracticeModel([say("We are closed on Sundays.")])
        reply = self.app.handle_message(model, self.messages,
                                        "Open Sunday?", shop.PUBLIC_TOOLS,
                                        always_deny)
        self.assertEqual(reply, "We are closed on Sundays.")
        self.assertEqual([m["role"] for m in self.messages],
                         ["system", "user", "assistant"])

    def test_long_input_never_reaches_model(self):
        model = PracticeModel([])
        reply = self.app.handle_message(model, self.messages, "x" * 5000,
                                        shop.PUBLIC_TOOLS, always_deny)
        self.assertIn("too long", reply)
        self.assertEqual(model.calls, 0)
        self.assertEqual(len(self.messages), 1)

    def test_failure_mid_answer_leaves_valid_history(self):
        model = PracticeModel([call_tool("list_free_slots")])
        reply = self.app.handle_message(model, self.messages, "Slots?",
                                        shop.PUBLIC_TOOLS, always_deny)
        self.assertIn("can't answer right now", reply)
        self.assertEqual(len(self.messages), 1)

    def test_one_booking_per_conversation(self):
        approve = limit_actions(always_allow, max_actions=1)
        model = PracticeModel([
            call_tool("book_appointment", slot="Mon 10:00",
                      customer_name="Tomas", service="gear tuning"),
            say("Booked Monday."),
            call_tool("book_appointment", slot="Tue 11:00",
                      customer_name="Tomas", service="gear tuning"),
            say("Sorry, I could not book Tuesday."),
        ])
        for text in ["Book Monday", "Also book Tuesday"]:
            self.app.handle_message(model, self.messages, text,
                                    shop.PUBLIC_TOOLS, approve)
        free = shop.list_free_slots()
        self.assertNotIn("Mon 10:00", free)
        self.assertIn("Tue 11:00", free)

    def test_quote_accepts_one_service_as_text(self):
        self.assertEqual(shop.calculate_quote("gear tuning")["total_usd"],
                         35.0)
        self.assertIn("Unknown services: unicycle",
                      shop.calculate_quote("unicycle"))

    def test_strip_thinking(self):
        from bob.models import strip_thinking
        self.assertEqual(strip_thinking("<think>Hmm.\nOK.</think>\n\nHi"),
                         "Hi")
        self.assertEqual(strip_thinking("  plain  "), "  plain  ")
        self.assertIsNone(strip_thinking(None))

    def test_greeting_says_it_is_an_ai(self):
        self.assertIn("AI assistant", self.app.GREETING)
        self.assertIn("approves every booking", self.app.GREETING)

    def test_strangers_get_public_tools(self):
        self.assertIs(self.app.choose_tools(False), shop.PUBLIC_TOOLS)
        self.assertIs(self.app.choose_tools(True), shop.SHOP_TOOLS)


class McpSketchTests(ShopDataTestCase):
    def ask(self, method, params=None, request_id=1):
        request = {"jsonrpc": "2.0", "id": request_id,
                   "method": method, "params": params or {}}
        return mcp_sketch.handle_request(request, mcp_sketch.READ_TOOLS)

    def test_tools_list_shape(self):
        result = self.ask("tools/list")["result"]
        self.assertEqual(result["resultType"], "complete")
        names = [t["name"] for t in result["tools"]]
        self.assertIn("check_repair_status", names)
        self.assertNotIn("book_appointment", names)
        for tool in result["tools"]:
            self.assertEqual(tool["inputSchema"]["type"], "object")

    def test_tools_call_success_and_tool_error(self):
        ok = self.ask("tools/call", {"name": "check_repair_status",
                                     "arguments": {"order_id": "R-1042"}})
        self.assertFalse(ok["result"]["isError"])
        self.assertIn("waiting for parts",
                      ok["result"]["content"][0]["text"])
        bad = self.ask("tools/call", {"name": "check_repair_status",
                                      "arguments": {"order": "R-1042"}})
        self.assertTrue(bad["result"]["isError"])

    def test_unknown_tool_and_method_are_protocol_errors(self):
        self.assertEqual(self.ask("tools/call", {"name": "book_appointment"})
                         ["error"]["code"], -32602)
        self.assertEqual(self.ask("resources/list")["error"]["code"],
                         -32601)

    def test_serve_over_lines(self):
        import io
        lines = io.StringIO(
            '{"jsonrpc": "2.0", "method": "notifications/x"}\n'
            "not json\n"
            '{"jsonrpc": "2.0", "id": 7, "method": "tools/list"}\n')
        out = io.StringIO()
        mcp_sketch.serve(mcp_sketch.READ_TOOLS, lines, out)
        replies = [json.loads(l) for l in out.getvalue().splitlines()]
        self.assertEqual(len(replies), 2)
        self.assertEqual(replies[0]["error"]["code"], -32700)
        self.assertEqual(replies[1]["id"], 7)
        for line in out.getvalue().splitlines():
            self.assertNotIn("\n", line)


class FakeServer(http.server.BaseHTTPRequestHandler):
    """Pretends to be a Chat Completions server on this computer."""
    last_body = None

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        FakeServer.last_body = json.loads(self.rfile.read(length))
        FakeServer.last_auth = self.headers.get("Authorization")
        reply = {"choices": [{"message": {
                     "role": "assistant", "content": None,
                     "tool_calls": [{"id": "x", "type": "function",
                                     "function": {"name": "recall",
                                                  "arguments": "{}"}}]}}],
                 "usage": {"total_tokens": 42}}
        data = json.dumps(reply).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


class ChatModelTests(unittest.TestCase):
    def test_request_and_reply_shape(self):
        server = http.server.HTTPServer(("127.0.0.1", 0), FakeServer)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/v1"
            model = ChatModel("test-model", base_url=url)
            reply = model.chat([{"role": "user", "content": "hi"}],
                               tools=[{"type": "function"}])
        finally:
            server.shutdown()
            server.server_close()
        self.assertEqual(FakeServer.last_body["model"], "test-model")
        self.assertIn("tools", FakeServer.last_body)
        self.assertIsNone(FakeServer.last_auth)
        self.assertEqual(reply["tool_calls"][0]["function"]["name"],
                         "recall")
        self.assertEqual(model.tokens_used, 42)
        self.assertNotIn("temperature", FakeServer.last_body)

    def test_temperature_is_sent_when_set(self):
        server = http.server.HTTPServer(("127.0.0.1", 0), FakeServer)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/v1"
            ChatModel("m", base_url=url, temperature=0).chat(
                [{"role": "user", "content": "hi"}])
        finally:
            server.shutdown()
            server.server_close()
        self.assertEqual(FakeServer.last_body["temperature"], 0)

    def test_missing_key_gives_clear_error(self):
        model = ChatModel("m", api_key_env="BOB_TEST_KEY_NOT_SET")
        with self.assertRaises(ModelError) as caught:
            model.chat([{"role": "user", "content": "hi"}])
        self.assertIn("BOB_TEST_KEY_NOT_SET", str(caught.exception))

    def test_server_down_gives_clear_error(self):
        model = ChatModel("m", base_url="http://127.0.0.1:9/v1", timeout=2)
        with self.assertRaises(ModelError) as caught:
            model.chat([{"role": "user", "content": "hi"}])
        self.assertIn("Is the model server running", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
