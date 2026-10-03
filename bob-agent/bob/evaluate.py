"""Evaluation: measure how well an agent behaves on a set of questions.

Tests check code that must never change. Evaluations check behavior
that a model decides, which can vary from run to run. So each case can
be run several times, and the result is a pass rate, not a single yes
or no. Approval is always refused, so an evaluation never changes data.
"""

import json
from pathlib import Path

from .agent import run_agent
from .guardrails import always_deny


def load_cases(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def tools_called(trace):
    """The names of the tools the model asked for, in order."""
    names = []
    for event in trace:
        if event["kind"] == "tool_call":
            names.append(event["detail"].split("(")[0])
    return names


def check_case(case, answer, trace):
    """Return the reasons a run failed. Empty means it passed."""
    called = tools_called(trace)
    problems = []
    for name in case.get("must_call", []):
        if name not in called:
            problems.append(f"did not call {name}")
    for name in case.get("must_not_call", []):
        if name in called:
            problems.append(f"called {name}")
    text = answer.lower()
    for word in case.get("answer_must_include", []):
        if word.lower() not in text:
            problems.append(f"answer lacks '{word}'")
    for word in case.get("answer_must_not_include", []):
        if word.lower() in text:
            problems.append(f"answer contains '{word}'")
    for event in trace:
        if event["kind"] == "stopped":
            problems.append("hit the step limit")
    return problems


def run_eval(make_model, cases, tools, system_prompt, runs=1,
             max_steps=8):
    """Run every case `runs` times and return one result per run.

    make_model is a function that receives a case and returns a fresh
    model for it, so practice scripts and real models both work.
    """
    results = []
    for case in cases:
        for run in range(1, runs + 1):
            messages = [{"role": "system", "content": system_prompt},
                        {"role": "user", "content": case["question"]}]
            trace = []
            answer = run_agent(make_model(case), messages, tools,
                               max_steps=max_steps,
                               approve=always_deny, trace=trace)
            steps = 0
            for event in trace:
                steps = max(steps, event["step"])
            results.append({"case": case["name"], "run": run,
                            "steps": steps, "answer": answer,
                            "problems": check_case(case, answer,
                                                   trace)})
    return results


def summary(results):
    """Pass rate and step counts for a list of results."""
    passed = [r for r in results if not r["problems"]]
    steps = [r["steps"] for r in results]
    return {"runs": len(results), "passed": len(passed),
            "pass_rate": len(passed) / len(results),
            "most_steps": max(steps),
            "average_steps": sum(steps) / len(steps)}


def show_results(results):
    for r in results:
        status = "PASS" if not r["problems"] else "FAIL"
        unit = "step" if r["steps"] == 1 else "steps"
        print(f"{status}  {r['case']} (run {r['run']}, "
              f"{r['steps']} {unit})")
        for problem in r["problems"]:
            print("        " + problem)
