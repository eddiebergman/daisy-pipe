from __future__ import annotations

from typing import Callable, ParamSpec, TypeVar

from daisy.link import DaisyLink
from daisy.util import Richable
from daisy.signatures import Signature, Param, Parameters

P = ParamSpec("P")
R = TypeVar("R")


class DaisyCallable(DaisyLink):
    """A pipe object which only consists of a plain callable"""

    def __init__(self, f: Callable[P, R]):
        self.f = f

    @property
    def signature(self) -> Signature:
        signature = Signature(f=self.f)
        return signature

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.f(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.signature}"

    def __rich__(self) -> str:
        return f"{self.signature:R}"

    def show(self, *args: P.args, **kwargs: P.kwargs) -> tuple[Signature, R]:
        ret = self.__call__(*args, **kwargs)
        sig = self.signature

        for i, x in enumerate(args):
            sig[i] = x

        for k, v in kwargs.items():
            sig[k] = v

        sig.set_return(ret)
        return (sig, ret)


if __name__ == "__main__":
    from itertools import product

    from rich import print
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text

    console = Console()
    console.rule()

    table = Table(title="Param")

    def f(x: str, y: int = 2) -> tuple[int, float]:
        return (len(x) + y, 14.2)

    table.add_column("f")
    table.add_column("show")

    daisy = DaisyCallable(f)
    sig, _ = daisy.show("hello")

    table.add_row(Signature(f), sig)

    print(table)
