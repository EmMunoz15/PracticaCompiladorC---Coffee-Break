"""Texto fuente de un programa Mini C y su lectura desde disco."""

from __future__ import annotations

from dataclasses import dataclass
from os import PathLike


@dataclass(frozen=True)
class SourceText:
    """Contenido de un programa Mini C.

    Atributos:
        text: el texto completo, tal como está en el archivo.
        path: ruta de origen, o ``None`` si el texto no viene de un archivo.
    """

    text: str
    path: str | None = None

    @classmethod
    def from_file(cls, path: str | PathLike[str]) -> SourceText:
        """Lee un archivo ``.mc`` en UTF-8 sin traducir los saltos de línea.

        Se usa ``newline=""`` para que ``\\r`` llegue intacto al lexer, que lo
        trata como espacio en blanco (capítulo IV, §4.4).

        Levanta:
            OSError: si el archivo no existe o no se puede leer.
            UnicodeDecodeError: si el archivo no está en UTF-8.
        """
        with open(path, encoding="utf-8", newline="") as file:
            return cls(file.read(), str(path))
