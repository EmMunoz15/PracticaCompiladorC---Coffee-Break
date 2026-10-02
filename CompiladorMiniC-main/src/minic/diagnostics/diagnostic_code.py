"""Catálogo de códigos de diagnóstico de Mini C y sus mensajes (SRS §19).

Cada código tiene una constante y una función que arma su mensaje. Las
funciones solo producen texto: la etapa que detecta el error crea el
``Diagnostic`` con la línea y la columna que correspondan.
"""

ERROR = "error"
"""Única severidad que usa Mini C."""

# Etapa léxica (proyecto 1).
LEX001 = "LEX001"
"""Carácter no reconocido."""

# Etapa sintáctica (proyecto 2).
SYN001 = "SYN001"
"""Se esperaba ``;``."""
SYN002 = "SYN002"
"""Se esperaba ``)``."""
SYN003 = "SYN003"
"""Se esperaba ``}``."""

# Etapa semántica (proyecto 3).
SEM001 = "SEM001"
"""Variable no declarada."""
SEM002 = "SEM002"
"""Variable redeclarada."""
SEM003 = "SEM003"
"""Variable no inicializada."""
SEM004 = "SEM004"
"""Operación semánticamente inválida."""

ALL_CODES: tuple[str, ...] = (
    LEX001,
    SYN001,
    SYN002,
    SYN003,
    SEM001,
    SEM002,
    SEM003,
    SEM004,
)
"""Los 8 códigos del catálogo, en orden de etapa."""


def unrecognized_character(character: str) -> str:
    """Mensaje de ``LEX001``: ``Carácter no reconocido: '<c>'``."""
    return f"Carácter no reconocido: '{character}'"


def expected_semicolon() -> str:
    """Mensaje de ``SYN001``."""
    return "Se esperaba ';'"


def expected_right_paren() -> str:
    """Mensaje de ``SYN002``."""
    return "Se esperaba ')'"


def expected_right_brace() -> str:
    """Mensaje de ``SYN003``."""
    return "Se esperaba '}'"


def undeclared_variable(name: str) -> str:
    """Mensaje de ``SEM001``."""
    return f"Variable no declarada: '{name}'"


def redeclared_variable(name: str) -> str:
    """Mensaje de ``SEM002``."""
    return f"Variable redeclarada: '{name}'"


def uninitialized_variable(name: str) -> str:
    """Mensaje de ``SEM003``."""
    return f"Variable no inicializada: '{name}'"


def invalid_operation(detail: str) -> str:
    """Mensaje de ``SEM004``; ``detail`` describe la operación rechazada."""
    return f"Operación semánticamente inválida: {detail}"
