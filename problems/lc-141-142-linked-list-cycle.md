# 【LC 141/142】环形链表：为什么快 2 慢 1 一定相遇

**来源**: https://zhoujungis.github.io/article/lc-141-142-linked-list-cycle/
**标签**: 算法、链表、LeetCode、面试
**难度**: 简单（141）/ 中等（142）

## 题目

### LC 141 环形链表

给你一个链表的头节点 `head`，判断链表中是否有环。如果链表中有某个节点，可以通过连续跟踪 `next` 指针再次到达，则链表中存在环。

**进阶**：你能用 `O(1)`（即常量）内存解决此问题吗？

```
输入：head = [3,2,0,-4], pos = 1
输出：true
解释：链表中有一个环，其尾部连接到第二个节点。

输入：head = [1,2], pos = -1
输出：false
解释：链表中没有环。
```

### LC 142 环形链表 II

给定一个链表的头节点 `head`，返回链表开始入环的第一个节点。如果链表无环，则返回 `null`。

```
输入：head = [3,2,0,-4], pos = 1
输出：返回下标为 1 的节点
解释：链表中有一个环，其尾部连接到第二个节点。

输入：head = [1,2], pos = -1
输出：null
解释：链表中没有环。
```

两题公共约束：

- 链表中节点的数目范围是 `[0, 10^4]`
- `-10^5 <= Node.val <= 10^5`
- `pos` 为 `-1` 或者链表中的一个有效索引
- 142 要求**不允许修改**链表

## 思路

- 最直接的是哈希表：边走边记录访问过的节点，撞见重复节点即有环，第一个重复节点就是入口；时间 O(n) 但空间 O(n)。
- Floyd 判圈（龟兔赛跑）：慢指针每步 1 格、快指针每步 2 格，同起点出发；`fast` 走到头说明无环，`slow` 与 `fast` 重合说明有环。
- 一定相遇的原因：慢指针进环后，快指针追上慢指针的距离 `gap` 每步减少 `closing = fastStep - 1 = 1` 格，而环上距离是模环长 `b` 的，必然依次经过 `b-1 … 1, 0`。严格地，`gap₀ = (-a·closing) mod b` 天生被 `gcd(closing, b)` 整除，同余方程必有解。
- 142 的钥匙：相遇时慢指针走了 `a+x`、快指针走了 `2(a+x)`，差值必是环长整数倍，得 `a + x = m·b`，即 `a ≡ b-x (mod b)`；于是把 `ptr1` 放回 head、两指针同速前进，走 `a` 步后同时落在入口（`a = 0` 时入口就是 head，代码天然处理）。
- 易错点：`while fast and fast.next` 的条件不能少（否则 `fast.next.next` 空指针）；「环长为偶数时快 3 慢 1 永不相遇」是把「不同起点」的反例错套到「同起点」Floyd 上的流传错误，同起点时任何 `fastStep ≥ 2` 都会相遇。
- 之所以必须是 2 和 1：相对速度须为正（`fastStep ≥ 2`）；且 142 的「回 head 同速前进」要求 `closing = 1`，两条取交集只有 2。

## 答案

### LC 141

#### 解法一：哈希表（时间 O(n) / 空间 O(n)）

不要求 O(1) 空间时最直白，代码最不易写错。

```python
def hasCycle(head):
    seen = set()
    while head:
        if head in seen:      # 又见到它了 → 有环
            return True
        seen.add(head)
        head = head.next
    return False
```

#### 解法二：Floyd 快慢指针（时间 O(n) / 空间 O(1)）

满足「O(1) 内存」进阶要求，且只动指针不动节点，不违反「不允许修改链表」。

```python
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:          # 快指针走得到头，就说明没环
        slow = slow.next
        fast = fast.next.next
        if slow is fast:               # 相遇 → 有环
            return True
    return False
```

#### Java 版

```java
public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}
```

### LC 142

#### 解法一：哈希表（时间 O(n) / 空间 O(n)）

第一个重复出现的节点就是环入口，逻辑最短，但空间 O(n)。

```python
def detectCycle(head):
    seen = set()
    while head:
        if head in seen:
            return head       # 第一次撞见的重复节点 = 环入口
        seen.add(head)
        head = head.next
    return None
```

#### 解法二：Floyd 判圈 + 第二阶段（时间 O(n) / 空间 O(1)）

先用快慢指针求相遇点，再把一个指针放回 head、两者同速前进，相遇处即入口。

```python
def detectCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:                 # 第一阶段：找到相遇点
            ptr1, ptr2 = head, slow      # ptr1 回 head，ptr2 留在相遇点
            while ptr1 is not ptr2:      # 第二阶段：同速前进
                ptr1 = ptr1.next
                ptr2 = ptr2.next
            return ptr1                  # 相遇处即入口
    return None
```

#### Java 版

```java
public ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            ListNode ptr1 = head, ptr2 = slow;
            while (ptr1 != ptr2) {
                ptr1 = ptr1.next;
                ptr2 = ptr2.next;
            }
            return ptr1;
        }
    }
    return null;
}
```
