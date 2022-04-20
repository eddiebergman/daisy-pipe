from __future__ import annotations
from typing import ParamSpec, TypeVar, Callable, Generic

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")

class PipeStart:

    def __or__(self, nxt: Callable[P, R]) -> Pipe:
        return Pipe(nxt, prv=self)


class Pipe(Generic[P, R]):
    """Something."""

    def __init__(self, f: Callable[P, R], *, prv: PipeStart | Pipe):
        self.f = f
        self.prv = prv

    def __or__(self, nxt: Callable[P, R]) -> Pipe:
        return Pipe(f=nxt, prv=self)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        if isinstance(self.prv, PipeStart):
            return self.f(*args, **kwargs)
        else:
            res = self.prv(*args, **kwargs)
            return self.f(res)

start = PipeStart()
