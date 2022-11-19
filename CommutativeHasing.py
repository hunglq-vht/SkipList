import hashlib

from SkipList import INF

def chash(x, y):
    """Commutative hashing algorithm as described in Goodrich section 3.2.
    
    Assumes input will always be a 256-bit integer, -Inf, or Inf.
    
    This function truncates the output of SHA-256 for readability 
    but it is not required.
    """
    
    # The Goodirch paper doesn't explicitly state how to handle the -Infinity
    # case but there are cases where it expects us to hash -Infinity elements.
    # E.g. The bottom-left node will hit case (1a) which requires
    # a hash of elem(v).
    # 
    # The Goodrich paper *also* says we don't need to hash Infinity elements
    # but I think it also contradicts itself. Since case (1a) would require the
    # hash of elem(w) which could be infinity if v was a non-plateau node immedietely
    # to the left of an Inf node.
    def _to_bytes(i):
        """Serialize a number into a byte string.

        Assumes input will always be a 256-bit integer. Sentinel values
        -Inf/Inf are serialized using values that are not otherwise
        possible under this assumption.
        """
        if i == INF:
            return b"\xff" * ((256//8)+1)
        elif i == -INF:
            return b"\x00" * ((256//8)+1)
        else:
            return i.to_bytes(256//8, byteorder='big')
    
    fst, sec = min(x, y), max(x, y)
    sha256 = hashlib.sha256()
    sha256.update(_to_bytes(fst))
    sha256.update(_to_bytes(sec))
    return int.from_bytes(sha256.digest(), byteorder='big') % 0xff

def chash_sequence(seq):
    """Hash a sequence of values using the algorithm described in Section 3.
    """
    if len(seq) == 2:
        return chash(seq[0], seq[1])
    return chash(seq[0], chash_sequence(seq[1:]))
