
class DijkstraNode:
    """Models a single node in a graph, running Dijkstra's algorithm.

       Create a new node (when the algorithm begins) using the constructor.

       Call update_dist(dist) (valid so long as the node has not been marked
       'done') to set (or reduce) the distance to this node.  It is *NOT*
       legal to increase the distance at any time!!!

       Call is_reached() to see if this node has ever been reached at any
       time in the past.  (Will also return true if the node is done.)
       This will return False until you call update_dist(), and True forever
       after that.

       Call is_done() to see if the node has already found its final distance,
       or set_done() to set the flag.

       Call get_dist() to get the current distance (which might or might not
       be the final value.  (It's illegal to call this before update_dist()
       was called the first time.)
    """


    def __init__(self):
        self._dist = None       # not reached yet, treat as infinite distance
        self._done = False

    def is_done(self):
        return self._done

    def is_reached(self):
        return self._dist is not None

    def get_dist(self):
        assert self._dist is not None
        return self._dist

    def update_dist(self, new_dist):
        assert new_dist >= 0
        assert not self._done
        assert self._dist is None or new_dist < self._dist
        self._dist = new_dist

    def set_done(self):
        assert not self._done
        self._done = True

