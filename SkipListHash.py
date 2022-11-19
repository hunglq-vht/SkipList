from CommutativeHasing import chash


def f(v):
    """Computes a hash representing node `v` in a skip list.
    """
    w = v.right
    u = v.down
    # Base case: w/right is None. Default to a zero value.
    if w is None:
        return 0
    
    # Case 1: We are at the bottom level of the skiplist.
    if u is None:
        # Case 1a: The node to our right is a "tower"
        if w.is_tower:
            return chash(chash(v.elem[0], v.elem[1]), chash(w.elem[0], w.elem[1]))
        # Case 1b: The node to our right is a "plateau".
        return chash(chash(v.elem[0], v.elem[1]), f(w))
    else:
        # Case 2a: The node to our right is a "tower" and we are not on the base level 
        if w.is_tower:
            return f(u)
        # Case 2b: The node to our right is a "plateau" and we are not on the base level
        return chash(f(u), f(w))