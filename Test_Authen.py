from AuthenticatedQuery import authenticated_query
from CommutativeHasing import chash, chash_sequence
from SkipList import SkipList, INF
from SkipListHash import f

skip_list = SkipList([
    [-INF,                                             INF], # Level 5
    [-INF,     17,                                     INF], # Level 4
    [-INF,     17,         25,                     55, INF], # Level 3
    [-INF,     17,         25, 31,                 55, INF], # Level 2
    [-INF, 12, 17,         25, 31, 38,     44,     55, INF], # Level 1
    [-INF, 12, 17, 20, 22, 25, 31, 38, 39, 44, 50, 55, INF], # Level 0
])

assert skip_list.height == 6
assert skip_list.get(12).elem == 12
assert skip_list.get(12).level == 0
assert skip_list.get(77) is None


assert chash(1, 2) == chash(2, 1)
assert chash(1, 2) != chash(2, 3)
assert chash(chash(2, 3), 1) == chash(chash(3, 2), 1) == chash(1, chash(3, 2)) == chash(1, chash(2, 3))
assert chash_sequence([1,2]) == chash(1, 2)
assert chash_sequence([1,2,3]) == chash(1, chash(2, 3))
assert chash_sequence([1,3,2]) == chash(1, chash(2, 3))
assert chash_sequence([1,2,3,4]) == chash(1, chash(2, chash(3, 4)))


# f should be deterministic for a given start node in a list.
assert f(skip_list.start) == f(skip_list.start)

# Some examples of `f` that are simples enough to expand in my head.
assert f(skip_list.get(38)) == chash(38, chash(39, 44))
assert f(skip_list.get(38).up) == chash(chash(38, chash(39, 44)), chash(44, chash(50, 55)))

# From Figure 7 description, the authentication information should be the same
assert authenticated_query(skip_list, 39) == authenticated_query(skip_list, 42)


# Confirm that query information for missing and non-missing values all hash correctly
fs = f(skip_list.start)
for x in range(1, 100):
    qx = authenticated_query(skip_list, x)
    assert chash_sequence(qx) == fs