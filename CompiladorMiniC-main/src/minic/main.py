"""Interfaz de terminal: ``python -m minic <archivo.mc>`` o ``minic <archivo.mc>``."""

from __future__ import annotations

import sys
from collections.abc import Sequence

from minic.compiler import compile_source
from minic.output.diagnostic_printer import format_diagnostic
from minic.output.token_printer import format_token
from minic.source.source_text import SourceText

EXIT_OK = 0
"""La fuente no tiene diagnósticos."""
EXIT_SOURCE_ERRORS = 1
"""La fuente tiene errores."""
EXIT_USAGE = 2
"""Falta el argumento o el archivo no se puede leer."""
EXIT_NOT_IMPLEMENTED = 3
"""La etapa pedida todavía no está implementada."""

USAGE = "Uso: python -m minic <archivo.mc>"


def main(argv: Sequence[str] | None = None) -> int:
    """Analiza léxicamente el archivo indicado e imprime el resultado.

    Recibe los argumentos sin el nombre del programa (por omisión,
    ``sys.argv[1:]``) y devuelve el código de salida.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print(USAGE, file=sys.stderr)
        return EXIT_USAGE

    try:
        source = SourceText.from_file(args[0])
    except (OSError, UnicodeDecodeError) as error:
        print(f"No se pudo leer '{args[0]}': {error}", file=sys.stderr)
        return EXIT_USAGE

    try:
        result = compile_source(source.text, stages=("lexer",))
    except NotImplementedError:
        print("Etapa léxica no implementada todavía", file=sys.stderr)
        return EXIT_NOT_IMPLEMENTED

    if result.diagnostics:
        for diagnostic in result.diagnostics:
            print(format_diagnostic(diagnostic))
        print("La fuente contiene errores léxicos.")
        return EXIT_SOURCE_ERRORS

    for token in result.tokens or []:
        print(format_token(token))
    print("Tokens preparados para el analizador sintáctico.")
    return EXIT_OK
