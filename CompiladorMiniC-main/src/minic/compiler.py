"""Coordinador: encadena las etapas del compilador que se pidan."""

from __future__ import annotations

from collections.abc import Sequence
from typing import NamedTuple

from minic.diagnostics.diagnostic import Diagnostic
from minic.lexer.lexer import Lexer
from minic.lexer.token import Token
from minic.parser.parser import Parser
from minic.semantic.semantic_analyzer import SemanticAnalyzer
from minic.semantic.symbol import Symbol
from minic.syntax_tree.program import Program

PIPELINE: tuple[str, ...] = ("lexer", "parser", "semantic")
"""Etapas en el orden en que se ejecutan."""


class CompilationResult(NamedTuple):
    """Lo producido por las etapas ejecutadas.

    Atributos:
        tokens: salida del lexer, o ``None`` si no se ejecutó.
        program: AST del parser, o ``None`` si no se ejecutó.
        symbols: tabla final de la semántica, o ``None`` si no se ejecutó.
        diagnostics: diagnósticos de todas las etapas ejecutadas, en orden.
    """

    tokens: list[Token] | None
    program: Program | None
    symbols: list[Symbol] | None
    diagnostics: list[Diagnostic]


def compile_source(text: str, stages: Sequence[str] = ("lexer",)) -> CompilationResult:
    """Ejecuta sobre ``text`` las etapas indicadas en ``stages``.

    ``stages`` debe ser un prefijo de ``PIPELINE``: cada etapa necesita la
    salida de la anterior. Si una etapa reporta diagnósticos, las siguientes
    no se ejecutan.

    Levanta:
        ValueError: si ``stages`` no es un prefijo no vacío de ``PIPELINE``.
        NotImplementedError: si alguna etapa pedida aún no está implementada.
    """
    requested = tuple(stages)
    if not requested or requested != PIPELINE[: len(requested)]:
        raise ValueError(f"Etapas inválidas: {requested!r}; deben ser un prefijo de {PIPELINE!r}")

    tokens, diagnostics = Lexer(text).scan()
    if diagnostics or "parser" not in requested:
        return CompilationResult(tokens, None, None, list(diagnostics))

    program, parse_diagnostics = Parser(tokens).parse()
    if parse_diagnostics or "semantic" not in requested:
        return CompilationResult(tokens, program, None, list(parse_diagnostics))

    symbols, semantic_diagnostics = SemanticAnalyzer(program).analyze()
    return CompilationResult(tokens, program, symbols, list(semantic_diagnostics))
