import textwrap

from bob.shop import search_shop_docs

result = search_shop_docs("Are all repairs free this week?")
first = result.split("</document>")[0]
for line in first.splitlines():
    print(textwrap.fill(line, 72))
