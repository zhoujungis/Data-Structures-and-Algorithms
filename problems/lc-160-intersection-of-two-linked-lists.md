# 【LC 160】相交链表：让 pA 走完 A 去走 B，两条路就一样长了

**来源**: https://zhoujungis.github.io/article/lc-160-intersection-of-two-linked-lists/
**标签**: 算法、链表、LeetCode、面试
**难度**: 简单

## 题目

给你两个单链表的头节点 `headA` 和 `headB`，请你找出并返回两个单链表相交的**起始节点**。如果两个链表不存在相交节点，返回 `null`。

图示两个链表在节点 `c1` 开始相交：

```
A:        a1 → a2
                 ↘
                   c1 → c2 → c3
                 ↗
B:   b1 → b2 → b3
```

题目数据**保证**整个链式结构中不存在环。

**注意**，函数返回结果后，链表必须**保持其原始结构**。

```
输入：intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skipA = 2, skipB = 3
输出：Intersected at '8'

输入：intersectVal = 2, listA = [1,9,1,2,4], listB = [3,2,4], skipA = 3, skipB = 1
输出：Intersected at '2'

输入：intersectVal = 0, listA = [2,6,4], listB = [1,5], skipA = 3, skipB = 2
输出：No intersection
```

**进阶**：你能否设计一个时间复杂度 `O(n + m)`、仅用 `O(1)` 内存的解决方案？

链表节点的定义（后面所有代码都用它）：

```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
```

## 思路

- **相交的判据是节点（引用），不是值**：两个链表共享的是同一批节点对象，形态必然是 **Y 字形**（一旦相交后面必须完全重合，因为每个节点只有一个 `next`），答案是共享后缀的起点。值相同的不同节点不算相交。
- **核心洞察：让两个指针走一样长的路**。设 A 独有段 `a`、B 独有段 `b`、公共段 `c`：pA 走完 A 接着走 B，路程 `a + c + b`；pB 走完 B 接着走 A，路程 `b + c + a`。加法交换律保证两者相等，速度相同、出发同时，因此**必然同时到达相交点**。
- **不相交也被同一套逻辑覆盖**：`c = 0` 时两者各走 `a + b` 步后**同时变成 `None`**，`while pA is not pB` 恰好成立退出，返回 `None` —— 不需要任何特判。
- **换头是合法的读操作**：只是指针变量改指向，没有修改任何 `next`，所以不破坏原始结构、也不会成环，空间自然 `O(1)`。
- **易错：换头判据要写 `if pA`（自己是不是 None），不能写 `if pA.next`** —— 后者会在最后一个真实节点就提前换头，少走一格，两条路就不等长了；循环条件同理写 `while pA is not pB`，而非 `while pA and pB`。

## 答案

### 解法一：双指针交换游标（时间 O(n + m) / 空间 O(1)）

```python
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        pA, pB = headA, headB
        while pA is not pB:          # 比的是"是不是同一个节点"，不是值
            pA = pA.next if pA else headB   # 走完 A 就换到 B 的头
            pB = pB.next if pB else headA   # 走完 B 就换到 A 的头
        return pA                    # 要么是相交点，要么是 None
```

### Java 版

```java
public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        if (headA == null || headB == null) return null;

        ListNode pA = headA, pB = headB;
        while (pA != pB) {                 // 比引用，不是比值
            pA = (pA == null) ? headB : pA.next;   // 走完 A 就换到 B 的头
            pB = (pB == null) ? headA : pB.next;   // 走完 B 就换到 A 的头
        }
        return pA;                          // 相交点，或 null
    }
}
```
