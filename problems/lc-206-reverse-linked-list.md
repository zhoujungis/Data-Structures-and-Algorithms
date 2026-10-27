# 【LC 206】反转链表：指针一改就断链，问题到底出在哪

**来源**: https://zhoujungis.github.io/article/lc-206-reverse-linked-list/
**标签**: 算法、链表、LeetCode、面试
**难度**: 简单

## 题目

给你单链表的头节点 `head`，请你反转链表，并返回反转后的链表。

```
输入：head = [1,2,3,4,5]
输出：[5,4,3,2,1]
```

链表节点的定义（后面所有代码都用它）：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

## 思路

- 把「反转」翻译成指针操作只有一句话：**把每个节点的 `next` 从「指向后面那个」改成「指向前面那个」**；难点不在改什么，而在改的**时机**。
- 链表的节点只认「我的下一个是谁」，一旦把 `curr.next` 改掉，原来后面的节点就永远找不到——所以每轮必须**先记住 `next`、再掉头、后前移**，漏掉第一步当场断链。
- 迭代用三个指针：`prev` 是已反转段的头（初值 `None`，因为原头节点将变成尾、其 `next` 必须为空），`curr` 是待处理节点，`nxt` 只是临时存档。`prev` 与 `curr` 之间永远隔着一道「已反转 / 未反转」的分界线，每轮右移一格。
- 顺序不可交换：先 `curr.next = prev` 再 `prev = curr`，否则 ② 用到的 `prev` 已是错值；`curr` 必须用 ① 存下的 `nxt` 前进。
- 循环结束时 `curr` 为 `None`，要 **`return prev`**（新头）；返回 `curr` 就是返回空链表，这是最高频的低级错误。空链表、单节点、两节点都无需特判，循环天然覆盖。
- 递归思路换个方向：`reverseList(head.next)` 已把后面整段反转好并返回新头，只需 `head.next.next = head` 让「反转后那段的尾」指向自己，再 `head.next = None`。**漏掉 `head.next = None` 会成环**（打印时死循环）。
- 递归终止条件必须是 `not head or not head.next`：只写后者，输入 `None` 会崩；只写前者，单节点会多递归一层。
- 空间代价是考点：递归 O(n) 来自函数调用栈（Python 默认 1000 层即 `RecursionError`，Java 也会 `StackOverflowError`），真实工程与默认答法都用迭代 O(1)。

## 答案

### 解法一：迭代（三指针）（时间 O(n) / 空间 O(1)）

任何长度都安全，面试首选。

```python
def reverseList(head):
    prev = None          # 反转后的尾节点，它的 next 必须是空
    curr = head          # 从原头节点开始

    while curr:          # curr 走到 None 就结束
        nxt = curr.next  # ① 先记住下一个
        curr.next = prev # ② 掉头
        prev = curr      # ③ prev 前移
        curr = nxt       # ④ curr 前移

    return prev          # 注意：返回 prev，不是 curr
```

### 解法二：递归（时间 O(n) / 空间 O(n)）

代码最短，但栈深 O(n)，长链表会爆栈。

```python
def reverseList(head):
    # 终止条件：空链表，或者只剩一个节点
    if not head or not head.next:
        return head

    new_head = reverseList(head.next)  # 先把后面整段反转好
    head.next.next = head              # 让后面的尾节点指向自己
    head.next = None                   # 自己成为新的尾节点
    return new_head                    # 新头节点一路原样传回去
```

### Java 版

```java
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nxt = curr.next;  // ① 先记住
            curr.next = prev;          // ② 掉头
            prev = curr;               // ③ 前移
            curr = nxt;                // ④ 前移
        }
        return prev;
    }
}
```
