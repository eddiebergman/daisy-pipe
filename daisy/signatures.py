from typing import Any, Callable, Iterator, Type
from io import StringIO

import inspect
from dataclasses import dataclass
from rich.markup import escape

from daisy.util import Richable, richify

NOCONCRETE = object
EMPTY = inspect._empty


def get_type(obj: Any) -> Any:
    if isinstance(obj, str):
        return escape(obj)
    else:
        val = str(obj)
        if val.startswith("<class"):
            return escape(obj.__qualname__)
        else:
            return escape(val.replace("typing.", ""))


@dataclass
class Param(Richable):
    name: str
    type: type | EMPTY
    default: Any | EMPTY

    active: bool = True
    highlight: bool = False
    concrete: Any = NOCONCRETE

    def __rich__(self) -> str:
        s = self.name

        if self.highlight:
            s = f"[bold red underline]{s}[/]"

        if self.type != EMPTY:
            s += f"[yellow]: [/][blue italic]{get_type(self.type)}[/]"  # type: ignore

        if self.concrete is not NOCONCRETE:
            pcol = "green" if not self.highlight else "cyan bold underline"
            s += f"[yellow] = [/][{pcol}]{self.concrete}[/]"
        elif self.default != EMPTY:
            s += f"[yellow] = [/][green]{self.default}[/]"

        return s


@dataclass
class Return(Richable):

    type: type | str | EMPTY

    active: bool = True

    highlight: bool = False
    concrete: Any = NOCONCRETE

    def empty(self) -> bool:
        return self.type == EMPTY and self.concrete == NOCONCRETE

    def __rich__(self) -> str:
        if self.empty():
            return ""
        pcol = "red bold underline" if self.highlight else "blue"
        if self.concrete != NOCONCRETE:
            obj = self.concrete
        else:
            obj = get_type(self.type)

        return f"[{pcol}]{obj}[/]"


@dataclass
class Parameters(Richable):

    params: list[Param]

    def __str__(self) -> str:
        if not any(self.params):
            return ""
        return ", ".join([str(p) for p in self.params if p.active])

    def __rich__(self, active: bool = False, highlight: bool = False) -> str:
        if not any(self.params):
            return ""

        parts = [
            format(param, "R")
            for param in self.params
            if self.iter(active=active, highlight=highlight)
        ]
        return "[yellow], [/]".join(parts)

    def __iter__(self) -> Iterator[Param]:
        return self.iter()

    def iter(self, active: bool = False, highlight: bool = False) -> Iterator[Param]:
        # active takes priority
        itr = iter(self.params)
        if highlight:
            itr = iter(p for p in itr if p.highlight)
        if active:
            itr = iter(p for p in itr if p.active)
        return itr

    def __getitem__(self, key: int | str) -> Param:
        return self.get(key)

    def __setitem__(self, key: int | str, val: Any) -> None:
        self.set(key, val)

    def get(self, key: int | str) -> Param:
        if isinstance(key, int):
            return self.params[key]
        else:
            return next(p for p in self.params if p.name == key)

    def set(
        self, key: int | str, val: Any, active: bool = True, highlight: bool = True
    ) -> None:
        if isinstance(key, int):
            param = self.params[key]
        else:
            param = next(p for p in self.params if p.name == key)

        param.concrete = val
        param.active = active
        param.highlight = highlight


class Signature(Richable):
    def __init__(self, f: Callable):
        sig = inspect.signature(f)
        self.f = f
        self.params = Parameters(
            [
                Param(
                    name=p.name,
                    type=p.annotation,
                    default=p.default,
                )
                for p in sig.parameters.values()
            ]
        )
        from rich import inspect as i

        self.ret = Return(sig.return_annotation)

    def __str__(self) -> str:
        fname = f"{self.f.__qualname__}"
        arg_str = f"{self.params}" if any(self.params) else ""
        ret_str = f" -> {self.ret}" if not self.ret.empty() else ""
        func_str = f"{fname}({arg_str}){ret_str}"

        mod = getattr(self.f, "__module__", None)
        if mod is not None and mod not in ["__main__", "builtins"]:
            return f"{mod}.{func_str}"
        else:
            return func_str

    def __rich__(self) -> str:
        fname = f"{self.f.__qualname__}"
        if fname.startswith("<lambda>"):
            fname = fname.replace("<lambda>", "λ", 1)

        arg_str = f"{self.params:R}" if any(self.params) else ""
        ret_str = f"[yellow] -> [/]{self.ret:R}" if not self.ret.empty() else ""

        func_str = f"[magenta]{fname}[/][yellow]([/]{arg_str}[yellow])[/]{ret_str}"

        mod = getattr(self.f, "__module__", None)
        if mod is not None and mod not in ["__main__", "builtins"]:
            return f"[white]{mod}[/].{func_str}"
        else:
            return func_str

    def __getitem__(self, key: int | str) -> Param:
        return self.params[key]

    def __setitem__(self, key: int | str, val: Any) -> None:
        self.params[key] = val

    def set_return(
        self,
        x: Any,
        active: bool = True,
        highlight: bool = True,
    ) -> None:
        self.ret.concrete = x
        self.ret.active = active
        self.ret.highlight = highlight


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
    table.add_column("Output", justify="left")
    table.add_column("type", justify="right")
    table.add_column("default", justify="right")
    table.add_column("active", justify="right")
    table.add_column("highlight", justify="right")
    table.add_column("concrete", justify="right")
    for name, t, default, active, highlight, concrete in product(
        ["open"],
        [str, EMPTY],
        [4, EMPTY],
        [True, False],
        [True, False],
        [16, NOCONCRETE],
    ):
        p = Param(name, type, default, active, highlight, concrete)
        c = concrete if concrete != NOCONCRETE else "NA"
        t = t.__name__ if t != EMPTY else "NA"
        d = default if default != EMPTY else "NA"
        table.add_row(p, str(t), str(d), str(active), str(highlight), str(c))

    print(table)

    console.rule()

    table = Table(title="Signature")
    table.add_column("Signature")

    def f():
        ...

    table.add_row(Signature(f))

    def f(x, y):
        ...

    table.add_row(Signature(f))

    def f(x, y) -> None:
        ...

    table.add_row(Signature(f))

    def f(x, y: int) -> int:
        ...

    table.add_row(Signature(f))

    def f(x: str, y: dict[int, tuple[int, int]], z: int) -> tuple[int, float]:
        ...

    sig = Signature(f)
    table.add_row(sig)

    def f(x: str, y: dict[int, tuple[int, int]], z: int) -> dict[int, tuple[str, str]]:
        ...

    sig = Signature(f)
    table.add_row(sig)

    from typing import Mapping
    def f(x: str, y: dict[int, tuple[int, int]], z: int) -> Mapping[int, tuple[str, str]]:
        ...

    sig = Signature(f)
    table.add_row(sig)

    from typing import Sequence
    def f(x: str, y: dict[int, tuple[int, int]], z: int) -> Sequence[int]:
        ...

    sig = Signature(f)
    table.add_row(sig)

    table.add_row(Signature(lambda x: x))
    table.add_row(Signature(lambda x, y=4: x))

    print(table)
    console.rule()

    table.add_row(Signature(lambda x: x))
    table.add_row(Signature(lambda x, y=4: x))

    print(table)
    console.rule()

    console.rule()
    table = Table(title="Signatures with highlights and concrete")
    table.add_column("Signature")

    def f(a: int, b: tuple[int, str] = (2, "hello")) -> str:
        ...

    sig = Signature(f)
    table.add_row(sig)

    sig = Signature(f)
    sig[0] = 5
    table.add_row(sig)

    sig = Signature(f)
    sig["b"] = "world"
    table.add_row(sig)

    sig = Signature(f)
    sig.set_return("world")
    table.add_row(sig)

    sig = Signature(f)
    sig.ret.type = EMPTY
    table.add_row(sig)

    sig = Signature(f)
    sig.ret.type = EMPTY
    sig.set_return("Hi")
    table.add_row(sig)

    print(table)
    console.rule()

    # console.print(Signature(f))
