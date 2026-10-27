# 【LC 155/232】最小栈 & 用栈实现队列：记历史与再翻一次

**来源**: https://zhoujungis.github.io/article/lc-155-232-min-stack-and-queue-via-stacks/
**标签**: 算法、栈、LeetCode、面试

## 题目

### LC 155 最小栈

设计一个栈，支持 `push`、`pop`、`top`，并能在 `O(1)` 时间内取到栈内最小元素 `getMin`。

```
输入: push(-2), push(0), push(-3), getMin(), pop(), top(), getMin()
输出:                getMin → -3
                     top    → 0
                     getMin → -2
```

### LC 232 用栈实现队列

只用两个栈，实现先进先出的队列，支持 `push`、`pop`、`peek`、`empty`。

```
输入: push(1), push(2), push(3), pop(), peek(), pop()
输出: pop → 1, peek → 2, pop → 2
```

## 思路

- **LC 155——难点是「历史」不是「当前」**：`getMin` 要 O(1)，而最小值埋在栈里任意一层；真正难的是 `pop` 掉最小值之后要回到**过去**的最小值，它必须本来就存着，不可能现场算又不扫描。
- **LC 155——同步辅助栈按层存**：主栈每压入一个 `x`，辅助栈就记下「x 入栈这一刻的全栈最小值」，不变量是**辅助栈顶恒等于全栈最小值**，`pop` 时两栈一起弹，旧最小值自动恢复。
- **LC 155——判据必须是 `<=`**：相等也是「这一刻的最小值」，写成 `<` 时 `push(2), push(2), pop` 会让辅助栈提前变空、`getMin` 崩；`pop` 时也只有弹掉的值**等于**辅助栈顶才跟着弹，否则会把还没发生的最小值提前扔掉。
- **LC 232——两次反转等于正序**：元素进 `in` 被倒一次，把 `in` 整摞翻进 `out` 再倒一次，最早来的沉到 `out` 顶，`out` 顶就是队首。
- **LC 232——两条钉子缺一不可**：只在 `out` **空时**才搬运（否则新元素插到老元素前面，队首就错了），搬运必须**整摞翻完**（搬一半会让「新的压在旧的上面」）。
- **均摊账本**：每个元素一生至多三次栈操作（进 `in`、搬一次、出 `out`），`n` 次操作总花费 `O(n)`，即均摊 `O(1)`、单次 `pop` 最坏 `O(n)`。

## 答案

### LC 155

#### 解法一：同步辅助栈记录每层最小值（时间 O(1) / 空间 O(n)）

```python
class MinStack:
    def __init__(self):
        self.main = []
        self.mins = []

    def push(self, x):
        self.main.append(x)
        # 判据是 <=（相等也压），见 9.1
        if not self.mins or x <= self.mins[-1]:
            self.mins.append(x)

    def pop(self):
        x = self.main.pop()
        if x == self.mins[-1]:      # 弹的是当前最小值 → 同步弹
            self.mins.pop()
        return x

    def top(self):
        return self.main[-1]

    def getMin(self):
        return self.mins[-1]        # O(1)：读历史栈顶
```

#### Java 版

```java
class MinStack {
    Deque<Integer> main = new ArrayDeque();
    Deque<Integer> mins = new ArrayDeque();

    public void push(int x) {
        main.push(x);
        if (mins.isEmpty() || x <= mins.peek()) {
            mins.push(x);                    // 判据 <=，相等也压
        }
    }

    public void pop() {
        if (main.pop().equals(mins.peek())) { // Integer 比较用 equals
            mins.pop();
        }
    }

    public int top()    { return main.peek(); }
    public int getMin() { return mins.peek(); }
}
```

### LC 232

#### 解法一：双栈 in / out，懒搬运（时间均摊 O(1)、单次最坏 O(n) / 空间 O(n)）

```python
class MyQueue:
    def __init__(self):
        self.inn = []
        self.out = []

    def push(self, x):
        self.inn.append(x)          # O(1)，直接进

    def _shift(self):
        if not self.out:            # 钉子一：out 空了才搬
            while self.inn:         # 钉子二：整摞翻
                self.out.append(self.inn.pop())

    def pop(self):
        self._shift()
        return self.out.pop()

    def peek(self):
        self._shift()
        return self.out[-1]

    def empty(self):
        return not self.inn and not self.out
```

#### Java 版

```java
class MyQueue {
    Deque<Integer> in = new ArrayDeque();
    Deque<Integer> out = new ArrayDeque();

    public void push(int x) { in.push(x); }

    private void shift() {
        if (out.isEmpty()) {                 // out 空才搬
            while (!in.isEmpty()) {          // 整摞翻
                out.push(in.pop());
            }
        }
    }

    public int pop()   { shift(); return out.pop(); }
    public int peek()  { shift(); return out.peek(); }
    public boolean empty() { return in.isEmpty() && out.isEmpty(); }
}
```
