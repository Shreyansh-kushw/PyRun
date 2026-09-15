# Test control flow and conditional branching in PyRun

print("=== Running Control Flow Tests ===")

# Comparison operators
print("10 < 20:", 10 < 20)
print("10 <= 10:", 10 <= 10)
print("15 == 15:", 15 == 15)
print("20 != 10:", 20 != 10)
print("30 > 25:", 30 > 25)
print("40 >= 40:", 40 >= 40)

# Membership and identity
numbers = [1, 2, 3, 4, 5]
print("3 in numbers:", 3 in numbers)
print("10 not in numbers:", 10 not in numbers)

none_val = None
print("none_val is None:", none_val is None)
print("none_val is not None:", none_val is not None)

# If - Else branches
score = 85
grade = "F"

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "D"

print("Calculated grade:", grade)

# Nested conditionals
val = 42
status = "unknown"

if val > 0:
    if val % 2 == 0:
        status = "positive even"
    else:
        status = "positive odd"
else:
    status = "non-positive"

print("Status of 42:", status)

# Short-circuiting style logical checks
flag1 = True
flag2 = False

if flag1 and not flag2:
    print("Logical AND/NOT branch executed correctly")

if flag2 or flag1:
    print("Logical OR branch executed correctly")

print("=== Control Flow Tests Passed ===")
