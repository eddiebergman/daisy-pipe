import daisy

def test_basic() -> None:

    def square(x: int) -> int:
        return x**2

    pipe = daisy.start | square | square
    assert pipe(3) == 81
    assert pipe(2) == 16
