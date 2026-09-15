# PyRun: Python Bytecode Virtual Machine

PyRun is a lightweight, stack-based Python bytecode interpreter written in pure Python. It executes compiled Python code objects by simulating the core architecture of CPython's virtual machine—complete with a call stack of frames, an evaluation data stack, a block stack for loops and exception control flow, and a dynamic bytecode instruction dispatcher.

---

## Architecture Overview

PyRun is modeled after the CPython virtual machine architecture:

```
+-------------------------------------------------------------------+
|                          VirtualMachine                           |
|                                                                   |
|   +-----------------------------------------------------------+   |
|   |                  Call Stack (self.frames)                 |   |
|   |                                                           |   |
|   |   +---------------------------------------------------+   |   |
|   |   |                   Frame (Active)                  |   |   |
|   |   |                                                   |   |   |
|   |   |   - code_obj (co_code, co_consts, co_varnames)    |   |   |
|   |   |   - global_names / local_names / builtin_names    |   |   |
|   |   |   - last_instruction (instruction pointer)        |   |   |
|   |   |                                                   |   |   |
|   |   |   +-------------------+   +-------------------+   |   |   |
|   |   |   |    Data Stack     |   |    Block Stack    |   |   |   |
|   |   |   | (value evaluation)|   | (loops & excepts) |   |   |   |
|   |   |   +-------------------+   +-------------------+   |   |   |
|   |   +---------------------------------------------------+   |   |
|   |                                                           |   |
|   +-----------------------------------------------------------+   |
+-------------------------------------------------------------------+
```

### Core Components

1. **`VirtualMachine` (`src/pyrun/vm.py`)**:
   - Manages the execution lifecycle, frame call stack, return values, and top-level error dispatch.
   - Decodes bytecode instructions from the code object's `co_code` bytes.
   - Dispatches instructions dynamically to handler methods (`byte_<OPCODE>`, `binaryOperator`, `inplaceOperator`, `unaryOperator`).

2. **`Frame`**:
   - Represents an execution context (e.g., module top-level or function invocation).
   - Holds reference to the code object, local/global/builtin namespaces, and instruction pointer (`last_instruction`).
   - Maintains its own **Data Stack** (for evaluating operands and expressions) and **Block Stack** (for structured control flow).

3. **`Block` (`namedtuple`)**:
   - Tracks control flow blocks (`loop`, `setup-except`, `finally`, `exception-handler`).
   - Remembers the stack height upon entry so that temporary stack items can be cleanly unwound when exiting via `break`, `return`, or an unhandled exception.

4. **`Function`**:
   - Emulates user-defined Python function objects created by `def`.
   - Uses `inspect.getcallargs` to bind positional and default parameters into a fresh local namespace frame.
   - Enables recursion and nested function calls within the VM.

---

## Supported Bytecode & Features

### 1. Stack & Name Resolution
- `LOAD_CONST`, `POP_TOP`
- `LOAD_NAME`, `STORE_NAME` (module / global scope)
- `LOAD_FAST`, `STORE_FAST` (fast local variable access in functions)
- `LOAD_GLOBAL` (global and builtin namespace lookup)

### 2. Operators
- **Binary Arithmetic**: `+`, `-`, `*`, `/`, `//`, `%`, `**`, `<<`, `>>`
- **Bitwise & Logical Operators**: `&`, `|`, `^`, `~`, `not`
- **In-Place Operators**: `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`, `<<=`, `>>=`, `&=`, `|=`, `^=`
- **Comparisons**: `<`, `<=`, `==`, `!=`, `>`, `>=`, `in`, `not in`, `is`, `is not`

### 3. Control Flow & Loops
- **Branching**: `POP_JUMP_IF_FALSE`, `POP_JUMP_IF_TRUE`, `JUMP_FORWARD`, `JUMP_ABSOLUTE`
- **Iteration**: `SETUP_LOOP`, `GET_ITER`, `FOR_ITER`, `POP_BLOCK`, `BREAK_LOOP`
- Supports `for` loops over ranges, lists, strings, and custom iterables with early exit via `break`.

### 4. Data Structures & Attributes
- **Lists**: `BUILD_LIST`, `BINARY_SUBSCR`, list methods
- **Maps**: `BUILD_MAP`, `STORE_MAP`, dictionary indexing and assignment
- **Attributes**: `LOAD_ATTR`, `STORE_ATTR` (accessing and mutating object attributes and methods)

### 5. Functions & Subroutines
- `MAKE_FUNCTION`, `CALL_FUNCTION`, `RETURN_VALUE`
- Supports parameter binding, default arguments, and returning values back to calling frames.

---

## Project Structure

```
PyRun/
├── pyproject.toml              # Project configuration and metadata
├── README.md                   # Project documentation
├── src/
│   └── pyrun/
│       ├── __init__.py         # Package entry point
│       ├── vm.py               # Core Virtual Machine, Frame, and Function classes
│       ├── run.py              # Runner script to compile and execute files
│       ├── legacy.py           # Educational minimal stack interpreter
│       └── test.py             # Basic manual test script
└── tests/
    ├── run_all_tests.py        # Automated test runner for all test suites
    ├── test_arithmetic.py      # Binary, unary, bitwise, and in-place operators
    ├── test_control_flow.py    # If/elif/else branching and comparison logic
    ├── test_loops.py           # For loops, step ranges, nested loops, break
    ├── test_functions.py       # Function calls, arguments, defaults, and returns
    ├── test_data_structures.py # Lists, dicts, indexing, and method invocations
    └── test_comprehensive.py   # Integration test (sorting, primes, Collatz sequence)
```

---

## Quickstart

### Prerequisites
- Python 3.5.x (the VM bytecode layout directly parses Python 3.5 instruction formats)

### Running Python Scripts inside PyRun

Execute any Python source file through the PyRun virtual machine using `run.py`:

```bash
# Run the included test script
python src/pyrun/run.py src/pyrun/test.py

# Or run any test or external script
python src/pyrun/run.py tests/test_arithmetic.py
```

### Running the Test Suite

A complete suite of tests is available under `tests/`.

You can run all tests sequentially with the test runner:

```bash
python tests/run_all_tests.py
```

Or execute individual test files with PyRun:

```bash
python src/pyrun/run.py tests/test_arithmetic.py
python src/pyrun/run.py tests/test_control_flow.py
python src/pyrun/run.py tests/test_loops.py
python src/pyrun/run.py tests/test_functions.py
python src/pyrun/run.py tests/test_data_structures.py
python src/pyrun/run.py tests/test_comprehensive.py
```

---

## Programmatic Usage

You can embed and use `VirtualMachine` directly in your Python code:

```python
from vm import VirtualMachine

# Source code to interpret
source = """
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print("Factorial of 5 is:", factorial(5))
"""

# Compile into Python bytecode
code = compile(source, "<string>", "exec")

# Instantiate and execute in PyRun
vm = VirtualMachine()
vm.run_code(code)
```

---

## How It Works: Step-by-Step

1. **Compilation**: Standard Python `compile()` turns Python source code into a code object (`types.CodeType`).
2. **Frame Initialization**: `vm.make_frame(code)` creates the root frame with global and builtin scopes.
3. **Instruction Decoding**:
   - `last_instruction` reads the opcode byte from `co_code`.
   - If the opcode is `>= dis.HAVE_ARGUMENT`, the next 2 bytes are parsed as a little-endian integer (`arg[0] + arg[1] * 256`).
   - The argument is resolved according to its table (`co_consts`, `co_names`, `co_varnames`, or relative jump offset).
4. **Dispatch**:
   - Method lookup searches for `byte_<OPNAME>`.
   - Arithmetic operations are routed to `binaryOperator`, `inplaceOperator`, or `unaryOperator`.
5. **Stack Execution**:
   - Operands are pushed/popped from `frame.stack`.
   - Control flow instructions manipulate `frame.last_instruction`.
   - Block statements (`for`, `try`) register entries on `frame.block_stack` for clean unwinding.
