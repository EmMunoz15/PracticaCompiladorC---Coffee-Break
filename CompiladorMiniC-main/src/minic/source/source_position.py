"""Posición dentro del texto fuente (uso interno de los analizadores)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SourcePosition:
    """Punto del texto fuente.

    Atributos:
        index: desplazamiento desde el inicio del texto (desde 0).
        line: número de línea (desde 1).
        column: número de columna (desde 1).
    """

    index: int
    line: int
    column: int
