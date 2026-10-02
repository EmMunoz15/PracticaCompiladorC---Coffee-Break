"""Nodo base del AST."""

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Node:
    """Base de todos los nodos del AST (SRS §16).

    ``line`` y ``column`` son de palabra clave obligatoria, así los campos
    propios de cada nodo van primero:
    ``Program(statements, line=1, column=1)``.

    Atributos:
        line: línea del token que inicia la construcción (desde 1).
        column: columna del token que inicia la construcción (desde 1).
    """

    line: int
    column: int
