"""Diagnósticos del programa fuente (LEX / SYN / SEM)."""

from minic.diagnostics import diagnostic_code
from minic.diagnostics.diagnostic import Diagnostic
from minic.diagnostics.diagnostic_bag import DiagnosticBag

__all__ = ["Diagnostic", "DiagnosticBag", "diagnostic_code"]
