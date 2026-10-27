# 【LC 93】复原 IP 地址：分段回溯，剪枝分两层

**来源**: https://zhoujungis.github.io/article/lc-93-restore-ip-addresses/
**标签**: 算法、回溯、LeetCode、面试

## 题目

有效 IP 地址由**四个 0-255 的整数**组成，中间用 `'.'` 分隔，且每个整数**不能有前导零**（`"0"` 合法，`"01"` 非法）。

给定只含数字的字符串 `s`，返回**所有**可能的有效 IP 地址，顺序不限。

```
输入: s = "25525511135"
输出: ["255.255.11.135", "255.255.111.35"]

输入: s = "0000"
输出: ["0.0.0.0"]

输入: s = "010010"
输出: ["0.10.0.10", "0.100.1.0"]    （"01"、"010" 都因前导零非法）
```

约束：

- `s` 仅由数字组成，长度需在 `[4, 12]` 之间（4 段、每段 1-3 位），否则无解；
- 每段取值 `0 ~ 255`，单段 `"0"` 合法，多位的段不能以 `0` 开头；
- 四段必须**恰好**覆盖整串，不能有多余数字被丢弃。

## 思路

- 规模天生有界：把 `s` 切成 4 段 = 在 `n-1` 个缝隙里选 3 个切点，`n ∈ [4, 12]`，切点组合最多 `C(11, 3) = 165`，回溯在这里是组织方式而不是性能手段。
- 剪枝分两层，回答两个不同的问题：**段合法性**（前导零 `seg[0] == '0' and seg_len > 1`、`int(seg) > 255`）与**可行性**（剩余位数必须满足 `segs <= rest <= segs * 3`）。第二层最容易漏，它管的是「段本身合法但整条路走不通」，例如 `"25525511135"` 第一段切 `"2"` 段合法、剩 10 位却装不进 3 段。
- 第 4 段必须**恰好用完**全部数字：切满 4 段就 `join` 会丢数字，产生 `"255.255.11.13"` 这类假答案。
- 前导零不能一刀切：`"0"` 合法、`"0x"` 非法，所以判断条件是 `seg[0] == '0' and seg_len > 1`，否则 `"0000"` 会空手而归。
- `path + [seg]` 每层传新列表，天然免手动回溯；Java/C++ 共享引用则必须 `add` / `remove` 配对。
- 入口先判 `4 <= n <= 12`，结构上不可能直接返回空，不必进搜索。

## 答案

### 解法一：分层剪枝回溯（时间 O(C(n-1, 3) × n) = O(1) / 空间 O(4)）

```python
def restoreIpAddresses(s: str) -> list[str]:
    ans = []
    n = len(s)

    def dfs(pos: int, path: list[str]) -> None:
        if len(path) == 4:
            if pos == n:                       # 恰好用完
                ans.append('.'.join(path))
            return
        remain_segs = 4 - len(path)
        for seg_len in (1, 2, 3):
            if pos + seg_len > n:              # 末尾不够切
                continue
            seg = s[pos:pos + seg_len]
            if seg[0] == '0' and seg_len > 1:  # 层一：前导零
                continue
            if int(seg) > 255:                 # 层一：超出范围
                continue
            rest = n - pos - seg_len           # 层二：可行性
            segs = remain_segs - 1
            if segs > 0 and not (segs <= rest <= segs * 3):
                continue
            dfs(pos + seg_len, path + [seg])   # 深入（path + [...] 免手动回溯）

    if 4 <= n <= 12:
        dfs(0, [])
    return ans
```

### 解法二：三重循环枚举切点（时间 O(C(n-1, 3) × n) = O(1) / 空间 O(1)）

同一搜索空间展开成循环，层数与分支固定时与回溯完全等价；段数不定、剪枝依赖路径状态时回溯更清晰。

```python
def restoreIpAddresses(s: str) -> list[str]:
    n, res = len(s), []
    if not (4 <= n <= 12):
        return res
    for i in range(1, 4):
        for j in range(i + 1, i + 4):
            for k in range(j + 1, j + 4):
                if k >= n:
                    continue
                parts = (s[:i], s[i:j], s[j:k], s[k:])
                if all(valid(seg) for seg in parts):
                    res.append('.'.join(parts))
    return res
```

### Java 版

```java
public List<String> restoreIpAddresses(String s) {
    List<String> ans = new ArrayList<>();
    int n = s.length();
    if (n < 4 || n > 12) return ans;

    dfs(s, 0, new ArrayList<>(), ans);
    return ans;
}

private void dfs(String s, int pos, List<String> path, List<String> ans) {
    if (path.size() == 4) {
        if (pos == s.length()) ans.add(String.join(".", path));
        return;
    }
    int remainSegs = 4 - path.size();
    for (int len = 1; len <= 3; len++) {
        if (pos + len > s.length()) continue;
        String seg = s.substring(pos, pos + len);
        if (seg.charAt(0) == '0' && len > 1) continue;       // 前导零
        if (Integer.parseInt(seg) > 255) continue;           // 超出范围
        int rest = s.length() - pos - len;
        int segs = remainSegs - 1;
        if (segs > 0 && (rest < segs || rest > segs * 3)) continue;  // 可行性
        path.add(seg);                                       // 手动回溯版
        dfs(s, pos + len, path, ans);
        path.remove(path.size() - 1);
    }
}
```
