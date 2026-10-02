"""Resultado de la etapa semántica."""

from typing import NamedTuple

from minic.diagnostics.diagnostic import Diagnostic
from minic.semantic.symbol import Symbol


class SemanticResult(NamedTuple):
    """Salida de ``SemanticAnalyzer.analyze()``; permite ``symbols, diagnostics = resultado``.

    Atributos:
        symbols: contenido final de la tabla de símbolos, en orden de declaración.
        diagnostics: diagnósticos ``SEM001``–``SEM004`` en orden de aparición.
    """

    symbols: list[Symbol]
    diagnostics: list[Diagnostic]
