"""Tabla de símbolos de Mini C.

Se implementa en el **proyecto 3** (SRS §17–18). Como ``Symbol`` es inmutable,
marcar una variable como inicializada reemplaza su entrada por una copia.
"""

from minic.semantic.symbol import Symbol


class SymbolTable:
    """Registra las variables declaradas y su estado de inicialización."""

    def __init__(self) -> None:
        self._symbols: dict[str, Symbol] = {}

    def declare(self, name: str, declared_line: int, initialized: bool) -> Symbol | None:
        """Declara ``name`` con tipo ``"INT"`` y el siguiente ``id`` disponible.

        Devuelve el ``Symbol`` creado, o ``None`` si ``name`` ya estaba
        declarado en el mismo ámbito (el analizador reporta ``SEM002``).
        """
        raise NotImplementedError("TODO: proyecto 3 — implementar SymbolTable.declare")

    def lookup(self, name: str) -> Symbol | None:
        """Busca ``name``; devuelve su ``Symbol`` o ``None`` si no fue declarado."""
        raise NotImplementedError("TODO: proyecto 3 — implementar SymbolTable.lookup")

    def mark_initialized(self, name: str) -> Symbol:
        """Reemplaza la entrada de ``name`` por una copia con ``initialized=True``.

        Precondición: ``name`` fue declarado. Devuelve el símbolo actualizado.
        """
        raise NotImplementedError("TODO: proyecto 3 — implementar SymbolTable.mark_initialized")

    def symbols(self) -> list[Symbol]:
        """Devuelve los símbolos en orden de declaración (por ``id``)."""
        raise NotImplementedError("TODO: proyecto 3 — implementar SymbolTable.symbols")
