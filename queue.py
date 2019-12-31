from error import QueueUnderflow
from stack import SStack

class SQueue:
    def __init__(self, init_len=8):
        self._len = init_len
        self._elems = [0] * init_len
        self._head = 0
        self._num = 0

    def is_empty(self):
        return self._num == 0

    def peek(self):
        if self._num == 0:
            raise QueueUnderflow("in peek.")
        return self._elems[self._head]

    def dequeue(self):
        if self._num == 0:
            raise QueueUnderflow("in dequeue.")
        e = self._elems[self._head]
        self._head = (self._head+1) % self._len
        self._num -= 1
        return e

    def enqueue(self, e):
        if self._num == self._len:
            self._extend()
        self._elems[(self._head+self._num) % self._len] = e
        self._num += 1

    def _extend(self):
        old_len = self._len
        self._len *= 2
        new_elems = [0] * self._len
        for i in range(old_len):
            new_elems[i] = self._elems[(self._head+i) % old_len]
        self._elems, self._head = new_elems, 0


# 队列应用
# 迷宫求解
# 1.递归 2.栈 3.队列

dirs = [(0,1), (1,0), (0,-1), (-1,0)]

def mark(maze, pos):
    maze[pose[0]][pos[1]] = 2
def passable(maze, pos):
    return maze[pose[0]][pose[1]] == 0

# 递归求解
def find_path(maze, pos, end):
    mark(maze, pos)
    if pos == end:
        print(pos, end=" ")
        return True
    for i in range(4):
        nextp = pos[0]+dirs[i][0], pos[1]+dirs[i][1]
        if passable(maze, nextp):
            if find_path(maze, nextp, end):
                print(pos, end=" ")
                return True
    return False

# 栈
def maze_solver(maze, start, end):
    if start == end:
        print(start)
        return
    st == SStack()
    mark(maze, start)
    st.push((start, 0))
    while not st.is_empty():
        pos, nxt = st.pop()
        for i in range(nxt, 4):
            nextp = pos[0]+dirs[i][0], pos[1]+dirs[i][1]
            if nextp == end:
                print_path(end, pos, st)
                return
            if passable(maze, nextp):
                st.push((pos, i+1))
                mark(maze, nextp)
                st.push((nextp, 0))
                break
    print("No path found.")

# 队列
def maze_solver_queue(maze, start, end):
    if start == end:
        print("Path find.")
        return
    qu = SQueue()
    mark(maze, start)
    qu.enqueue(start)
    while not qu.is_empty():
        pos = qu.dequeue()
        for i in range(4):
            nextp = pos[0]+dirs[i][0], pos[1]+dirs[i][1]
            if passable(maze, nextp):
                if nextp == end:
                    print("Path find.")
                    return
                mark(maze, nextp)
                qu.enqueue(nextp)
    print("No path.")
