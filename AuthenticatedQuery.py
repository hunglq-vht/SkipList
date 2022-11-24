from SkipListHash import f


def authenticated_query(skiplist, element):
    """Given a `skiplist` and a `element`, return a set of authentication information 
    that can be hashed and compared to `f(skiplist.start)`.
    """
    search_stack = skiplist.search(element)
    px = list(reversed(search_stack))
    
    # build Q(X)
    qx = []
    w1 = px[0].right
    if w1.is_plateau:
        qx.append(f(w1))
    else:
        qx.append(w1.elem)
    

    qx.append(px[0].elem)
    

    for i in range(1, len(search_stack)):
        wi = px[i].right
        if wi.is_plateau:
            if wi != px[i-1]:
                qx.append(f(wi))
            else:
                if px[i].level == 0:
                    qx.append(px[i].elem)
                else:
                    qx.append(f(px[i].down))
            
    v1 = px[0]
    qxr = list(reversed(qx))
    if v1.elem != element:
        w1 = v1.right
        z = v1.right.right
        if w1.is_tower:
            return qxr
        if w1.is_plateau and z.is_tower:
            return qxr[:-1] + [z.elem, w1.elem]
        if w1.is_plateau and z.is_plateau:
            return qxr[:-1] + [f(z), w1.elem]
    return qxr
