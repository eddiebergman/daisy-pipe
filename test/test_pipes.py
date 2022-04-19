import daisy

def test_basic() -> None:

    def square(x: int) -> int:
        return x**2

    def divides(x: int) -> int:
        return x / 2

    pipe = daisy.start | square | square | divides

    assert pipe(3) == 81
    assert pipe(2) == 16

    pipe |= square | square

