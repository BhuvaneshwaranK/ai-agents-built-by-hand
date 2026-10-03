# AI Agents, Built by Hand: companion files

Code, data, examples, and practice solutions for the book
*AI Agents, Built by Hand: A Beginner's Guide to Making a Safe, Tested AI
Agent in Plain Python*, by Bhuvaneshwaran Krishnamoorthy.

In the book you build **Bob**, an AI assistant for **The Bike Stop**, a
small (fictional) bicycle repair shop, using nothing but Python's standard
library.

## Download

1. Open the **Releases** section of this page (on the right, or under
   the repository name on a phone) and choose the latest release.
2. Download **`bob-agent.zip`** and extract it.
3. You now have a folder called `bob-agent`. Chapter 3 of the book takes
   you from here.

The same files are also in the [`bob-agent`](bob-agent) folder of this
repository, if you prefer to browse them online.

## Check that it works

You need Python 3.12 or newer, and nothing else. In a terminal, inside
the `bob-agent` folder:

```text
python bob_app.py --demo
python -m unittest discover -s tests
```

The demo prints a short conversation, and the tests end with `OK`.

## Running the book's examples

Every example from the book is in `bob-agent/listings/`, by chapter, and
every runnable practice solution is in `bob-agent/exercises/solutions/`.
Copy an example into the `bob-agent` folder before running it, so that it
can find the `bob` package and the shop's data.

## Versions

`bob-agent/VERSIONS.md` lists the versions of Python, models, and
specifications the book was checked against (October 2026).

## License

The code is released under the MIT License (see `LICENSE`). The shop data
is dedicated to the public domain under CC0 1.0 (see
`bob-agent/data/README.md`). The Bike Stop, Bob, and all shop data are
fictional.

## Errata

Corrections to the book will be listed here.
