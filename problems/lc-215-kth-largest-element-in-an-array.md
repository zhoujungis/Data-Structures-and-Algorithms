# 【LC 215】数组中的第 K 个最大元素：快速选择只在回答「我排第几」

**来源**: https://zhoujungis.github.io/article/lc-215-kth-largest-element/
**标签**: 算法、TopK、LeetCode、面试

## 题目

给定整数数组 `nums` 和整数 `k`，请返回数组中第 `k` 个最大的元素。要求设计时间复杂度为 O(n) 的算法。

```
输入：nums = [3,2,1,5,6,4], k = 2
输出：5

输入：nums = [3,2,3,1,2,4,5,5,6], k = 4
输出：4
```

- 「第 k 大」是**排序后第 k 个位置上的元素，不是第 k 个不同的值**：第二个例子的降序排列是 `[6,5,5,4,3,3,2,2,1]`，第 4 个位置上是 `4`；两个 `5` 各占各的位置。若理解成「第 4 个不同的值」会错答 `3`。
- 等价表述：**升序排序后下标为 `n - k` 的那个数**（`n = nums.length`，0 基下标）。
- `k` 合法（`1 <= k <= n`），元素可重复。

## 思路

- 语义先钉死：**「第 k 大」= 升序下标 `n-k`**，写成 `k-1` 是最常见错误（那找的是第 k 小）；对称样例（如 `[1,2,3,2,1]`）恰好掩盖这个 bug，用 `k = n` 应得最小值的特例自检。
- 核心洞察：**分区之后枢轴落在它最终排序位置上，而位置就是排名**。于是「找第 k 大」变成判断题——枢轴位等于目标位就结束，小于就只进右边，大于就只进左边。
- **快排递归两边、快速选择只进一边**，扫描量是 `n + n/2 + n/4 + … = 2n`，这就是平均 O(n) 的全部来源；若两边都递归就写成快排了。
- 淘汰是确定性的：左侧元素排名全都 `<= pivotIdx < target`，不可能出现在目标位上。
- 最坏退化成 O(n²) 的两种真实输入：**有序数组 + 固定取末尾当枢轴**、**全部元素相同 + Lomuto 分区**。修复：随机化枢轴；重复多时用三路分区（荷兰国旗）。
- 堆解法要**容量固定为 k 的小根堆**：堆顶守在「第 k 大」这道门槛上，新元素想进前 k 先打赢门槛；只 push 不 pop 会退化成 O(n log n)。
- 选型看两件事常被忽略：**快速选择不能流式（要全量随机访问）、会原地修改数组**；堆稳定 O(n log k)、空间 O(k)、不改原数组。

## 答案

### 解法一：快速选择（Lomuto 分区 + 迭代收缩）（时间 平均 O(n)，最坏 O(n²) / 空间 O(1)）

适用：一次性拿到全量数据、允许修改数组时最快；生产代码应把枢轴随机化（见 Java 版）。

```python
import random

def findKthLargest(nums, k):
    target = len(nums) - k          # 第 k 大 = 升序下标 n-k
    left, right = 0, len(nums) - 1
    while True:
        pivot = nums[right]         # 生产代码应该随机化，见第五节
        i = left
        for j in range(left, right):
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[right] = nums[right], nums[i]
        if i == target:
            return nums[i]
        elif i < target:
            left = i + 1            # 答案在右边
        else:
            right = i - 1           # 答案在左边
```

### 解法二：容量为 k 的小根堆（时间 O(n log k) / 空间 O(k)）

适用：数据流式到达、k 远小于 n、内存受限、不允许改动原数组；最坏情况不会退化。

```python
import heapq

def findKthLargest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
```

### 解法三：排序后取下标（时间 O(n log n) / 空间 O(1) 原地）

适用：数据量小、追求一次写对；不满足题目的 O(n) 进阶要求。

```python
def findKthLargest(nums, k):
    nums.sort()
    return nums[len(nums) - k]
```

### Java 版

```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        int target = nums.length - k;          // 第 k 大 = 升序下标 n-k
        int left = 0, right = nums.length - 1;
        while (true) {
            int idx = partition(nums, left, right);
            if (idx == target) return nums[idx];
            else if (idx < target) left = idx + 1;
            else right = idx - 1;
        }
    }

    private int partition(int[] a, int left, int right) {
        int r = left + (int) (Math.random() * (right - left + 1));  // 随机化
        swap(a, r, right);
        int pivot = a[right], i = left;
        for (int j = left; j < right; j++) {
            if (a[j] <= pivot) {
                swap(a, i, j);
                i++;
            }
        }
        swap(a, i, right);
        return i;
    }

    private void swap(int[] a, int i, int j) {
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }
}
```

```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        for (int x : nums) {
            heap.offer(x);
            if (heap.size() > k) heap.poll();
        }
        return heap.peek();
    }
}
```
