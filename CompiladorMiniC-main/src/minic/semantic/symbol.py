"""Entrada de la tabla de símbolos."""

from dataclasses import dataclass

INT = "INT"
"""Único tipo de dato de Mini C."""


@dataclass(frozen=True)
class Symbol:
    """Variable declarada (SRS §17).

    Atributos:
        id: identificador numérico en orden de declaración (desde 1).
        name: nombre de la variable.
        type: tipo de dato; siempre ``"INT"``.
        initialized: ``True`` si ya recibió un valor.
        declared_line: línea de la declaración.
    """

    id: int
    name: str
    type: str
    initialized: bool
    declared_line: int
