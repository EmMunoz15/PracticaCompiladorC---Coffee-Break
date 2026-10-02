"""Formato de un token para la terminal. Se implementa en el proyecto 1."""

from minic.lexer.token import Token


def format_token(token: Token) -> str:
    """Devuelve ``TIPO 'lexema' línea columna``, separados por un espacio.

    Ejemplo: ``KW_INT 'int' 1 1``. El ``EOF`` se muestra con lexema vacío:
    ``EOF '' 1 42``. Referencia: CLAUDE.md §5.
    """
    return f"{token.type} '{token.lexeme}' {token.line} {token.column}"
