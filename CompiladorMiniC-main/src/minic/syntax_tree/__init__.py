"""Árbol de sintaxis abstracta de Mini C (SRS §16). Lo construye el parser del proyecto 2.

Se llama ``syntax_tree`` y no ``ast`` para no tapar el módulo estándar ``ast``.
"""

from minic.syntax_tree.expressions import (
    BinaryExpression,
    ComparisonExpression,
    Expression,
    IdentifierExpression,
    IntegerLiteral,
)
from minic.syntax_tree.node import Node
from minic.syntax_tree.program import Program
from minic.syntax_tree.statements import (
    Assignment,
    Statement,
    VariableDeclaration,
    WhileStatement,
)

__all__ = [
    "Assignment",
    "BinaryExpression",
    "ComparisonExpression",
    "Expression",
    "IdentifierExpression",
    "IntegerLiteral",
    "Node",
    "Program",
    "Statement",
    "VariableDeclaration",
    "WhileStatement",
]
