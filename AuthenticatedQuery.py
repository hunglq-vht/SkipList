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
    
    # the algorithm in Figure 6 has a typo. It assigns $x1$ (The second element of Q(x))
    # to the value $x$. This cannot be correct, as $x$ is not guaranteed to exist in the
    # skip list. Based on other examples in the paper, I believe $v1$ is the intended value here.
    # px[0] = the paper's $v1$.
    qx.append(px[0].elem)
    
    # Paper is using one-indexing but Python uses zero-indexing.
    # Hence, I start at 1 here, not 2.
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
            
    # The special cases from 4.3, where the searched for element does not match $v1$.
    v1 = px[0]
    qxr = list(reversed(qx))
    if v1.elem != element:
        w1 = v1.right
        z = v1.right.right
        # w1 is a tower node, return Q(x) as-is
        if w1.is_tower:
            return qxr
        if w1.is_plateau and z.is_tower:
            # I believe one of these elements from Q(X) should be dropped in this case.
            return qxr[:-1] + [z.elem, w1.elem]
        if w1.is_plateau and z.is_plateau:
            # I believe one of these elements from Q(X) should be dropped in this case.
            return qxr[:-1] + [f(z), w1.elem]
    return qxr
