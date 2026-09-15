# Test user-defined functions and frame management in PyRun

print("=== Running Function Tests ===")

# Simple function
def greet(name):
    return "Hello, " + name

print(greet("PyRun"))

# Multi-argument function
def add_three(a, b, c):
    return a + b + c

print("Sum of 3 args:", add_three(10, 20, 30))

# Function with default arguments
def power(base, exp=2):
    res = 1
    for _ in range(exp):
        res *= base
    return res

print("Default exponent (3^2):", power(3))
print("Explicit exponent (2^5):", power(2, 5))

# Function with local state and accumulator
def calculate_stats(numbers):
    total = 0
    count = 0
    for num in numbers:
        total += num
        count += 1
    return total // count

sample_nums = [10, 20, 30, 40, 50]
print("Average:", calculate_stats(sample_nums))

# Function calling another function
def square(x):
    return x * x

def sum_of_squares(a, b):
    return square(a) + square(b)

print("Sum of squares (3^2 + 4^2):", sum_of_squares(3, 4))

# Function returning multiple values via list
def min_max(elements):
    minimum = elements[0]
    maximum = elements[0]
    for x in elements:
        if x < minimum:
            minimum = x
        if x > maximum:
            maximum = x
    return [minimum, maximum]

res = min_max([45, 12, 89, 3, 67])
print("Min:", res[0], "Max:", res[1])

print("=== Function Tests Passed ===")
