# Test arithmetic and in-place operators in PyRun

print("=== Running Arithmetic and Operator Tests ===")

# Basic arithmetic
a = 10
b = 3

print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)
print("True division:", a / b > 3.3)
print("Floor division:", a // b)
print("Modulo:", a % b)
print("Power:", b ** 3)

# Unary operators
pos = +a
neg = -a
bitwise_not = ~a
boolean_not = not (a == 10)

print("Positive:", pos)
print("Negative:", neg)
print("Bitwise invert:", bitwise_not)
print("Boolean not:", boolean_not)

# Bitwise binary operators
x = 12  # 1100
y = 5   # 0101
print("Bitwise AND:", x & y)
print("Bitwise OR:", x | y)
print("Bitwise XOR:", x ^ y)
print("Left shift:", x << 2)
print("Right shift:", x >> 1)

# In-place operators
val = 100
val += 25
print("Inplace add:", val)

val -= 15
print("Inplace sub:", val)

val *= 2
print("Inplace mul:", val)

val //= 5
print("Inplace floor div:", val)

val %= 7
print("Inplace mod:", val)

val **= 2
print("Inplace pow:", val)

bits = 1
bits <<= 4
print("Inplace left shift:", bits)

bits >>= 2
print("Inplace right shift:", bits)

bits |= 1
print("Inplace OR:", bits)

bits &= 3
print("Inplace AND:", bits)

bits ^= 2
print("Inplace XOR:", bits)

print("=== Arithmetic Tests Passed ===")
