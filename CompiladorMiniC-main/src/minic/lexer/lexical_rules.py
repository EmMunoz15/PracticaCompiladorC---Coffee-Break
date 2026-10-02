"""Tablas y clases de caracteres del léxico de Mini C (capítulo IV, §4.4).

Las tablas son de solo lectura (``MappingProxyType`` y ``frozenset``) para no
tener estado global mutable.
"""

from types import MappingProxyType
from typing import Mapping

from minic.lexer.token_type import TokenType

KEYWORDS: Mapping[str, str] = MappingProxyType(
    {
        "int": TokenType.KW_INT,
        "while": TokenType.KW_WHILE,
    }
)
"""Palabras reservadas. Se consultan después de consumir el nombre completo."""

DOUBLE: Mapping[str, str] = MappingProxyType(
    {
        "==": TokenType.EQUAL_EQUAL,
        "!=": TokenType.NOT_EQUAL,
    }
)
"""Operadores de dos caracteres. Se consultan antes que ``SINGLE`` (máxima coincidencia)."""

SINGLE: Mapping[str, str] = MappingProxyType(
    {
        "=": TokenType.ASSIGN,
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        "{": TokenType.LBRACE,
        "}": TokenType.RBRACE,
        ";": TokenType.SEMICOLON,
    }
)
"""Símbolos de un carácter."""

WHITESPACE: frozenset[str] = frozenset({" ", "\t", "\r", "\n"})
"""Caracteres que se consumen sin producir token. Solo ``\\n`` abre línea nueva."""

NEWLINE = "\n"


def is_identifier_start(character: str) -> bool:
    """Indica si ``character`` puede iniciar un identificador: ``[A-Za-z_]`` (ASCII)."""
    return character == "_" or ("a" <= character <= "z") or ("A" <= character <= "Z")


def is_digit(character: str) -> bool:
    """Indica si ``character`` es un dígito decimal ASCII: ``[0-9]``."""
    return "0" <= character <= "9"


def is_identifier_part(character: str) -> bool:
    """Indica si ``character`` puede continuar un identificador: ``[A-Za-z0-9_]``."""
    return is_identifier_start(character) or is_digit(character)
