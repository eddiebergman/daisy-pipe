```python
def square(x: int) -> int:
    return x ** 2
    
pipe = daisy.pipe | square | square
assert pipe(3) == 27
```
