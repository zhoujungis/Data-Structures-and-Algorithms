from error import StackUnderflow
from linkedlist import LNode

class SStack:
     def __init__(self):
         self._stack = []
         
     def is_empty(self):
         return len(self._stack) == 0
     
     def push(self, e):
         self._stack.append(e)
         
     def pop(self):
         if self.is_empty():
             raise StackUnderflow("in pop.")
         return self._stack.pop()
     
     def top(self):
         if self.is_empty():
             raise StackUnderflow("in top.")
         return self._stack[-1]

class LStack:
     def __init__(self):
          self._top = None
          
     def is_empty(self):
          return self._top is None

     def push(self, e):
          self._top = LNode(e, self._top)

     def pop(self):
          if self.is_empty():
               raise StackUnderflow("in pop.")
          p = self._top
          self._top = p.next
          return p.elem

     def top(self):
          if self.is_empty():
               raise StackUnderflow("in top.")
          return self._top.elem


# 栈的应用
# 1.括号匹配  代码中空间为O(n),若为单符号，可以简化为O(1)空间
def check_parens(text):
     parens = "(){}[]"
     open_parens = "({["
     opposite = {")":"(", "}":"{", "]":"["}

     def parentheses(text):
          i, text_len = 0, len(text)
          while True:
               while i < text_len and text[i] not in parens:
                    i += 1
               if i >= text_len:
                    return
               yield text[i], i
               i += 1
     
     st = SStack()
     for pr, i in parentheses(text):
          if pr in open_parens:
               st.push(pr)
          elif st.pop() != opposite[pr]:
               print("Unmatching is found at", i, "for", pr)
               return False
     print("All parentheses are correctly matched.")
     return True


# 2.数学表达式
# 利用后缀表达式和栈实现数学运算
class ESStack(SStack):
     def depth(self):
          return len(self._elems)

def suffix_exp_evaluator(line):
     return suf_exp_evaluator(line.split())

def suf_exp_evaluator(exp):
     operators = "+-*/"
     st = ESStack()

     for x in exp:
          if x not in operators:
               st.push(float(x))
               continue

          if st.depth() < 2:
               raise SyntaxError("Short of operand(s).")
          a = st.pop()
          b = st.pop()

          if x == "+":
               c = b + a
          elif x == "-":
               c = b - a
          elif x == "*":
               c = b * a
          elif x == "/":
               c = b / a
          else:
               break

          st.push(c)

     if st.depth() == 1:
          return st.pop()
     raise SyntaxError("Extra operand(s).")

def suffix_exp_calculator():
     while True:
          try:
               lien = input("Math Calculator(entry 'end' to quit)\nSuffix Expression: ")
               if line == "end": return
               res = suffix_exp_evaluator(line)
               print(res)
          except Exception as ex:
               print("Error:", type(ex), ex.args)

# 中缀表达式到后缀表达式的转换
priority = {"(":1, "+":3, "-":3, "*":5, "/":5}
infix_operators = "+-*/()"

def trans_infix_suffix(line):
     st = SStack()
     exp = []

     for x in tokens(line):
          if x not in infix_operators:
               exp.append(x)
          elif st.is_empty() or x == "(":
               st.push(x)
          elif x == ")":
               while not st.is_empty() and st.top != "(":
                    exp.append(st.pop())
               if st.is_empty():
                    raise SyntaxError("Missing '('.")
               st.pop()
          else:
               while (not st.is_empty() and priority[st.top()] >= priority[x]):
                    exp.append(st.pop())
               st.push(x)
     while not st.is_empty():
          if st.top() == "(":
               raise SyntaxError("Missing ')'.")
          exp.append(st.pop())

     return exp

def tokens(line):
     i, llen = 0, len(line)
     while i < llen:
          while line[i].isspace():
               i += 1
          if i >= llen:
               break
          if line[i] in infix_operators:
               yield line[i]
               i += 1
               continue
          j = i + 1
          while (j < llen and not line[j].isspace() and line[j] not in infix_operators):
               if (line[j] == 'e' or line[j] == 'E') and j+1 < llen and line[j+1] == '-':
                    j += 1
               j += 1
          yield line[i:j]
          i = j

# 测试
def test_trans_infix_suffix(s):
     print(s)
     print(trans_infix_suffix(s))
     print("Value:", suf_exp_evaluator(trans_infix_suffix(s)))
