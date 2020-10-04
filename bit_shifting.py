"""
Bit Shifting: shifting bits left and right

A >> 1 shift/move A right 1 bit
0b1110 >> 1 = 0b111

A << 3 shift/move A left 3 bits
"""

print(bin(0b1110 >> 1)) # Shift to the right by 1 --> 0b111

print(bin(0b1110 >> 3))  # Shift to the right by 3 --> 0b1

# how do you efficiently divide by 8? - it's always faster than +-
print(int(0b1110)) # --> 14
print(int(0b1110 >> 1)) # division by 2 --> 7
print(int(0b1110 >> 2))  # division by 4 --> 3
print(int(0b1110 >> 3))  # division by 8 --> 1

print(int(0b1110))  # 14
print(int(0b1110 << 1))  # multiply by 2 --> 28
print(int(0b1110 << 2))  # multiply by 4 --> 56
print(int(0b1110 << 3))  # multiply by 8 --> 112
