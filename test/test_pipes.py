import daisy

def square(x: int) -> int:
    return x**2

def divides(x: int) -> int:
    return x / 2

pipe = daisy.start | square | (lambda x: x + 1) | divides

xs = [pipe(i) for i in range(4)]
print(xs)

pipe = (
    pipe
    | square
    | divides
    | (lambda x: x + 4)
)

x = pipe(34)
print(x)
