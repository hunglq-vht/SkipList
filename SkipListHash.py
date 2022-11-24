from CommutativeHasing import chash


def f(v):
    """
        Calculate hash value of node v inside skip list.
    """
    w = v.right
    u = v.down
    # node ben phai v la None thi gia tri hash la 0 
    if w is None:
        return 0
    
    # Case 1: Dang o muc duoi cung trong skip list
    if u is None:
        # Case 1a: Node ben phai la "tower"
        if w.is_tower:
            return chash(chash(v.elem[0], v.elem[1]), chash(w.elem[0], w.elem[1]))
        # Case 1b: Node ben phai la "plateau".
        return chash(chash(v.elem[0], v.elem[1]), f(w))
    else:
        # Case 2a: node ben phai la "tower" va dang khong o cung level 
        if w.is_tower:
            return f(u)
        # Case 2b: Node ben phai "plateau" va dang khong o cung level
        return chash(f(u), f(w))