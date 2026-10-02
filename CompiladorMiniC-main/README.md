# Mini C — compilador parcial

Proyecto del curso **Lenguajes Formales, Autómatas y Compiladores** (UTP-FISC).
Mini C es un lenguaje educativo mínimo; este repositorio construye, por etapas,
un compilador **parcial** en Python:

```
fuente → Lexer → tokens → Parser → AST → Análisis semántico ⇄ Tabla de símbolos
                  └────────────── Diagnósticos (LEX / SYN / SEM) ──────────────┘
```

No hay generación de código, optimización ni ejecución.

## Estado actual: esqueleto

Están definidos los contratos (tipos, firmas y docstrings), el coordinador y la
interfaz de terminal. Los analizadores levantan `NotImplementedError("TODO: …")`
y se completan en proyectos sucesivos:

| Proyecto | Qué se implementa | Archivos |
|---|---|---|
| 1 | Analizador léxico e impresión de tokens y diagnósticos | `lexer/lexer.py`, `output/*` |
| 2 | Parser descendente recursivo y AST | `parser/parser.py` |
| 3 | Análisis semántico y tabla de símbolos | `semantic/symbol_table.py`, `semantic/semantic_analyzer.py` |

Cada proyecto rellena sus stubs **sin cambiar los contratos** ya definidos.

## Requisitos e instalación

- Python ≥ 3.10, sin dependencias en tiempo de ejecución.
- `pytest` solo para desarrollo.

```bash
python -m pip install -e ".[dev]"     # o: pip install -r requirements.txt
```

## Uso

```bash
python -m minic examples/valid/example01.mc     # o: minic examples/valid/example01.mc
```

| Código de salida | Significado |
|---|---|
| 0 | Sin diagnósticos: imprime un token por línea (`TIPO 'lexema' línea columna`) y `Tokens preparados para el analizador sintáctico.` |
| 1 | Con errores: imprime un diagnóstico por línea (`CÓDIGO severidad línea:columna mensaje`) y `La fuente contiene errores léxicos.` |
| 2 | Falta el argumento o el archivo no se puede leer |
| 3 | La etapa léxica aún no está implementada (estado del esqueleto) |

## Pruebas

```bash
python -m pytest
```

`tests/test_structure.py` verifica el esqueleto. Las carpetas `tests/lexer`,
`tests/parser` y `tests/semantic` reciben las pruebas de cada proyecto.

## Estructura

```
src/minic/
├── main.py, __main__.py   # CLI
├── compiler.py            # compile_source(text, stages=("lexer",))
├── source/                # SourceText, SourcePosition
├── diagnostics/           # Diagnostic, DiagnosticBag, códigos LEX/SYN/SEM
├── lexer/                 # Token, TokenType, reglas léxicas, Lexer
├── parser/                # Parser, ParserResult
├── syntax_tree/           # nodos del AST
├── semantic/              # Symbol, SymbolTable, SemanticAnalyzer
└── output/                # format_token, format_diagnostic
```

## Convenciones

- Código y nombres en inglés; docstrings, mensajes y comentarios en español.
- Registros inmutables (`@dataclass(frozen=True)`) y resultados de etapa como
  `NamedTuple` (`tokens, diagnostics = Lexer(source).scan()`).
- Los errores del programa fuente se registran como `Diagnostic` y el análisis
  continúa; las excepciones son solo para errores de uso.
- Los nodos del AST reciben la posición por nombre:
  `Program(statements, line=1, column=1)`.
- Consulta `CLAUDE.md` para la especificación completa.
