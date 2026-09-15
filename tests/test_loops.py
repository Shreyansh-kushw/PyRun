# Test loops, iteration, and block stack handling in PyRun

print("=== Running Loop Tests ===")

# Basic for loop with range
total = 0
for i in range(1, 11):
    total += i

print("Sum 1..10:", total)

# For loop with step
even_sum = 0
for i in range(0, 10, 2):
    even_sum += i

print("Sum of evens < 10:", even_sum)

# Looping over a list
items = [10, 20, 30, 40]
product = 1
for x in items:
    product *= x

print("Product of list items:", product)

# Looping over a string
char_count = 0
for ch in "PyRun":
    char_count += 1

print("String length via loop:", char_count)

# Break inside a loop
found = -1
for i in range(100):
    if i == 42:
        found = i
        break

print("Break found value:", found)

# Nested loops
pairs = []
matrix_sum = 0
for i in range(3):
    for j in range(3):
        matrix_sum += i * j

print("Matrix product sum:", matrix_sum)

# Nested loop with inner break
inner_break_count = 0
for i in range(5):
    for j in range(5):
        if j == 2:
            break
        inner_break_count += 1

print("Inner break count:", inner_break_count)

print("=== Loop Tests Passed ===")
