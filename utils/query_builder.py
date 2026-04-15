from itertools import combinations

def build_boolean_queries(keywords, mode="OR"):
    if not keywords:
        return ""
    if mode.upper() == "OR":
        return " OR ".join([f'"{k}"' for k in keywords])
    elif mode.upper() == "AND":
        return " AND ".join([f'"{k}"' for k in keywords])
    elif mode.upper() == "COMBO":
        combos = combinations(keywords, 2)
        return [" AND ".join(c) for c in combos]