"""Unidad léxica producida por el lexer."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    """Token de Mini C (capítulo IV, §4.4).

    Atributos:
        type: categoría, una de las constantes de ``TokenType``.
        lexeme: texto exacto de la fuente; vacío en ``EOF``.
        literal: valor entero en ``INTEGER_LITERAL``; ``None`` en los demás.
        line: línea donde empieza el lexema (desde 1).
        column: columna donde empieza el lexema (desde 1).
    """

    type: str
    lexeme: str
    literal: int | None
    line: int
    column: int
