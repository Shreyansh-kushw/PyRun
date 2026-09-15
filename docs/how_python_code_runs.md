# How Python Code Runs

When we think of Python, we often refer to the Python interpreter rather than referring to the language itself, or we use these terms interchangeably.

However, that is not entirely accurate:
- **Python (the language)** is a specification—a set of rules and syntax for writing instructions in a high-level language for the computer.
- **The Interpreter** is the software used to understand and execute those instructions.

---

## The Execution Pipeline

An interpreter is not the only step in the execution of Python code. There are three main steps before the interpreter runs:

1. **Lexing (Tokenizing)**  
   The step where raw text (the Python source code) is broken down into a sequence of meaningful chunks called **tokens**.

2. **Parsing**  
   A parser takes the linear token stream produced by the lexer and determines if it conforms to the formal grammatical rules of the programming language. This is what verifies whether the syntax is valid and constructs an Abstract Syntax Tree (AST).

3. **Compiling**  
   This step transforms the programmer's source code from abstract syntax trees into structured **code objects** containing instructions (bytecode) that the interpreter can understand.

4. **Interpreting**  
   This is where the interpreter executes the instructions. Note that the interpreter does not need to understand raw Python syntax; it only needs to understand the instructions produced by the compiler. Therefore, a Python interpreter can be written in any language—even in Python itself.

```text
+-------------+         +---------+         +------------+         +-------------+
| Source Code | ------> |  Lexer  | ------> |   Parser   | ------> |  Compiler   |
|  (.py file) |         | (Tokens)|         |   (AST)    |         | (Bytecode)  |
+-------------+         +---------+         +------------+         +------+------+
                                                                          |
                                                                          v
                                                                   +-------------+
                                                                   | Interpreter |
                                                                   |  (Stack VM) |
                                                                   +-------------+
```

---

## Language Decoupling & Alternative Interpreters

Because the interpreter does not need to understand the raw syntax of the language, the same interpreter can be used to execute different languages as long as the compiler is compatible. For example, if we build a compiler that translates Lisp syntax into the bytecode instructions expected by the interpreter, the same interpreter can execute Lisp syntax as well.

### Common Python Implementations

- **CPython**: The reference and most common implementation, written in C. This is the default implementation downloaded from the official website.
- **Jython**: Written in Java, running on the Java Virtual Machine (JVM).
- **IronPython**: Written in C#, targeting the .NET CLR.
- **PyPy**: Written in RPython, featuring a Just-In-Time (JIT) compiler for speed.

Each has its own quirks and target environments, though CPython remains the standard.

---

## Why is Python Called an "Interpreted" Language?

Despite Python being called an interpreted language, it still involves a compilation step.

Most interpreted languages, including Python, involve compilation. The reason Python is called "interpreted" is that the compilation step does relatively less work (and the interpreter does relatively more) compared to traditional compiled languages (like C or Rust, which compile ahead-of-time directly to native machine code).

Another way of understanding this: the compiler is not executing the code, but rather translating it into an intermediate instruction set for the interpreter to execute.

---

## How Does a Python Interpreter Work?

The Python interpreter acts like a **virtual machine**, meaning it emulates a physical computer.

Specifically, it is a **stack machine**—it manipulates several stacks (such as the value stack, call stack, and block stack) to perform operations, unlike a **register machine** which writes to and reads from specific memory locations/registers.

### Bytecode and Code Objects

The Python interpreter is a **bytecode interpreter**:
- **Input**: Its input is instruction sets called **bytecode**. When you write Python, the lexer, parser, and compiler generate **code objects** for the interpreter to operate on.
- **Code Objects**: Each code object contains a set of instructions to be executed—that's the bytecode—plus metadata (such as constants, variable names, and line mappings) that the interpreter will need.
- **Bytecode Representation**: Bytecode is an intermediate representation (IR) of Python code: it expresses the source code in a way the virtual machine can understand. It is analogous to the way assembly language serves as an intermediate representation between C code and a piece of hardware.
