import textwrap

from bob.shop import search_shop_docs

result = search_shop_docs("Do you repair electric bikes?")
end = result.index(".)") + 2
for line in result[:end].splitlines():
    print(textwrap.fill(line, 72))
print("Chunks returned:", result.count("<document "))
