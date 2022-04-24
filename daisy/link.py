from __future__ import annotations

from typing import Any
from abc import abstractmethod

from daisy.util import Richable


class DaisyLink(Richable):
    """Something."""

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        ...
