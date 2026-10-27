# 【LC 207】课程表：Kahn 的入度表，和 DFS 的三色标记（附 210 返序）

**来源**: https://zhoujungis.github.io/article/lc-207-course-schedule/
**标签**: 算法、图、拓扑排序、LeetCode、面试

## 题目

你一共需要修 `numCourses` 门课，课程编号为 `0` 到 `numCourses - 1`。先修关系由 `prerequisites` 给出，`prerequisites[i] = [a, b]` 表示**修课程 `a` 之前必须先修课程 `b`**。

判断是否可能修完所有课程：能修完返回 `true`，否则返回 `false`。

```
输入: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
输出: true

输入: numCourses = 2, prerequisites = [[1,0],[0,1]]
输出: false        —— 1 等 0、0 等 1，互相等待
```

- 方向：`[a, b]` 是「修 a 前先修 b」，所以边是 **b → a**（先修课指向后修课）。
- 允许自环（`[[0,0]]`，课程等自己）、重边（`[[1,0],[1,0]]`），图也可能是多个连通块。
- 附带变体 **LC 210 课程表 II**：同一张图，若能修完返回**任意一种**合法的修课顺序，修不完返回空数组（例如上面的例子返回 `[0,1,2,3]` 或 `[0,2,1,3]`，而 `[0,3,1,2]` 不合法）。

## 思路

- 整道题只有一句翻译：**修课顺序 = 有向图的拓扑序；能修完 ⇔ 这张图没有环**。有环 ⇒ 环上的课互相等 ⇒ 无解。
- **Kahn**：入度 = 还有几门先修没修完。反复把入度为 0 的课出队「修掉」，修完把它指向的后继入度减 1，减到 0 才入队；出队顺序天然就是拓扑序。
- **Kahn 的判据是「出队数量 == numCourses」，不是「队列空了」**——所有课修完队列也会空，只剩环（或其树枝）时队列也会提前枯竭。
- **DFS 必须用三色（白/灰/黑），不能只用一个 `visited` 布尔值**：探到**灰**色邻居才是环（回边指向递归栈里的祖先）；探到**黑**色邻居是安全汇合，应跳过，否则误报。
- DFS 的**后序必须反转才是拓扑序**：节点在所有后继处理完之后才 append，先修课自然排在后面，反转后翻到前面。
- **方向画反是本题第一大坑**：把 `[a, b]` 建成 a → b 会让拓扑序整个反过来。
- 拓扑序**不唯一**：默认例子中 Kahn 给 `[0,1,2,3]`、DFS 给 `[0,2,1,3]`，两者都合法；要判唯一性是 LC 444 的追问。

## 答案

### 解法一：Kahn 入度表 + 队列（时间 O(V+E) / 空间 O(V+E)）

适用：直观、天然产出拓扑序（切 LC 210 只需返回 `order`）。`V = numCourses`，`E = prerequisites.length`。

```python
from collections import deque

def canFinish(numCourses, prerequisites):
    adj = [[] for _ in range(numCourses)]
    indegree = [0] * numCourses
    for a, b in prerequisites:
        adj[b].append(a)          # 先修 b → 后修 a
        indegree[a] += 1
    q = deque(v for v in range(numCourses) if indegree[v] == 0)
    order = []
    while q:
        cur = q.popleft()
        order.append(cur)         # 出队顺序就是拓扑序
        for nxt in adj[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:    # 入度减到 0 才能修
                q.append(nxt)
    return len(order) == numCourses   # 207 的答案；210 直接返回 order（不足则 []）
```

### 解法二：DFS 三色标记（时间 O(V+E) / 空间 O(V+E)）

适用：判环顺手，后序反转即得拓扑序；链形图递归深度最坏 O(V)。

```python
def canFinish_dfs(numCourses, prerequisites):
    adj = [[] for _ in range(numCourses)]
    for a, b in prerequisites:
        adj[b].append(a)
    color = [0] * numCourses        # 0 白 / 1 灰 / 2 黑
    order = []                      # 后序

    def dfs(v):
        color[v] = 1                # 白 → 灰
        for nxt in adj[v]:
            if color[nxt] == 1:     # 灰色回边 = 环
                return False
            if color[nxt] == 0 and not dfs(nxt):
                return False
        color[v] = 2                # 灰 → 黑
        order.append(v)             # 后序：把它追加在「所有后继之后」
        return True

    for v in range(numCourses):
        if color[v] == 0 and not dfs(v):
            return False
    return True                     # 210 的答案 = order[::-1]
```

### Java 版

```java
class Solution {
    // Kahn：入度表 + 队列
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        int[] indegree = new int[numCourses];
        for (int[] p : prerequisites) {
            adj.get(p[1]).add(p[0]);      // 先修 p[1] → 后修 p[0]
            indegree[p[0]]++;
        }
        Deque<Integer> queue = new ArrayDeque<>();
        for (int v = 0; v < numCourses; v++) {
            if (indegree[v] == 0) queue.offer(v);
        }
        int done = 0;
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            done++;
            for (int nxt : adj.get(cur)) {
                if (--indegree[nxt] == 0) queue.offer(nxt);
            }
        }
        return done == numCourses;
    }
}
```

```java
class Solution {
    // DFS 三色：0 白 / 1 灰 / 2 黑
    private List<List<Integer>> adj;
    private int[] color;

    public boolean canFinish(int numCourses, int[][] prerequisites) {
        adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        for (int[] p : prerequisites) adj.get(p[1]).add(p[0]);
        color = new int[numCourses];
        for (int v = 0; v < numCourses; v++) {
            if (color[v] == 0 && !dfs(v)) return false;
        }
        return true;
    }

    private boolean dfs(int v) {
        color[v] = 1;
        for (int nxt : adj.get(v)) {
            if (color[nxt] == 1) return false;          // 灰色回边 = 环
            if (color[nxt] == 0 && !dfs(nxt)) return false;
        }
        color[v] = 2;
        return true;
    }
}
```
