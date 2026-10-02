"""Formato de un diagnóstico para la terminal. Se implementa en el proyecto 1."""

from minic.diagnostics.diagnostic import Diagnostic


def format_diagnostic(diagnostic: Diagnostic) -> str:
    """Devuelve ``CÓDIGO severidad línea:columna mensaje``.

    Ejemplo: ``LEX001 error 1:3 Carácter no reconocido: '!'``.
    Referencia: CLAUDE.md §5.
    """
    return f"{diagnostic.code} {diagnostic.severity} {diagnostic.line}:{diagnostic.column} {diagnostic.message}"
