# 【LC 19】删除链表倒数第 N 个：快指针先出发

**来源**: https://zhoujungis.github.io/article/lc-19-remove-nth-from-end/
**标签**: 算法、链表、LeetCode、面试
**难度**: 中等

## 题目

给你一个链表，删除链表的倒数第 `n` 个结点，并且返回链表的头结点。要求**一趟扫描**实现。

```
输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]
```

链表节点的定义（后面所有代码都用它）：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

约束：`1 ≤ n ≤ 链表长度`。

## 思路

- 删除的关键不是待删节点本身，而是它的**前驱**：`前驱.next = 前驱.next.next` 一行完成删除，所以目标是定位**倒数第 n+1 个**节点。
- 核心技巧是「间隔锁死」：`fast` 先走 `n+1` 步，然后两个指针同步前进，`fast` 走到 `null` 时 `slow` 恰好停在倒数第 `n+1` 个（待删节点的前驱）。必须走 `n+1` 而不是 `n`，因为我们要停在前驱上。
- 「间距 `n+1` 始终不变」是唯一的不变量，同步阶段的每一次移动都保持它，因此终点位置可被精确推出。
- 引入哑结点 `ListNode(0, head)`：给头节点凭空造一个前驱，把「删头」变成普通删除，否则 `[1], n=1` 这类用例必须特判。
- 返回值必须是 `dummy.next` 而不是 `head`——当 `n` 等于链长时头节点已被摘掉，返回 `head` 等于返回一个已不在链上的节点。
- 两种约定都能写对：「先走 `n` 步 + `while fast.next`」或「先走 `n+1` 步 + `while fast`」，但**绝不能混用**，混用必然差一个身位、删错节点。

## 答案

### 解法一：快慢指针一趟扫描（+ 哑结点）（时间 O(L) / 空间 O(1)）

```python
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    fast = dummy
    for _ in range(n + 1):       # ① fast 先走 n+1 步
        fast = fast.next

    slow = dummy                 # ② slow 从 dummy 出发
    while fast:                  # ③ 两个指针同步前进
        fast = fast.next
        slow = slow.next

    slow.next = slow.next.next   # ④ slow 停在前驱上，摘掉目标节点
    return dummy.next            # ⑤ 返回 dummy.next，而不是 head
```

### Java 版

```java
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0, head);
        ListNode fast = dummy;
        for (int i = 0; i < n + 1; i++) {   // ① 先走 n+1 步
            fast = fast.next;
        }
        ListNode slow = dummy;
        while (fast != null) {              // ③ 同步前进
            fast = fast.next;
            slow = slow.next;
        }
        slow.next = slow.next.next;         // ④ 删除
        return dummy.next;                  // ⑤ 注意不是 head
    }
}
```
