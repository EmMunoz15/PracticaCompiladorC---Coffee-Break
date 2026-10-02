"""Resultado de la etapa léxica."""

from typing import NamedTuple

from minic.diagnostics.diagnostic import Diagnostic
from minic.lexer.token import Token


class LexerResult(NamedTuple):
    """Salida de ``Lexer.scan()``; permite ``tokens, diagnostics = resultado``.

    Atributos:
        tokens: tokens en orden, terminados siempre en un único ``EOF``.
        diagnostics: diagnósticos ``LEX001`` en orden de aparición.
    """

    tokens: list[Token]
    diagnostics: list[Diagnostic]
