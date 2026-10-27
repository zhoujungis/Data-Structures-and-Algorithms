# 【扑克】5 张牌判断顺子：王只补缺失，补不了重复

**来源**: https://zhoujungis.github.io/article/lc-61-poker-straight/
**标签**: 算法、LeetCode、面试
**难度**: 简单

## 题目

给定 5 张牌，牌面数字 1~13（A=1，J=11，Q=12，K=13），判断是不是顺子（连续 5 张）。追问：如果牌里有大小王（记作 0，可当任意牌），怎么判断？

```
输入: [1, 2, 3, 4, 5]
输出: true

输入: [0, 0, 1, 2, 5]     两张王补上 3、4，凑出 1-2-3-4-5
输出: true
```

说明与约束：

- 恰好 5 张牌，牌面取 1~13；`0` 表示大小王（任意牌）；
- 顺子是 **5 个互不相同的数**连续：王能填「缺失的数」，填不了「重复的数」；
- 无王时判据收紧为：5 个数互不相同且 `max - min = 4`；
- 全王（`[0,0,0,0,0]`）也是顺子。

## 思路

- **把「连续 5 张」塌缩成「相邻差」**：排序后相邻差全为 1 即连续；有断档的地方差就大于 1，而每张王正是一次「任意填」的机会 —— 缺几个数就消耗几张王。
- **判据一：无重复**。`[1,2,2,3,4]` 里两个 2，再来十张王也变不成顺子：王能填缺失的数，填不了已有的数。重复检查必须放在补洞之前，这两个失败原因互相救不了。
- **判据二：跨度够小**。非王牌互不相同时，「王够用」⇔ `max - min < 5`（等价于洞数 ≤ 王数）。无王时它自动收紧成 `max - min = 4`，一条判据同时覆盖有王、无王两个版本。
- **`=` 与 `<` 的边界**：无王时跨度必须**恰好** 4。写成 `<= 5` 就会把 `[1,2,3,4,6]`（缺一个 5、手里没王）放过去。
- **王不该参与统计**：求跨度、查重复、算差值时都要先跳过 0。把王算进 `max - min`（或把 `min` 初始化成 0）会让跨度虚大，把真顺子错杀 —— `[0,0,1,2,5]` 会被算成 `5 - 0 = 5`。
- **易错点：遍历从下标 1 开始**。`0` 与 `0` 这一对也会被算成相邻对，贡献负 gap（`0-0-1 = -1`），把真正的洞抵掉：`[0,0,1,2,6]` 账面合计 2「刚好够」，实际要补 3、4、5 三个洞。必须只对**非王牌**逐对检查。

## 答案

### 解法一：排序 + 数王 + 逐对补洞（时间 O(1) / 空间 O(1)）

适用场景：本题标准解 —— 能同时报出洞数与剩余王数，边界情况最容易讲清楚。

```python
def is_straight(cards: list[int]) -> bool:
    if len(cards) != 5:
        raise ValueError("必须恰好 5 张牌")
    s = sorted(cards)          # 王（0）小于所有牌面，自动排到最前
    jokers = s.count(0)        # 每张王 = 一次「任意填」的机会
    rest = s[jokers:]          # 非王牌，升序
    for i in range(1, len(rest)):
        if rest[i] == rest[i - 1]:
            return False       # 重复：王填不了已有的数
        if rest[i] - rest[i - 1] > 1:
            jokers -= rest[i] - rest[i - 1] - 1   # 中间的洞拿王补
            if jokers < 0:
                return False   # 王用完了还不够
    return True
```

### 解法二：等价判据「非王无重复 + 跨度 < 5」（时间 O(1) / 空间 O(1)）

适用场景：一行判据同时覆盖有无王两个版本，写起来最短；但说不出「为什么 < 5」时别用。

```python
def is_straight(cards: list[int]) -> bool:
    s = sorted(cards)
    rest = [c for c in s if c != 0]
    if len(set(rest)) != len(rest):
        return False
    return True if not rest else max(rest) - min(rest) < 5
```

### Java 版

```java
public class PokerStraight {
    // cards 长度必须为 5，0 表示大小王
    public static boolean isStraight(int[] cards) {
        if (cards == null || cards.length != 5) {
            throw new IllegalArgumentException("必须恰好 5 张牌");
        }
        Arrays.sort(cards);
        int jokers = 0;
        while (jokers < 5 && cards[jokers] == 0) {
            jokers++;
        }
        for (int i = jokers + 1; i < 5; i++) {
            if (cards[i] == cards[i - 1]) {
                return false;                       // 重复，王救不了
            }
            jokers -= cards[i] - cards[i - 1] - 1;  // 补洞
            if (jokers < 0) {
                return false;                       // 王不够
            }
        }
        return true;
    }
}
```
