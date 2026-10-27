# 【LC 347】前 K 个高频元素：频率是天然的桶下标

**来源**: https://zhoujungis.github.io/article/lc-347-top-k-frequent-elements/
**标签**: 算法、TopK、哈希表、LeetCode、面试

## 题目

给定一个整数数组 `nums` 和一个整数 `k`，请返回其中出现频率前 `k` 高的元素，要求时间复杂度**优于** `O(n log n)`。

```
输入: nums = [1,1,1,2,2,3], k = 2
输出: [1,2]
```

说明与约束：

- 返回的是 `k` 个**不同的值**，每个值只出现一次（这点与 LC 215「第 k 大是位置」正好相反）；
- 题目保证答案唯一，不会出现频率并列卡在边界上的歧义；
- 时间必须优于 `O(n log n)`（计数后直接对 distinct 列表排序最坏仍是 `O(n log n)`，卡线不过）。

## 思路

- **两步框架**：先哈希计数一遍 `O(n)`（这一步没有任何技巧），剩下的问题是"按频率挑出前 k 个值" —— 又是一个 TopK。
- **结构性免费**：一个值的出现频率最少是 1、最多是 n，即**频率天生落在 `[1, n]` 这个小整数区间**。要排序的键恰好是范围已知的小整数，这正是计数排序的前提，于是"按频率排序"免费。
- **桶排序做法**：建 `n+1` 个桶（下标 0..n，下标 0 永远空），频率是多少就丢进下标多少的桶，入桶 `O(1)` 不比较；收集时从桶 `n` 往桶 `1` 扫，收满 k 个立刻停。三步全线性，总计 `O(n)`，比题目红线还低一档。代价是 `O(n)` 桶空间。
- **堆做法是通用解**：对 `(频率, 值)` 维护容量 k 的小根堆，堆顶是候选里频率最小的，新元素先打赢门槛才能进前 k，`O(n log k)`；不依赖键的值域、流式友好、空间只有 `O(k)`，k 很大时退化为 `O(n log n)`。
- **易错点**：比较器方向 —— 要"频率最小的在堆顶"就是 `a[1] - b[1]` 升序，写成降序会弹掉频率最高的；桶数组大小按频率上限 n 建 `n+1` 格，少建一格越界；频率并列的多个值同桶，收集顺序由入桶顺序决定（本题保证唯一，LC 692 这类要并列按字典序的需桶内再排）。
- **海量数据变体**：distinct 元素表本身可能装不进内存，需"哈希分桶（同一元素必落同一文件）→ 每桶局部计数 + 局部 TopK → 归并"。分水岭是"单机内存里必须装下什么"：装得下 k 个候选就用堆，连去重表都装不下才分桶分治。

## 答案

### 解法一：计数 + 桶排序（时间 O(n) / 空间 O(n)）

适用场景：本题正解，前提是"键是小整数、范围已知"（频率必在 `[1, n]`）；只取前 k 个，收集可提前停。

```python
from collections import Counter

def topKFrequent(nums, k):
    freq = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for v, f in freq.items():
        buckets[f].append(v)         # 频率即下标，O(1) 入桶
    ans = []
    for f in range(len(nums), 0, -1):
        for v in buckets[f]:
            ans.append(v)
            if len(ans) == k:
                return ans
    return ans
```

### 解法二：计数 + 小根堆（时间 O(n log k) / 空间 O(k)）

适用场景：键没有"小整数范围"保证（如按距离挑前 k）、数据流式到达、或内存吃紧时；k 远小于 distinct 数时更稳。

```python
import heapq

def topKFrequent(nums, k):
    freq = {}
    for x in nums:
        freq[x] = freq.get(x, 0) + 1
    heap = []
    for v, f in freq.items():
        heapq.heappush(heap, (f, v))     # 按频率比的小根堆
        if len(heap) > k:
            heapq.heappop(heap)
    return [v for f, v in heap]
```

### Java 版

```java
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int x : nums) freq.merge(x, 1, Integer::sum);

        List<List<Integer>> buckets = new ArrayList<>();
        for (int i = 0; i <= nums.length; i++) buckets.add(new ArrayList<>());
        for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
            buckets.get(e.getValue()).add(e.getKey());   // 频率即下标
        }

        int[] ans = new int[k];
        int idx = 0;
        for (int f = nums.length; f >= 1 && idx < k; f--) {
            for (int v : buckets.get(f)) {
                ans[idx++] = v;
                if (idx == k) break;
            }
        }
        return ans;
    }
}
```

原文附带的堆版片段（`PriorityQueue` 默认小根堆，比较器按频率）：

```java
PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> a[1] - b[1]);
for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
    heap.offer(new int[]{e.getKey(), e.getValue()});
    if (heap.size() > k) heap.poll();
}
```
