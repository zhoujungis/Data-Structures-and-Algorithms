# 【LC 165】比较版本号：归一化后逐列比

**来源**: https://zhoujungis.github.io/article/lc-165-compare-version-numbers/
**标签**: 算法、双指针、LeetCode、面试

## 题目

给你两个版本号字符串 `version1` 和 `version2`，比较它们。

版本号由以点（`.`）分隔的修订号组成，修订号从左到右依次比较：

- **忽略前导零**：每个修订号的数字比较时忽略前导零（`"01"` 等于 `"1"`）；
- **缺失视为 0**：如果版本号没有某处的修订号，视为 `0`（`"1.0"` 与 `"1.0.0"` 相等）。

返回规则：`version1 > version2` 返回 1，`version1 < version2` 返回 -1，相等返回 0。

```
输入: version1 = "1.01", version2 = "1.001"
输出: 0   （忽略前导零后都是 1.1）

输入: version1 = "1.0", version2 = "1.0.0"
输出: 0   （缺失的修订号视为 0）

输入: version1 = "1.2", version2 = "1.10"
输出: -1  （2 < 10 —— 字符比较 '2' > '1' 会错成 1）
```

## 思路

- **两条规则指向同一个动作**：剥前导零 + 缺失补零 = 先把每个修订号**归一化**，再做最朴素的逐列比较，某列分出胜负立即短路返回。
- **剥零必须留一位**：守卫写成 `i < len(s) - 1`，否则 `"000"` 会被剥成空串，后续比长度全错。
- **漂亮事实：剥完前导零后比数值 = 先比长度、等长再比字典序** —— 没有前导零的数字串，位数多的一定更大；等长时字典序与数值序完全一致。全程**不需要任何数字转换**。
- **纯字符串法免疫精度陷阱**：修订号长度不受限制，JS 的 `parseInt` / Java 的 `Long.parseLong` 对超长修订号会失真（两个不同的 21 位数会被判相等），字符串法零转换天然正确。
- **缺失侧必须按 `"0"` 参与比较**，不能拿「列数差」当大小：`"1.0"` vs `"1.0.0"` 相等，`"1.0.1"` vs `"1"` 应返回 -1。

## 答案

### 解法一：split + 归一化字符串比较（时间 O(m + n) / 空间 O(m + n)）

原文分三段给出：剥前导零、归一化比较、主流程。

```python
def strip_zeros(s: str) -> str:
    i = 0
    while i < len(s) - 1 and s[i] == '0':   # len(s) - 1 保证至少留一位
        i += 1
    return s[i:]
```

```python
def cmp_norm(a: str, b: str) -> int:
    if len(a) != len(b):
        return -1 if len(a) < len(b) else 1
    if a == b:
        return 0
    return -1 if a < b else 1
```

```python
def compareVersion(version1: str, version2: str) -> int:
    rev1 = version1.split('.')
    rev2 = version2.split('.')
    cols = max(len(rev1), len(rev2))

    for i in range(cols):
        v1 = strip_zeros(rev1[i]) if i < len(rev1) else '0'
        v2 = strip_zeros(rev2[i]) if i < len(rev2) else '0'
        c = cmp_norm(v1, v2)
        if c != 0:
            return c            # 第一列分出胜负，短路返回
    return 0
```

### 解法二：split + 直接转整数（时间 O(m + n) / 空间 O(m + n)）

适用场景：最短写法，适用于 Python（`int()` 任意精度直接安全）；JS `parseInt` / Java `Long` 在超长修订号上会失真，不能用这个版本。

```python
def compareVersion(version1: str, version2: str) -> int:
    rev1 = version1.split('.')
    rev2 = version2.split('.')
    n = max(len(rev1), len(rev2))
    for i in range(n):
        a = int(rev1[i]) if i < len(rev1) else 0
        b = int(rev2[i]) if i < len(rev2) else 0
        if a != b:
            return -1 if a < b else 1
    return 0
```

### Java 版

```java
public int compareVersion(String version1, String version2) {
    String[] rev1 = version1.split("\\.");
    String[] rev2 = version2.split("\\.");
    int cols = Math.max(rev1.length, rev2.length);

    for (int i = 0; i < cols; i++) {
        String v1 = i < rev1.length ? stripZeros(rev1[i]) : "0";
        String v2 = i < rev2.length ? stripZeros(rev2[i]) : "0";
        int c = cmpNorm(v1, v2);
        if (c != 0) return c;
    }
    return 0;
}

private String stripZeros(String s) {
    int i = 0;
    while (i < s.length() - 1 && s.charAt(i) == '0') i++;
    return s.substring(i);
}

private int cmpNorm(String a, String b) {
    if (a.length() != b.length()) return a.length() < b.length() ? -1 : 1;
    int c = a.compareTo(b);
    return c < 0 ? -1 : c > 0 ? 1 : 0;
}
```
