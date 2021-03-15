import json
import numpy as np

with open("advex_papers.json") as f:
    papers = json.load(f)

plist = []
for paper in papers:
    plist.append(paper)

abscitepapers = {}
# sorting by absolute citation count
plist.sort(reverse=True, key=lambda x: x[-1][0])
print("Absolute citation counts:")
for p in plist[:50]:
    print("Paper: ", p[2])
    print("Authors: ", p[3])
    print("Date: ", p[0][0])
    print("Citation Count: ", p[-1][0])
    abscitepapers[p[-1][0]] = p[:-1]

with open("abscitepapers.json", "w") as f:
    json.dump(abscitepapers, f, sort_keys=False)

print()
print()
relcitepapers = {}
# sorting by relative citation count
print("Relative citation counts:")
plist.sort(reverse=True, key=lambda x: x[-1][1])
for p in plist[:50]:
    print("Paper: ", p[2])
    print("Authors: ", p[3])
    print("Date: ", p[0][0])
    print("Relative Citation Count: ", p[-1][1])
    relcitepapers[p[-1][1]] = p[:-1]

with open("relcitepapers.json", "w") as f:
    json.dump(relcitepapers, f, sort_keys=False)
