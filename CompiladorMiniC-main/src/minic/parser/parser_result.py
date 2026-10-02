"""Resultado de la etapa sintáctica."""

from typing import NamedTuple

from minic.diagnostics.diagnostic import Diagnostic
from minic.syntax_tree.program import Program


class ParserResult(NamedTuple):
    """Salida de ``Parser.parse()``; permite ``program, diagnostics = resultado``.

    Atributos:
        program: raíz del AST construido. Con errores de sintaxis contiene lo
            que se pudo reconocer tras la recuperación.
        diagnostics: diagnósticos ``SYN001``–``SYN003`` en orden de aparición.
    """

    program: Program
    diagnostics: list[Diagnostic]
