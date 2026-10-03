# Bob: companion code

Bob is the small AI agent you build in this book. It helps customers of
The Bike Stop, a fictional bicycle repair shop.

## What you need

- Python 3.12 or newer (tested on 3.12.3).
- Nothing else for the practice model. There are no packages to install.
- Optional: Ollama, to run a real model on your own computer for free.
- Optional: an account with a cloud model provider (this may cost money).

## Try it

```bash
python bob_app.py --demo              # free, offline, predictable
python bob_app.py --model qwen3:4b    # local model through Ollama
python bob_app.py --model qwen3:4b --staff   # adds notebook tools
```

`--staff` is for testing only: anyone who can type a command can use it.
In a real shop, notebook access must come from a proper sign-in.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Files

| File | What it does | First used in |
|---|---|---|
| `bob/models.py` | Practice model and real model adapter | Chapter 5 |
| `bob/tools.py` | Describing and safely running tools | Chapter 6 |
| `bob/agent.py` | The agent loop | Chapter 7 |
| `bob/memory.py` | History trimming and a notes file | Chapter 8 |
| `bob/knowledge.py` | Searching the shop documents | Chapter 9 |
| `bob/workflows.py` | The booking workflow | Chapter 10 |
| `bob/guardrails.py` | Approval helpers, action limits, untrusted-text labels | Chapter 11 |
| `bob/evaluate.py` | Evaluation helpers | Chapter 12 |
| `bob/shop.py` | Bob's tools, public tool list, and system prompt | Chapters 6 to 13 |
| `bob_app.py` | Bob 1.0, the terminal app | Chapter 13 |
| `evals/bob_cases.json` | Evaluation questions | Chapter 12 |
| `listings/` | Every example from the book, by chapter | All |

## Security notes

- API keys are read from environment variables. Never paste a key into code.
- `book_appointment` always asks a person before it runs, and the app
  allows at most one booking per conversation.
- Anonymous customers get `PUBLIC_TOOLS`, without the shared notebook.
- The shop data is fictional. Do not connect Bob to real customer data
  without adding authentication and a privacy review.

## Running the examples

Every example from the book is in `listings/`, by chapter, and every
runnable practice solution is in `exercises/solutions/`. To run one, copy
it into this `bob-agent` folder first, then run it from here:

```bash
python two_part_question.py
```

Run from inside `listings/` or `exercises/`, an example cannot find the
`bob` package or the `data` folder, and stops with
`ModuleNotFoundError: No module named 'bob'`.

License: the code is under the MIT License (see LICENSE); the shop data
is public domain (CC0 1.0, see data/README.md).
