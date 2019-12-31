from error import LinkedListUnderflow

class LNode:
     def __init__(self, elem, next_=None):
          self.elem = elem
          self.next = next_

class DLNode(LNode):
     def __init__(self, elem, prev=None, next_=None):
          LNode.__init__(self, elem, next_)
          self.prev = prev

# 单链表
class LList:
     def __init__(self):
          self._head = None

     def is_empty(self):
          return self._head is None

     def prepend(self, e):
          self._head = LNode(e, self._head)

     def append(self, e):
          if self.is_empty():
               self._head = LNode(e)
               return
          p = self._head
          while p.next:
               p = p.next
          p.next = LNode(e)

     def pop(self):
          if self.is_empty():
               raise LinkedListUnderflow("in pop.")
          e = self._head.elem
          self._head = self._head.next
          return e

     def pop_last(self):
          if self.is_empty():
               raise LinkedListUnderflow("in pop_last.")
          p = self._head
          if p.next is None:
               e = p.elem
               self._head = None
               return e
          while p.next.next:
               p = p.next
          e = p.next.elem
          p.next = None
          return e

     def find(self, pred):
          p = self._head
          while p:
               if pred(p.elem):
                    return p.elem
               p = p.next

     def printall(self):
          p = self._head
          while p:
               print(p.elem, end="")
               if p.next:
                   print(", ", end="")
               p = p.next
          print("")

     def for_each(self, proc):
          p = self._head
          while p:
               proc(p.elem)
               p = p.next

     def elements(self):
          p = self._head
          while p:
               yield p.elem
               p = p.next

     def filter(self, pred):
          p = self._head
          while p:
               if pred(p.elem):
                    yield p.elem
               p = p.next

     def rev(self):
          p = None
          while self._head:
               q = self._head
               self._head = q.next
               q.next = p
               p = q
          self._head = p

# 加入尾结点的链表
class LList1(LList):
     def __init__(self):
          LList.__init__(self)
          self._rear = None

     def prepend(self, e):
          if self._head is None:
               self._head = LNode(e, self._head)
               self._rear = self._head
          else:
               self._head = LNode(e, self._head)

     def append(self, e):
          if self._head is None:
               self._head = LNode(e, self._head)
               self._rear = self._head
          else:
               self._rear.next = LNode(e)
               self._rear = self._rear.next
               
     def pop_last(self):
          if self._head is None:
               raise LinkedListUnderflow("in pop_last.")
          p = self._head
          if p.next is None:
               e = p.elem
               self._head = None
               return e
          while p.next.next:
               p = p.next
          e = p.next.elem
          p.next = None
          self._rear = p
          return e

# 循环单链表
class LCList:
     def __init__(self):
          self._rear = None

     def is_empty(self):
          return self._rear is None

     def prepend(self, e):
          p = LNode(e)
          if self.is_empty():
               p.next = p
               self._rear = p
          else:
               p.next = self._rear.next
               self._rear.next = p

     def append(self, e):
          self.prepend(e)
          self._rear = self._rear.next

     def pop(self):
          if self.is_empty():
               raise LinkedListUnderflow("in pop.")
          p = self._rear.next
          if self._rear is p:
               self._rear = None
          else:
               self._rear.next = p.next
          return p.elem

     def pop_last(self):
          if self.is_empty():
               raise LinkedListUnderflow("in pop_last.")
          p = self._rear
          while p.next is not self._rear:
               p = p.next
          self._rear = p
          return self.pop()

     def printall(self):
          if self.is_empty():
               return
          p = self._rear.next
          while True:
               print(p.elem)
               if p is self._rear:
                    break
               p = p.next

# 双链表
class DLList(LList1):
     def __init__(self):
          LList1.__init__(self)

     def prepend(self, e):
          p = DLNode(e, None, self._head)
          if self._head is None:
               self._rear = p
          else:
               p.next.prev = p
          self._head = p

     def append(self, e):
          p = DLNode(e, self._rear, None)
          if self._head is None:
               self._head = p
          else:
               p.prev.next = p
          self._rear = p

     def pop(self):
          if self._head is None:
               raise LinkedListUnderflow("in pop.")
          e = self._head.elem
          self._head = self._head.next
          if self._head:
               self._head.prev = None
          return e

     def pop_last(self):
          if self._head is None:
               raise LinkedListUnderflow("in pop_last.")
          e = self._rear.elem
          self._rear = self._rear.prev
          if self._rear is None:
               self._head = None
          else:
               self._rear.next = None
          return e

# 循环双链表
class DLCList:
     def __init__(self):
          self._rear = None

     def is_empty(self):
          return self._rear is None

     def prepend(self, e):
          p = DLNode(e)
          if self.is_empty():
               p.next = p
               p.prev = p
               self._rear = p
          else:
               p.prev = self._rear
               self._rear.next.prev = p
               p.next = self._rear.next
               self._rear.next = p

     def append(self, e):
          self.prepend(e)
          self._rear = self._rear.next

     def pop(self):
          if self.is_empty():
               raise LinkedListUnderflow("in pop.")
          p = self._rear.next
          if self._rear is p:
               self._rear = None
          else:
               self._rear.next = p.next
               p.next.prev, p.prev.next = p.prev, p.next
          return p.elem

     def pop_last(self):
          if self.is_empty:
               raise LinkedListUnderflow("in pop_last.")
          p = self._rear
          if self._rear.next is p:
               self._rear = None
          else:
               self._rear = self._rear.prev
               self._rear.next = p.next
               p.next.prev, p.prev.next = p.prev, p.next
          return p.elem

     def printall(self):
          if self.is_empty():
               return
          p = self._rear.next
          while True:
               print(p.elem)
               if p is self._rear:
                    break
               p = p.next

# 单链表应用——求解Josephus环问题
# 1.数组求解；2.顺序表求解；3.循环单链表求解

def josephus_A(n, k, m):
     people = list(range(1, n+1))
     i = k - 1
     for num in range(n):
          count = 0
          while count < m:
               if people[i] > 0:
                    count += 1
               if count == m:
                    print(people[i], end="")
                    people[i] = 0
               i = (i + 1) % n
          if num < n - 1:
               print(", ", end="")
          else:
               print("")
     return

def josephus_L(n, k, m):
     people = list(range(1, n+1))
     i = k-1
     for num in range(n, 0, -1):
          i = (i + m - 1) % num
          print(people.pop(i), end=(", " if num > 1 else "\n"))
     return

class Josephus(LCList):
     def turn(self, m):
          for i in range(m):
               self._rear = self._rear.next

     def __init__(self, n, k, m):
          LCList.__init__(self)
          for i in range(n):
               self.append(i+1)
          self.turn(k-1)
          while not self.is_empty():
               self.turn(m-1)
               print(self.pop(), end=(", " if not self.is_empty() else "\n"))
