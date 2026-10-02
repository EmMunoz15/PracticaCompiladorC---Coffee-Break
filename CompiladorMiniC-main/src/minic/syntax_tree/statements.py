"""Nodos de instrucción del AST (SRS §16)."""

from __future__ import annotations

from dataclasses import dataclass

from minic.syntax_tree.expressions import Expression
from minic.syntax_tree.node import Node


@dataclass(frozen=True)
class Statement(Node):
    """Categoría de las instrucciones. No agrega campos; solo agrupa."""


@dataclass(frozen=True)
class VariableDeclaration(Statement):
    """``int x;`` o ``int x = expresion;``.

    Atributos:
        name: nombre declarado.
        initializer: expresión inicial, o ``None`` si no hay ``=``.
    """

    name: str
    initializer: Expression | None


@dataclass(frozen=True)
class Assignment(Statement):
    """``x = expresion;``.

    Atributos:
        name: variable que recibe el valor.
        value: expresión asignada.
    """

    name: str
    value: Expression


@dataclass(frozen=True)
class WhileStatement(Statement):
    """``while (condicion) { instruccion* }``.

    Atributos:
        condition: condición entre paréntesis. La gramática exige una
            comparación y la semántica lo vuelve a verificar (SEM004).
        body: instrucciones del bloque, en orden.
    """

    condition: Expression
    body: tuple[Statement, ...]
