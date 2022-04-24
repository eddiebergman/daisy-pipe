from __future__ import annotations

from typing import Any

from rich.console import Console, ConsoleRenderable, RichCast


def richify(o: Any) -> str:
    console = Console()
    with console.capture() as capture:
        console.print(o)

    return capture.get()


class Richable(RichCast):
    def __rich__(self) -> ConsoleRenderable | RichCast | str:
        return richify(self)

    def __format__(self, s: str) -> str:
        if s == "R":
            richitem = self.__rich__()
            if isinstance(richitem, str):
                return richitem
            else:
                raise ValueError(f"Can't use format flag R on {self}")
        else:
            return super().__format__(s)


def slice_to_str(slc: slice | int) -> str:
    if isinstance(slc, int):
        return f"[{slc}]"

    # Could have tried to build the string but this
    # was just easier to work backward and implement
    s, e, st = slc.start, slc.stop, slc.step

    # Can list them out as a binary table
    mapping = {
        (0, 0, 0): "[:]",
        (0, 0, 1): f"[::{st}]",
        (0, 1, 0): f"[:{e}:]",
        (0, 1, 1): f"[:{e}:{st}]",
        (1, 0, 0): f"[{s}:]",
        (1, 0, 1): f"[{s}::{st}]",
        (1, 1, 0): f"[{s}:{e}]",
        (1, 1, 1): f"[{s}:{e}:{st}]",
    }
    key = (int(s is not None), int(e is not None), int(st is not None))
    return mapping[key]

    # xs[::] == xs[:]
    if (s is None) and (e is None) and (st is None):
        return "[:]"

    # xs[::1]
    if (s is None) and (e is None) and (st is not None):
        pass

    # xs[::1]
    # xs[:1]
    # xs[1:1]
    # xs[1:1:1]
    # xs[1:1:1]

    if s is not None and e is not None:
        pass
