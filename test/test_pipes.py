from daisy import daisy

from rich import print
from rich.console import Console
from rich.markdown import Markdown
from math import pow

console = Console()

console.line()
console.line()
console.rule("Defining a pipe")
console.line()

def sq(x: int) -> int:
    return x**2

def div(x: int, y: int = 2) -> float:
    return x / y

pipe = daisy | sq | div

console.print(Markdown(
"""
```python
from daisy import daisy
from rich import print

def sq(x: int) -> int:
    return x**2

def div(x: int, divisor: int = 2) -> int:
    return x / divisor

# Start a chain with `daisy`
pipe = daisy | sq | div

print(pipe)
```
""", code_theme="one-dark"
))
print(pipe)

console.line()
console.rule("Add to a pipe!")
console.line()

console.print(Markdown(
"""
```python
# Each pipe operation will return the same daisy chain
pipe = pipe | (lambda x: x + 4) | sq

# You could also just do without assignment
# pipe | (lambda x: x + 4) | sq

# Give it a custom name
pipe.name = "ChillPepper"

print(pipe)
```
""", code_theme="one-dark"
))
pipe = pipe | (lambda x: x + 4) | sq
pipe.name = "ChilliPepper"
print(pipe)


console.line()
console.rule("Showing a computation through the daisy chain")
console.line()

console.print(Markdown(
"""
```python
# Can use it just as a function
result = pipe(2)

# But to see the chain, use `show`
panel = pipe.show(2)

print(panel)
```
""", code_theme="one-dark"
))

panel = pipe.show(2)
print(panel)


console.line()
console.rule("Slicing a pipe")
console.line()

console.print(Markdown(
"""
```python
# Just use `show`
segment = pipe[1:3]

print(segment)
print(segment.show(2))
```
""", code_theme="one-dark"
))

segment = pipe[1:3]

print(segment)
print(segment.show(2))
