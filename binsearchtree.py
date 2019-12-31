from stack import SStack
from bintree import BinTNode

class Assoc:
     def __init__(self, key, value):
         self.key = key
         self.value = value
         
     def __lt__(self, other):
         if not isinstance(other, Assoc):
             raise ValueError
         return self.key < other.key
     
     def __le__(self, other):
         if not isinstance(other, Assoc):
             raise ValueError
         return self.key < other.key or self.key == other.key
     
     def __str__(self):
         return "Assoc({0},{1}).format(self.key, self.value)"

class DictBinTree:
     def __init__(self):
         self._root = None
         
     def is_empty(self):
         return self._root is None
     
     def search(self, key):
         bt = self._root
         while bt:
             entry = bt.data
             if key < entry.key:
                 bt = bt.left
             elif key > entry.key:
                 bt = bt.right
             else:
                 return entry.value
         return None
     
     def insert(self, key, value):
         bt = self._root
         if bt is None:
             self._root = BinTNode(Assoc(key, value))
             return
         while True:
             entry = bt.data
             if key < entry.key:
                 if bt.left is None:
                     bt.left = BinTNode(Assoc(key, value))
                     return
                 bt = bt.left
             elif key > entry.key:
                 if bt.right is None:
                     bt.right = BinTNode(Assoc(key, value))
                     return
                 bt = bt.right
             else:
                 bt.data.value = value
                 return
               
     def values(self):
         t, s = self._root, SStack()
         while t or not s.is_empty():
             while t:
                 s.push(t)
                 t = t.left
             t = s.pop()
             yield t.data.key, t.data.value
             t = t.right
             
     def delete(self, key):
         p, q = None, self._root
         
         while q and q.data.key != key:
             p = q
             if key < q.data.key:
                 q = q.left
             else:
                 q = q.right
         if q is None:
             return
         if q.left is None:
             if p is None:
                 self._root = q.right
             elif q is p.left:
                 p.left = q.right
             else:
                 p.right = q.right
             return

         r = q.left
         while r.right:
             r = r.right
         r.right = q.right
         if p is None:
             self._root = q.left
         elif p.left is q:
             p.left = q.left
         else:
             p.right = q.left
             
     def print(self):
         for k, v in self.values():
             print(k, v)
