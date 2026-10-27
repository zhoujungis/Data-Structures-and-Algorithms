# 【LC 143】重排链表：一题拆三题，中间那道刷过

**来源**: https://zhoujungis.github.io/article/lc-143-reorder-list/
**标签**: 算法、链表、LeetCode、面试
**难度**: 中等

## 题目

给定一个单链表 `L`：`L0 → L1 → … → Ln-1 → Ln`，重新排列为：`L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …`。

**不能只是修改节点内部的值，须实际改动节点**（即只能改 `next` 指针、重新排列节点本身）。

```
输入：head = [1,2,3,4]
输出：[1,4,2,3]
```

奇数长度同理，中间节点留在原位：

```
输入：head = [1,2,3,4,5]
输出：[1,5,2,4,3]
```

节点定义：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

## 思路

- 重排的形态是「前半段顺序不变，后半段倒过来，再一个一个插进前半段的缝隙」，因此可拆成三个已做过的子问题：找中点（LC 876）、反转后半段（LC 206）、交替合并（LC 21 的插入动作）。
- 找中点用快慢指针，`fast` 从 `head.next` 起步、条件 `while fast and fast.next`，让 `slow` 停在**前半段的最后一个节点**上；奇数长度时中点归前半段（否则中间节点会被搬到末尾）。
- **`slow.next = None` 断开是本题最要命的一行**：少了它，前半段尾巴仍连着后半段，合并时指针绕成环，LeetCode 上表现为 TLE 而不是报错。
- 反转必须写迭代（O(1) 空间），递归会把空间抬到 O(L/2) 且有爆栈风险。
- 合并循环条件写 `while second`（后半段更短，用完即止），且必须先把两条链的「下家」存进 `t1/t2` 再改指针，顺序不能反。
- 返回值为 `void`：头节点始终是原来的 `head`，不要 `return head`。

## 答案

### 解法一：找中点 + 反转后半段 + 交替合并（时间 O(L) / 空间 O(1)）

```python
def reorderList(head):
    if not head or not head.next:
        return                      # 长度 0/1，无需重排

    # ① 找中点：slow 停在前半段的最后一个节点
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # ② 断开 + 反转后半段
    second = slow.next
    slow.next = None                # 断开，否则合并时会成环
    prev, curr = None, second
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    # ③ 交替合并
    first, second = head, prev
    while second:
        t1, t2 = first.next, second.next
        first.next = second
        second.next = t1
        first, second = t1, t2
```

### Java 版

```java
class Solution {
    public void reorderList(ListNode head) {
        if (head == null || head.next == null) return;

        // ① 找中点
        ListNode slow = head, fast = head.next;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        // ② 断开 + 反转后半段
        ListNode second = slow.next;
        slow.next = null;                 // 断开
        ListNode prev = null, curr = second;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }

        // ③ 交替合并
        ListNode first = head;
        second = prev;
        while (second != null) {
            ListNode t1 = first.next, t2 = second.next;
            first.next = second;
            second.next = t1;
            first = t1;
            second = t2;
        }
    }
}
```
