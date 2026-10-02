"""Colección ordenada de diagnósticos que acumula cada etapa."""

from __future__ import annotations

from collections.abc import Iterable, Iterator

from minic.diagnostics import diagnostic_code
from minic.diagnostics.diagnostic import Diagnostic


class DiagnosticBag:
    """Acumula diagnósticos en el orden en que se reportan.

    Cada analizador crea su propia bolsa. Registrar un error no detiene el
    análisis (principio «diagnósticos, no excepciones»).
    """

    def __init__(self) -> None:
        self._items: list[Diagnostic] = []

    def add(self, diagnostic: Diagnostic) -> None:
        """Agrega un diagnóstico ya construido."""
        self._items.append(diagnostic)

    def report(self, code: str, message: str, line: int, column: int) -> Diagnostic:
        """Crea un diagnóstico con severidad ``"error"``, lo agrega y lo devuelve."""
        diagnostic = Diagnostic(code, diagnostic_code.ERROR, message, line, column)
        self.add(diagnostic)
        return diagnostic

    def extend(self, diagnostics: Iterable[Diagnostic]) -> None:
        """Agrega varios diagnósticos conservando su orden."""
        self._items.extend(diagnostics)

    def has_errors(self) -> bool:
        """Indica si hay al menos un diagnóstico de severidad ``"error"``."""
        return any(item.severity == diagnostic_code.ERROR for item in self._items)

    def to_list(self) -> list[Diagnostic]:
        """Devuelve una copia de los diagnósticos en orden de registro."""
        return list(self._items)

    def __iter__(self) -> Iterator[Diagnostic]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)
