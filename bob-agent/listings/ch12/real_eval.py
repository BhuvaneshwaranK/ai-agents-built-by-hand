from bob import ChatModel, ModelError
from bob.evaluate import load_cases, run_eval, show_results, summary
from bob.shop import SHOP_TOOLS, SYSTEM_PROMPT


def make_model(case):
    return ChatModel("qwen3:4b")


cases = load_cases("evals/bob_cases.json")
try:
    results = run_eval(make_model, cases, SHOP_TOOLS, SYSTEM_PROMPT,
                       runs=3)
    show_results(results)
    totals = summary(results)
    print(f"Passed {totals['passed']} of {totals['runs']} "
          f"({totals['pass_rate']:.0%}). Most steps: "
          f"{totals['most_steps']}, average "
          f"{totals['average_steps']:.1f}.")
except ModelError as error:
    print("Problem:", error)
