# hotel often gives us data in really weird formats that aren't nice machine-readable names
# use this list to translate back to our nice names.


def name_nums(basename, start, end):
    return [basename + str(i) for i in range(start, end+1)]


def alpha_nums(basename, start, end):
    return [basename + chr(i) for i in range(ord(start), ord(end)+1)]

translation = dict()


def breakup(basename, *permutations):
    for p in permutations:
        translation[basename + " " + p] = [basename + " " + c for c in p]

for e in ["Prince George's Prefunction", "Prince George's Exhibit Hall"]:
    breakup(e, "ABCDE")
    breakup(e, "ABCD", "BCDE")
    breakup(e, "ABC", "BCD", "CDE")
    breakup(e, "AB", "BC", "CD", "DE")

translation["Prince George's A-E Registration Desk"] = ["Prince George's {} Registration Desk".format(c) for c in "ABCDE"]

translation["Maryland 1-6"] = ["Maryland {}".format(c) for c in "123456"]
translation["Maryland 4-6"] = ["Maryland {}".format(c) for c in "456"]
translation["Maryland BD/4-6"] = ["Maryland B", "Maryland D"] + translation["Maryland 4-6"]
translation["Maryland A/1-3"] = ["Maryland A"] + ["Maryland {}".format(c) for c in "123"]

translation["Baltimore 1-2"] = ["Baltimore 1", "Baltimore 2"]

translation["Camellia 3-4"] = ["Camellia {}".format(c) for c in "34"]

translation["Potomac A/C Lobby"] = ["Potomac {} Lobby".format(c) for c in "AC"]

translation["Potomac Registration Desk A-C"] = ["Potomac Registration Desk {}".format(c) for c in "AC"]
