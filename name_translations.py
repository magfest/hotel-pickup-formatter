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


def typo(issue, fix):
    translation[issue] = [fix]

translation["Prince George's Exhibit Hall"] = ["Prince George's Exhibit Hall {}".format(c) for c in "ABCDE"]

translation["Prince George's A-E Registration Desk"] = ["Prince George's {} Registration Desk".format(c) for c in "ABCDE"]

translation["Eastern Shore 1-2"] = ["Eastern Shore {}".format(c) for c in "12"]
translation["Eastern Shore"] = ["Eastern Shore {}".format(c) for c in "123"]

translation["Maryland 1-6"] = ["Maryland {}".format(c) for c in "123456"]
translation["Maryland 4-6"] = ["Maryland {}".format(c) for c in "456"]
translation["Maryland BD/4-6"] = ["Maryland B", "Maryland D"] + translation["Maryland 4-6"]
translation["Maryland A/1-3"] = ["Maryland A"] + ["Maryland {}".format(c) for c in "123"]

translation["Baltimore 1-2"] = ["Baltimore {}".format(c) for c in "12"]
translation["Baltimore 3-5"] = ["Baltimore {}".format(c) for c in "345"]

translation["Camellia 3-4"] = ["Camellia {}".format(c) for c in "34"]

translation["Potomac A-C Lobby"] = translation["Potomac A/C Lobby"] = ["Potomac {} Lobby".format(c) for c in "AC"]

translation["Potomac Registration Desk A-C"] = ["Potomac Registration Desk {}".format(c) for c in "AC"]

translation["Ft. Washington RegDesk"] = ["Ft. Washington Reg Desk"]

translation["Chesa pea ke J-L"] = ["Chesapeake {}".format(c) for c in "JKL"]
translation["Chesapeake J-L"] = ["Chesapeake {}".format(c) for c in "JKL"]

typo("Magnolia2", "Magnolia 2")

typo("PAN AM Foyer", "Pan Am Foyer")

translation["Beech"] = translation["Beech Room"] = ["Beech {}".format(c) for c in "AB"]

translation["Plaza Ballroom"] = ["Plaza Ballroom {}".format(c) for c in "ABC"]

translation["Plaza Ballroom AB"] = ["Plaza Ballroom {}".format(c) for c in "AB"]

typo("Magnolia Room", "Magnolia")