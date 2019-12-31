# 字符串匹配
# 1.朴素的字符串匹配；2.KMP算法

# 朴素的字符串匹配
def naive_amtching(t, p):
     m, n = len(p), len(t)
     i, j = 0, 0
     while i < m and j < n:
          if p[i] == t[j]:
               i, j = i + 1, j + 1
          else:
               i, j = 0, j - i + 1
     if i == m:
          return j - i
     return -1

# KMP算法
def matching_kmp(t, p, pnext):
     i, j = 0, 0
     m, n = len(p), len(t)
     while j < n and i < m:
          if i == -1 or t[j] == p[i]:
               i, j = i+1, j+1
          else:
               i = pnext[i]
     if i == m:
          return j-i
     return -1

def gen_pnext(p):
     i, k, m = 0, -1, len(p)
     pnext = [-1] * m
     while i < m-1:
          if k == -1 or p[i] == p[k]:
               i += 1
               k += 1
               if p[i] == p[k]:
                    # 如果p[i]==p[k],因为p[i]≠t[j],所以可以往后挪更多
                    pnext[i] = pnext[k]
               else:
                    pnext[i] = k
          else:
               # p[i]≠p[k],寻找p[:k]的公共前缀
               k = pnext[k]
     return pnext


# 正则表达式
def match(re, text):
     def match_here(re, i, text, j):
          while True:
               if i == rlen:
                    return True
               if re[i] == "$":
                    return i+1 == rlen and j == tlen
               if i+1 < rlen and re[i+1] == "*":
                    return match_star(re[i], re, i+2, text, j)
               if j == tlen or (re[i] != "." and re[i] != text[j]):
                    return False
               i, j = i+1, j+1

     def match_star(c, re, i, text, j):
          for n in range(j, tlen):
               if match_here(re, i, text, n):
                    return True
               if text[n] != c and c != ".":
                    break
          return False

     rlen, tlen = len(re), len(text)
     if re[0] == "^":
          if match_here(re, 1, text, 0):
               return 1
     for n in range(tlen):
          if match_here(re, 0, text, n):
               return n
     return -1
