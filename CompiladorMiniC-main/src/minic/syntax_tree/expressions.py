"""Nodos de expresión del AST (SRS §16)."""

from __future__ import annotations

from dataclasses import dataclass

from minic.syntax_tree.node import Node


@dataclass(frozen=True)
class Expression(Node):
    """Categoría de las expresiones. No agrega campos; solo agrupa."""


@dataclass(frozen=True)
class IntegerLiteral(Expression):
    """Literal entero, por ejemplo ``10``.

    Atributos:
        value: valor en base 10 (el ``literal`` del token).
    """

    value: int


@dataclass(frozen=True)
class IdentifierExpression(Expression):
    """Lectura de una variable, por ejemplo ``x``.

    Atributos:
        name: nombre de la variable.
    """

    name: str


@dataclass(frozen=True)
class BinaryExpression(Expression):
    """Suma o resta, por ejemplo ``x - 1``. Asocia a la izquierda.

    Atributos:
        left: operando izquierdo.
        operator: lexema del operador, ``"+"`` o ``"-"``.
        right: operando derecho.
    """

    left: Expression
    operator: str
    right: Expression


@dataclass(frozen=True)
class ComparisonExpression(Expression):
    """Comparación, por ejemplo ``x != 0``. Solo aparece como condición del ``while``.

    Atributos:
        left: expresión izquierda.
        operator: lexema del operador, ``"=="`` o ``"!="``.
        right: expresión derecha.
    """

    left: Expression
    operator: str
    right: Expression
