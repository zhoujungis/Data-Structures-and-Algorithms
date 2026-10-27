# 【LC 56】合并区间：排序把重叠压成只比当前

**来源**: https://zhoujungis.github.io/article/lc-56-merge-intervals/
**标签**: 算法、贪心、LeetCode、面试

## 题目

以数组 `intervals` 表示若干个区间的集合，其中单个区间为 `intervals[i] = [starti, endi]`。请你合并所有重叠的区间，并返回一个与输入区间数量最少的区间数组，且这些区间不重叠。

示例：`[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`。

## 思路

- **暴力为什么慢**：`n` 个区间有 `n(n-1)/2` 对要判重叠（`a1 <= b2 && b1 <= a2`），而且合并结果会改变后续的比较对象 —— 又难写又 `O(n²)`。
- **排序带来的结构性免费**：按**左端点**排序后，扫到 `[s, e]` 时 `s` 是已见过的最大左端点。若 `s > curEnd`，则它与更早的任何区间都不可能重叠（更早那些区间的 end 全都 `<= curEnd`，否则早该被并进去了）。于是"和前面所有区间比一遍"塌缩成"只和当前合并区间比一次"。
- **两种动作**：`s <= curEnd` → 延伸 `curEnd = max(curEnd, e)`；`s > curEnd` → 收段（当前合并区间进结果，`[s, e]` 开新的一段）。
- **易错点 1：延伸必须取 max**。`[2,3]` 落在 `[1,6]` 里时直接覆盖会把区间**缩**回去，后面 `[5,7]` 就被错拆两段。
- **易错点 2：端点相触也算重叠**，判据是 `s <= curEnd`。写成 `<` 会把 `[1,4],[4,5]` 错拆成两段，而官方样例里没有端点相触的区间、测不出来 —— 要用 `[1,4],[4,5]` 自测。
- **收段为什么可以定格 + 复杂度**：排序保证后面的 start 只会更大，所以收掉的段边界不再受任何未来输入影响；扫描严格 `O(n)`，总成本 `O(n log n)` 全在排序。结果里的区间要新造数组（Java 里 `new int[]{s, e}`），别把输入区间的引用塞进结果。

## 答案

### 解法一：排序 + 线性扫描（时间 O(n log n) / 空间 O(log n)）

适用场景：本题正解，也是 435 / 452 / 57 / 986 一整族区间题的模板。原文该解法给出的完整实现为 Java 版，以下逐字复制。

```java
class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> result = new ArrayList<>();
        int curStart = intervals[0][0], curEnd = intervals[0][1];
        for (int i = 1; i < intervals.length; i++) {
            int s = intervals[i][0], e = intervals[i][1];
            if (s <= curEnd) {                       // 端点相触也算重叠
                curEnd = Math.max(curEnd, e);        // 延伸取 max
            } else {
                result.add(new int[]{curStart, curEnd});  // 新造数组
                curStart = s;
                curEnd = e;
            }
        }
        result.add(new int[]{curStart, curEnd});
        return result.toArray(new int[0][]);
    }
}
```
