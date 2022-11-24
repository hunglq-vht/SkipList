from AuthenticatedQuery import authenticated_query
from CommutativeHasing import chash, chash_sequence
from SkipList import SkipList, INF
from SkipListHash import f

skip_list = SkipList([
    [(-INF, -INF),                                                                                                     (INF, INF)], # Level 5
    [(-INF, -INF),          (1, 17),                                                                                   (INF, INF)], # Level 4
    [(-INF, -INF),          (1, 17),                   (7, 25),                                               (6, 55), (INF, INF)], # Level 3
    [(-INF, -INF),          (1, 17),                   (7, 25), (4, 31),                                      (6, 55), (INF, INF)], # Level 2
    [(-INF, -INF), (2, 12), (1, 17),                   (7, 25), (4, 31), (8, 38),           (3, 44),          (6, 55), (INF, INF)], # Level 1
    [(-INF, -INF), (2, 12), (1, 17), (0, 20), (5, 22), (7, 25), (4, 31), (8, 38), (10, 39), (3, 44), (9, 50), (6, 55), (INF, INF)], # Level 0
])

assert skip_list.height == 6
assert skip_list.get((2, 12)).elem == (2, 12)
print(skip_list.get((2, 12)))


assert chash(1, 2) == chash(2, 1)
assert chash(1, 2) != chash(2, 3)
assert chash(chash(2, 3), 1) == chash(chash(3, 2), 1) == chash(1, chash(3, 2)) == chash(1, chash(2, 3))
assert chash_sequence([1,2]) == chash(1, 2)
assert chash_sequence([1,2,3]) == chash(1, chash(2, 3))
assert chash_sequence([1,3,2]) == chash(1, chash(2, 3))
assert chash_sequence([1,2,3,4]) == chash(1, chash(2, chash(3, 4)))


print(skip_list.start)
# # f should be deterministic for a given start node in a list.
assert f(skip_list.start) == f(skip_list.start)

# Some examples of `f` that are simples enough to expand in my head.
assert f(skip_list.get((8, 38))) == chash(chash(8, 38), chash(chash(10, 39), chash(3, 44)))
# assert f(skip_list.get(38).up) == chash(chash(38, chash(39, 44)), chash(44, chash(50, 55)))

# # From Figure 7 description, the authentication information should be the same
assert authenticated_query(skip_list, (10, 39)) == authenticated_query(skip_list, (17, 42))


# # Confirm that query information for missing and non-missing values all hash correctly
# fs = f(skip_list.start)
# for x in range(1, 100):
#     qx = authenticated_query(skip_list, x)
#     assert chash_sequence(qx) == fs