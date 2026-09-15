# Comprehensive integration test for PyRun VM
# Exercises functions, conditionals, nested loops, in-place updates, and data structures

print("========================================")
print("     PyRun Comprehensive Integration    ")
print("========================================")

# 1. Bubble Sort Implementation
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
    return arr

unsorted_list = [64, 34, 25, 12, 22, 11, 90]
sorted_list = bubble_sort(unsorted_list)
print("Sorted Array:", sorted_list)

# 2. Prime Number Sieve / Search
def find_primes(limit):
    primes = []
    for candidate in range(2, limit + 1):
        is_prime = True
        for divisor in range(2, candidate):
            if candidate % divisor == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
    return primes

primes_up_to_30 = find_primes(30)
print("Primes up to 30:", primes_up_to_30)

# 3. Collatz Sequence Length
def collatz_steps(n):
    steps = 0
    curr = n
    while True:
        if curr == 1:
            break
        if curr % 2 == 0:
            curr //= 2
        else:
            curr = curr * 3 + 1
        steps += 1
    return steps

start_num = 27
print("Collatz steps for 27:", collatz_steps(start_num))

# 4. In-Place Bitwise Accumulation
accumulator = 0
for bit_pos in range(8):
    accumulator |= (1 << bit_pos)

print("8-bit bitmask (all 1s):", accumulator)

print("========================================")
print("  All Comprehensive Tests Completed!    ")
print("========================================")
