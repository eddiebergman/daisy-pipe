from __future__ import annotations

from typing import Callable, TypeVar

from daisy.callables import DaisyCallable
from daisy.link import DaisyLink
from daisy.tuples import DaisyTuple
from daisy.util import slice_to_str, Richable
from rich.panel import Panel
from functools import reduce

SelfT = TypeVar("SelfT", bound="DaisyChain")


class DaisyChain(Richable):
    def __init__(
        self,
        name: str | None = None,
        chain: list[Daisy] | DaisyLink | None = None,
    ):
        self.name = name
        if isinstance(chain, DaisyLink):
            chain = [chain]

        self.chain: list[Daisy] = chain if chain is not None else []

    def __or__(self: SelfT, nxt: Callable | tuple) -> SelfT:
        daisy: Daisy
        if callable(nxt):
            daisy = DaisyCallable(nxt)
        elif isinstance(nxt, tuple):
            daisy = DaisyTuple(nxt)
        else:
            raise NotImplementedError(nxt)

        self.chain.append(daisy)
        return self

    def __len__(self) -> int:
        """Get the length of this chain

        Returns
        -------
        int
            The length of this daisy chain
        """
        return len(self.chain)

    def __getitem__(self, idx: int | slice) -> DaisyChain:
        name = f"{self.name}{slice_to_str(idx)}" if self.name is not None else None
        return DaisyChain(name=name, chain=self.chain[idx])

    def __str__(self) -> str:
        parts = [str(daisy) for daisy in self.chain]
        if self.name is not None:
            return f"{self.name} || " + " | ".join(parts)
        else:
            return " | ".join(parts)

    def __rich__(self) -> Panel:
        parts = [f"{daisy:R}" for daisy in self.chain]
        sep = "[white] | [/]"
        return Panel(
            sep.join(parts),
            title=f"[yellow bold]{self.name}[/]",
            title_align="left",
            expand=False
        )

    def named(self, name: str) -> DaisyChain:
        return DaisyChain(name=name, chain=self.chain)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        # Compute the chain
        res = self.chain[0](*args, **kwargs)
        for link in self.chain[1:]:
            res = link(res)
        return res

    def show(self, *args, **kwargs) -> Panel:
        sig, res = self.chain[0].show(*args, **kwargs)

        sigs = [sig]
        for link in self.chain[1:]:
            sig, res = link.show(res)
            sigs.append(sig)

        start = f"[red bold underline]{str(*args, **kwargs)}[/]"
        parts = [start] + [f"{sig:R}" for sig in sigs]
        sep = "[white] | [/]"

        title = (
            f"[yellow bold]{self.name}[/]"
            f"([cyan bold underline]{str(*args, **kwargs)}[/])"
            f"[yellow] = [/][cyan bold underline]{res}[/]"
        )
        return Panel(
            sep.join(parts),
            title=title,
            title_align="left",
            expand=False,
        )




daisy = DaisyChain(name="Daisy")
