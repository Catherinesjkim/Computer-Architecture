"""
Bitwise Operations - similar to boolean operators (and, or, not in python)

A AND & && B = C

  OR | ||
  
  X-OR ^
  
  NOT ~ !
"""

#   01011010
# & 10101111
# ----------
#   00001010

a = 0b01011010
b = 0b01011010
print(bin(a & b))

#   01011010
# | 10101111
# ----------
#   11111111
print(bin(a | b))

#   01011010
# ^ 10101111
# ----------
#   11110101

# print x-or A B
print(bin(a ^ b) | (b & a))

# given these numbers
a = 0b01011010
b = 0b10101111

# Evaluate (A | B) ^ (A & B)
# 11111111 ^ 00001010
# 11110101
