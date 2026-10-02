"""Mini C: compilador parcial educativo (lexer, parser y análisis semántico).

Curso Lenguajes Formales, Autómatas y Compiladores (UTP-FISC).
"""

from minic.compiler import CompilationResult, compile_source

__version__ = "0.1.0"

__all__ = ["CompilationResult", "compile_source", "__version__"]
