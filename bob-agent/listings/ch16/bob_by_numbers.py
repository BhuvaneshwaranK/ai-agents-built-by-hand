import unittest
from pathlib import Path

from bob.evaluate import load_cases
from bob.shop import PUBLIC_TOOLS, SHOP_TOOLS

modules = sorted(Path("bob").glob("*.py"))
lines = 0
for path in modules:
    lines = lines + len(path.read_text(encoding="utf-8").splitlines())
lines = lines + len(Path("bob_app.py").read_text().splitlines())

tests = unittest.defaultTestLoader.discover("tests").countTestCases()
cases = load_cases("evals/bob_cases.json")

print("Python files in the bob package:", len(modules))
print("Lines of code, including the app: ", lines)
print("Tools:", len(SHOP_TOOLS), "for staff,", len(PUBLIC_TOOLS),
      "for customers")
print("Automatic tests:", tests)
print("Evaluation cases:", len(cases))
print("Libraries installed with pip: 0")
