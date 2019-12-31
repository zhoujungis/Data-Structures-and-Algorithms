from prioqueue import PrioQueue

class BinTNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

class BinTree:
    def __init__(self):
        self._root = None

    def is_empty(self):
        return self._root is None

    def root(self):
        return self._root

    def leftchild(self):
        return self._root.left

    def rightchild(self):
        return self._root.right

    def set_root(self, rootnode):
        self._root = rootnode

    def set_left(self, leftchild):
        self._root.left = leftchild

    def set_right(self, rightchild):
        self._root.right = rightchild

    def preorder(self):
        t, s = self._root, SStack()
        while t or not s.is_empty():
            while t:
                s.push(t.right)
                yield t.data
                t = t.left
            t = s.pop()
    
    def postorder(self):
        t, s = self._root, SStack()
        while t or not s.is_empty():
            s.push(t)
            t = t.left if t.left else t.right
        t = s.pop()
        yield t.data
        if not s.is_empty() and s.top().left == t:
            t = s.top().right
        else:
            t = None
    
# 哈夫曼树
class HTNode(BinTNode):
    def __lt__(self, othernode):
        if not isinstance(othernode, HTNode):
            raise ValueError
        return self.data < othernode.data

class HuffmanPrioQ(PrioQueue):
    def number(self):
        return len(self._elems)

def HuffmanTree(weights):
    trees = HuffmanPrioQ()
    for w in weights:
        trees.enqueue(HTNode(w))
    while trees.number() > 1:
        t1 = trees.dequeue()
        t2 = trees.dequeue()
        x = t1.data + t2.data
        trees.enqueue(HTNode(x, t1, t2))
    return trees.dequeue
