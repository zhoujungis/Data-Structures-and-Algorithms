# 【LC 994】腐烂的橘子：多源 BFS，和一张腐烂时刻表

**来源**: https://zhoujungis.github.io/article/lc-994-rotting-oranges/
**标签**: 算法、图、BFS、LeetCode、面试

## 题目

**LC 994 腐烂的橘子**：给你一个 `m × n` 的网格，每个格子是 `0`（空，不是橘子）、`1`（新鲜橘子）或 `2`（腐烂橘子）。**每分钟**，所有腐烂橘子会把它**上下左右四个方向**相邻的新鲜橘子变腐烂。返回直到网格中**没有新鲜橘子**为止所必须经过的**最小分钟数**；如果不可能，返回 `-1`。

```
输入: grid = [
  [2,1,1],
  [1,1,0],
  [0,1,1]
]
输出: 4

输入: grid = [
  [2,1,1],
  [0,1,1],
  [1,0,1]
]
输出: -1     （左下角那个 1 被 0 隔开，永远烂不到）
```

约束与细节：

- 空格（`0`）不传播，腐烂只能发生在新鲜橘子上；
- 扩散是**每分钟一轮、所有腐烂橘子同时发生**（不是排队一个个来）；
- `[[0,2]]` 这种没有新鲜橘子的网格 → 输出 `0`（不需要任何时间）。

## 思路

- 把每个格子看成图上的点，相邻就连边。腐烂从所有 `2` 同时开始，所以每个新鲜橘子变烂的时刻就是**它到最近那个 `2` 的边数**，答案 = 全场最大距离。
- **多源 BFS**：初始就把所有 `2` 一起入队当第 0 层，BFS「第一次访问的层数就是到最近源的距离」这条性质会自动算出结果，不需要对每个源各跑一遍再取 `min`（只入队一个源是本题第一大坑）。
- 分钟数按**层**记：`for _ in range(len(q))` 进入时先固定本层长度，新入队的属于下一分钟，`minute += 1` 写在整层处理完之后。按「弹出格子数」加分钟会让答案膨胀。
- **入队即标记**（`grid[nr][nc] = 2`）防止同一格被多个邻居重复入队、`fresh` 被重复减。
- 维护 `fresh` 计数：`while q and fresh` 提前退出，循环结束后 `fresh > 0` 才返回 `-1`。判据是「BFS 结束后仍有新鲜橘子」，不是「队列空了就 -1」。
- 不能用 DFS：要的是**最短**时间，DFS 给出的是某条路径上的时间。

## 答案

### 解法一：层序循环多源 BFS（时间 O(m·n) / 空间 O(m·n)）

最直观的写法：用 `for _ in range(len(q))` 把「一层 = 一分钟」切出来。

```python
from collections import deque

def orangesRotting(grid):
    m, n = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 2:
                q.append((r, c))      # 所有源一起入队
            elif grid[r][c] == 1:
                fresh += 1
    minute = 0
    while q and fresh:
        for _ in range(len(q)):       # 固定本层 = 第 minute+1 分钟要扩散的格子
            r, c = q.popleft()
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2  # 入队即标记
                    fresh -= 1
                    q.append((nr, nc))
        minute += 1
    return minute if fresh == 0 else -1
```

### 解法二：队列存时间戳（时间 O(m·n) / 空间 O(m·n)）

不切层，把 `(r, c, t)` 一起入队；适合想省掉层结构、或要顺便记录每格时刻的场景。注意 `answer` 必须在**入队**处更新，写在弹出处会在提前退出时漏掉最后一批时间戳、答案差 1。

```python
def orangesRotting_ts(grid):
    m, n = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 2:
                q.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1
    answer = 0
    while q and fresh:
        r, c, t = q.popleft()
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                answer = max(answer, t + 1)   # 关键：入队时就把时间戳记进答案
                q.append((nr, nc, t + 1))
    return answer if fresh == 0 else -1
```

### 解法三：距离场盖表（时间 O(m·n) / 空间 O(m·n)）

显式维护「每格腐烂时刻」的表，答案取表内最大值；适合题目进一步索要距离矩阵、或需要把距离场复用的场景。

```python
def orangesRotting_dist(grid):
    m, n = len(grid), len(grid[0])
    stamp = [[None] * n for _ in range(m)]
    q = deque()
    fresh = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 2:
                stamp[r][c] = 0
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    minute = 0
    while q and fresh:
        minute += 1
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    stamp[nr][nc] = minute   # 盖章：腐烂时刻 = 到最近源的距离
                    fresh -= 1
                    q.append((nr, nc))
    if fresh > 0:
        return -1
    return max((v for row in stamp for v in row if v is not None), default=0)
```

### Java 版

```java
class Solution {
    private static final int[][] DIRS = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

    public int orangesRotting(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int fresh = 0, minute = 0;
        Deque<int[]> queue = new ArrayDeque<>();
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] == 2) queue.offer(new int[]{r, c});   // 所有源入队
                else if (grid[r][c] == 1) fresh++;
            }
        }
        while (!queue.isEmpty() && fresh > 0) {
            for (int size = queue.size(); size > 0; size--) {        // 固定本层
                int[] cur = queue.poll();
                for (int[] d : DIRS) {
                    int nr = cur[0] + d[0], nc = cur[1] + d[1];
                    if (nr < 0 || nr >= m || nc < 0 || nc >= n || grid[nr][nc] != 1) continue;
                    grid[nr][nc] = 2;                                // 入队即标记
                    fresh--;
                    queue.offer(new int[]{nr, nc});
                }
            }
            minute++;
        }
        return fresh == 0 ? minute : -1;
    }
}
```
