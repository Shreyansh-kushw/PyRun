# Test lists, maps, indexing, and object attributes in PyRun

print("=== Running Data Structure Tests ===")

# List creation and indexing
lst = [10, 20, 30, 40]
print("Element at index 0:", lst[0])
print("Element at index 2:", lst[2])
print("Negative indexing (-1):", lst[-1])

# List mutation via methods
lst.append(50)
print("After append length:", len(lst))
print("Appended element:", lst[4])

# Dictionary creation and access
user = {"name": "Alice", "age": 25, "role": "engineer"}
print("User name:", user["name"])
print("User age:", user["age"])

# Dictionary mutation
user["status"] = "active"
print("User status:", user["status"])

# Modifying dictionary values
user["age"] = 26
print("Updated age:", user["age"])

# Object attributes and methods
word = "pyrun interpreter"
upper_word = word.upper()
print("Upper string attribute call:", upper_word)
print("Starts with pyrun:", word.startswith("pyrun"))

# List inside dictionary
config = {
    "servers": ["srv1", "srv2", "srv3"],
    "retries": 3
}
print("Config servers count:", len(config["servers"]))
print("First server:", config["servers"][0])

print("=== Data Structure Tests Passed ===")
