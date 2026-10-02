"""Registro de un error encontrado en el programa fuente."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Diagnostic:
    """Error del programa fuente (SRS §19).

    Atributos:
        code: código del catálogo, por ejemplo ``"LEX001"``.
        severity: severidad; en Mini C siempre es ``"error"``.
        message: mensaje en español para el usuario.
        line: línea donde empieza el problema (desde 1).
        column: columna donde empieza el problema (desde 1).
    """

    code: str
    severity: str
    message: str
    line: int
    column: int
