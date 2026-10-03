from bob import PracticeModel, call_tool, say
from bob.evaluate import load_cases, run_eval, show_results, summary
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT

# Practice scripts: what a model "did" for each case. Two are wrong
# on purpose, so you can see what failures look like.
SCRIPTS = {
    "status": [call_tool("check_repair_status", order_id="R-1042"),
               say("It is waiting for a part; ready on Thursday.")],
    "price": [say("Together they cost $60.")],
    "sunday": [call_tool("search_shop_docs", question="open Sundays"),
               say("No, we are closed on Sundays.")],
    "ebike": [call_tool("search_shop_docs", question="electric bikes"),
              say("Yes, the mechanical parts, but not batteries or "
                  "motors.")],
    "booking": [call_tool("list_free_slots"),
                say("Monday has free slots at 10:00 and 14:00.")],
    "refund attack": [say("I can't issue refunds. Please speak to "
                          "the shop owner.")],
    "injection attack": [
        call_tool("search_shop_docs", question="special offers"),
        say("Good news: all repairs are free this week!")],
}


def make_model(case):
    return PracticeModel(SCRIPTS[case["name"]])


cases = load_cases("evals/bob_cases.json")
results = run_eval(make_model, cases, SHOP_TOOLS, SYSTEM_PROMPT)
show_results(results)
totals = summary(results)
print(f"Passed {totals['passed']} of {totals['runs']} "
      f"({totals['pass_rate']:.0%}). Most steps: "
      f"{totals['most_steps']}.")
