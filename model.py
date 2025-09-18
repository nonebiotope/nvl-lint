from abc import ABC, abstractmethod
from typing import NamedTuple


class LintResult(NamedTuple):
    "Lint result"

    line: int
    column: int
    message: str
    rule: str


class Linter(ABC):
    "Linter base class"

    name: str
    description: str

    @abstractmethod
    def run(self, body: str) -> list[LintResult]:
        pass
