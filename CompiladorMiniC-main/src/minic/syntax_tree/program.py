"""Raíz del AST."""

from __future__ import annotations

from dataclasses import dataclass

from minic.syntax_tree.node import Node
from minic.syntax_tree.statements import Statement


@dataclass(frozen=True)
class Program(Node):
    """Programa completo: ``instruccion* EOF`` (SRS §14 y §16).

    Atributos:
        statements: instrucciones de nivel superior, en orden.
    """

    statements: tuple[Statement, ...]
