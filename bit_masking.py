"""
Bit Masking: 

10000010 --> 00000010 = 2
--  ---- instructions
# of operands
masking: shifting + boolean bitwise Operations
"""

instruction = 0b10000010 # LDI
shifted = instruction >> 6 # isolate a certain values = shifting
print(bin(shifted))


instruction = 0b10011010
shifted = instruction >> 3
# filters out al unnecessary values
mask = 0b00000011 & shifted
print(bin(mask))


instruction = 0b10010010
mask = 0b00011000 & instruction # && one of the hash algos (djb2) uses bitwise operations to hash numbers
shifted = mask >> 3
# filters out al unnecessary values
print(bin(shifted))
# print(10 & 2)
