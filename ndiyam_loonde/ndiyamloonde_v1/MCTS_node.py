
from .State import State

class MCTSNode:
    def __init__(self, state:State):
        self._state = state
        self._visits = 0
        self._winrate = 0.0
        self._totalwin = 0.0
        self._parent = None
        self._children:set["MCTSNode"] = []

    @property
    def winrate(self):
        return self._winrate
    
    @property
    def visits(self):
        return self._visits
    
    @property
    def data(self):
        return self._state.text
    
    @property
    def state(self):
        return self._state

    @property
    def totalwin(self):
        return self._totalwin
    
    @property
    def children(self):
        return self._children
    
    @property
    def parent(self):
        return self._parent

    def add_child(self, child_node:"MCTSNode"):
        child_node.set_parent(self)
        self._children.append(child_node)

    def set_parent(self, parent_node:"MCTSNode"):
        self._parent = parent_node
    
    def increase_visits(self):
        self._visits += 1

    def update_winrate(self, data):
        self._totalwin += data
        self._winrate = self._totalwin / max(1,self._visits)