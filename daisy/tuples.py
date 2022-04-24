from typing import Any

from daisy.link import DaisyLink


class DaisyTuple(DaisyLink):
    def __init__(self, tup: tuple):
        self.tup = tup

    def value(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError()
