"""Bob 1.0: run Bob from the terminal.

    python bob_app.py --demo
        A free, offline demo using the practice model.

    python bob_app.py --model qwen3:4b
        Chat with a real model served locally by Ollama.

    python bob_app.py --model NAME --base-url URL --key-env VAR
        Chat with a cloud model (may cost money; see the book).

Add --staff to give Bob the notebook tools as well. In a real shop,
only signed-in staff should get them (Chapter 11).
"""

import argparse
import textwrap

from bob import ChatModel, ModelError, PracticeModel, call_tool, say
from bob import run_agent, show_trace
from bob.guardrails import check_user_input, limit_actions
from bob.memory import trim_history
from bob.shop import PUBLIC_TOOLS, SHOP_TOOLS, SYSTEM_PROMPT
from bob.tools import ask_in_terminal

GREETING = (
    "Hello! I'm Bob, an AI assistant for The Bike Stop. I can check "
    "repairs, prices, opening hours, and free slots. I can make "
    "mistakes, and a person approves every booking. Type 'quit' to "
    "stop."
)


def demo():
    model = PracticeModel([
        call_tool("check_repair_status", order_id="R-1042"),
        say("Your mountain bike (R-1042) is waiting for parts. "
            "We expect it to be ready on Thursday."),
    ])
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "Is my bike R-1042 ready?"}]
    trace = []
    answer = run_agent(model, messages, SHOP_TOOLS, trace=trace)
    show_trace(trace)
    print()
    print(textwrap.fill("Bob: " + answer, 72,
                        subsequent_indent="     "))


def choose_tools(staff):
    """Least privilege: strangers get PUBLIC_TOOLS (Chapter 11)."""
    if staff:
        return SHOP_TOOLS
    return PUBLIC_TOOLS


def handle_message(model, messages, text, tools, approve):
    """Answer one customer message and return Bob's reply."""
    problem = check_user_input(text)
    if problem:
        return problem
    messages.append({"role": "user", "content": text})
    messages[:] = trim_history(messages, keep_last=30)
    start = len(messages) - 1  # where this question's messages begin
    try:
        return run_agent(model, messages, tools, approve=approve)
    except ModelError as error:
        del messages[start:]  # forget this question, keep the rest
        return f"Sorry, I can't answer right now. ({error})"


def chat(model, tools):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    approve = limit_actions(ask_in_terminal, max_actions=1)
    print(GREETING)
    while True:
        try:
            text = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            break
        if text.strip().lower() in ("quit", "exit"):
            break
        print("Bob:", handle_message(model, messages, text, tools,
                                       approve))
    print("\nGoodbye.")


def main():
    parser = argparse.ArgumentParser(description="Bob, a shop agent")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--base-url",
                        default="http://localhost:11434/v1")
    parser.add_argument("--key-env", default=None)
    parser.add_argument("--staff", action="store_true")
    args = parser.parse_args()

    if args.demo or not args.model:
        demo()
    else:
        model = ChatModel(args.model, args.base_url, args.key_env)
        chat(model, choose_tools(args.staff))


if __name__ == "__main__":
    main()
