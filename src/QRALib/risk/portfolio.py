# src/QRALib/risk/portfolio.py

from typing import List, Iterator, Union
from .model import Risk

class RiskPortfolio:
    """A sequence-like container of Risk objects with lookup & search."""

    def __init__(self, risks: List[Risk]) -> None:
        self._risks = list(risks)

    def __len__(self) -> int:
        return len(self._risks)

    def __getitem__(self, idx: Union[int, str]) -> Risk:
        if isinstance(idx, int):
            return self._risks[idx]
        for r in self._risks:
            if r.uniq_id == idx:
                return r
        raise KeyError(f"No risk with ID {idx!r}")

    def __iter__(self) -> Iterator[Risk]:
        return iter(self._risks)

    def ids(self) -> List[str]:
        """Return all risk IDs."""
        return [r.uniq_id for r in self._risks]

    def search(self, term: str) -> List[Risk]:
        """Case-insensitive search in ID or name."""
        term = term.lower()
        return [
            r for r in self._risks
            if term in r.uniq_id.lower() or term in r.name.lower()
        ]

    def to_dicts(self) -> List[dict]:
        """Serialize all risks to dict form."""
        return [r.to_dict() for r in self._risks]

    def lookup(self, key: Union[int, str]) -> dict:
        """Fetch a single risk as a dict, by index or ID."""
        return self[key].to_dict()
