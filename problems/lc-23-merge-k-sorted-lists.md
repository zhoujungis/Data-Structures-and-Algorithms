# 【LC 23】合并 K 个升序链表：堆里到底该放几个节点

**来源**: https://zhoujungis.github.io/article/lc-23-merge-k-sorted-lists/
**标签**: 算法、链表、LeetCode、面试
**难度**: 困难

## 题目

给你一个链表数组，每个链表都已经按升序排列。请你将所有链表合并到一个升序链表中，返回合并后的链表。

```
输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,5,6]
解释：将所有链表合并到一个升序链表中，得到 1→1→2→3→4→5→6

输入：lists = []
输出：[]

输入：lists = [[]]
输出：[]
```

约束：

- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` 按升序排列
- `lists[i].length` 的总和不超过 `10^4`

节点定义沿用 LC 21：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

留意约束里的两个数字：**k 可以到 10⁴，但所有链表的节点总数不超过 10⁴** —— 这已经提示了朴素做法会死在哪。

## 思路

- 这题是 LC 21「合并两个有序链表」的 K 元版，核心子程序不变（dummy + tail、先接再走、剩余整段接上），差别只在**怎么调用它、调用几次**。
- **全局最小一定只在 K 条链表各自当前的头部产生**，所以只需要一台「随时塞入、随时取最小」的机器。**堆里只放 K 个头部**（弹出堆顶后补入它所在链表的下一个节点），这才是复杂度里 `log k` 而不是 `log N` 的来源；把 N 个节点全塞进堆虽然结果正确，却退化成 O(N log N)，白扔了「每段已升序」的条件。
- **顺序两两合并是 O(k²N)**：第 i 轮要把已经接好的 `i·n` 个节点再走一遍，累加出平方。**分治两两配对**把轮数从 k 压到 ⌈log₂k⌉，每轮总工作量 O(N)。
- Python 的 `heapq` 是**小顶堆**（正好要小的），且没有 `key` 参数：元组 `(val, node)` 在值相等时会去比较 `ListNode`，直接 `TypeError`，必须塞一个互不相同的序号 `i` 垫背。Java 的 `PriorityQueue` 也是默认小顶堆，但传了显式 `Comparator`，不需要垫背。
- 同为 O(N log k) 也有取舍：**分治的比较次数更少**（每节点约 log k 次 vs 堆的约 2·log k 次，多出来的是上浮下沉成本），**堆的节点访问次数更少**（每节点只进出堆一次，分治每轮都要搬）——所以堆适合流式 / 外排场景。而 **k 很小（≤8）时顺序合并反而最快**（实测 k=4 时堆最慢），不必为「显得高级」引入堆。
- 易错点：建堆时 `if head` 不能省（空链表取 `.val` 会崩）；弹出后必须把新头补进堆；分治迭代版奇数条时最后一条要**原样带进下一轮**而非丢弃（否则只有 k 为奇数才复现少一截）。

## 答案

### 解法一：最小堆（时间 O(N log k) / 空间 O(k)）

适用：堆里始终只有 K 个头部，天然支持流式 / K 路归并外排的面试主推写法。

```python
import heapq

def mergeKLists(lists):
    dummy = ListNode(0)
    tail = dummy
    heap = []

    # 建堆：K 个头部入堆
    for i, head in enumerate(lists):
        if head:                                    # 空链表直接跳过
            heapq.heappush(heap, (head.val, i, head))

    while heap:
        val, i, node = heapq.heappop(heap)          # 取出全局最小
        tail.next = node                            # 接到结果尾部
        tail = tail.next
        if node.next:                               # 该链表前移一格
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
```

### 解法二：分治（递归，两两配对）（时间 O(N log k) / 空间 O(log k) 递归栈）

适用：比较次数最少的一档；`mergeTwoLists` 即 LC 21 的合并函数。递归深度约 log₂k 层，不会爆栈。

```python
def mergeKLists(lists):
    if not lists:
        return None
    return merge_range(lists, 0, len(lists) - 1)

def merge_range(lists, lo, hi):
    if lo == hi:                              # 只剩一条，直接返回
        return lists[lo]
    mid = (lo + hi) // 2
    left = merge_range(lists, lo, mid)        # 排左半边
    right = merge_range(lists, mid + 1, hi)   # 排右半边
    return mergeTwoLists(left, right)         # 合并两半（LC 21 的代码）
```

### 解法三：分治（迭代，自底向上）（时间 O(N log k) / 空间 O(1)）

适用：不想用递归栈时；`mergeTwoLists` 同上。奇数条轮空的那条原样进下一轮。

```python
def mergeKLists(lists):
    if not lists:
        return None
    level = lists
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            if i + 1 < len(level):
                nxt.append(mergeTwoLists(level[i], level[i + 1]))
            else:
                nxt.append(level[i])          # 轮空，原样进下一轮
        level = nxt
    return level[0]
```

### Java 版

```java
public ListNode mergeKLists(ListNode[] lists) {
    ListNode dummy = new ListNode(0);
    ListNode tail = dummy;
    // PriorityQueue 默认就是小顶堆；这里按节点值排序
    PriorityQueue<ListNode> heap =
        new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));

    for (ListNode head : lists) {
        if (head != null) heap.offer(head);
    }
    while (!heap.isEmpty()) {
        ListNode node = heap.poll();
        tail.next = node;
        tail = tail.next;
        if (node.next != null) heap.offer(node.next);
    }
    return dummy.next;
}
```
