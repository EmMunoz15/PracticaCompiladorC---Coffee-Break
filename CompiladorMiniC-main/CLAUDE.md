# CLAUDE.md — Proyecto Mini C (esqueleto modular)

Este archivo le da contexto a Claude Code sobre el proyecto. Léelo completo antes de crear o modificar archivos. Si una instrucción mía en el chat contradice este documento, pregúntame antes de actuar.

---

## 1. Qué es el proyecto

Mini C es un lenguaje educativo mínimo del curso **Lenguajes Formales, Autómatas y Compiladores** (UTP-FISC, facilitador Edwin Saucedo). El proyecto final del curso es un **compilador parcial** en Python con estas etapas:

```
fuente → Lexer → tokens → Parser → AST → Análisis semántico ⇄ Tabla de símbolos
                  └────────────── Diagnósticos (LEX / SYN / SEM) ──────────────┘
```

No hay generación de código, optimización ni ejecución.

**Tu tarea en esta etapa:** crear la **estructura base modular**, con contratos (tipos, firmas y docstrings), el ciclo de construcción y la interfaz de terminal, pero **sin implementar ningún analizador**. Los estudiantes implementarán cada etapa en proyectos sucesivos: primero el lexer, luego el parser y el AST, y al final la semántica.

---

## 2. Principios

1. **Modularidad por etapas.** Cada etapa vive en su paquete, expone una sola clase de entrada y un resultado tipado. Ninguna etapa importa internos de otra: solo sus contratos públicos (`Token`, `Diagnostic`, nodos del AST, `Symbol`).
2. **Contratos primero.** Todas las firmas, dataclasses y docstrings quedan definidas. Los cuerpos de los analizadores levantan `NotImplementedError("TODO: …")`, con un docstring que explica qué debe hacer el método.
3. **El folleto manda.** Nombres de tokens, campos, códigos de diagnóstico y formato de salida siguen el capítulo IV y la SRS (sección 4). No inventes categorías, campos ni códigos.
4. **Sin dependencias externas** en tiempo de ejecución. Solo la biblioteca estándar de Python ≥ 3.10 (se usa `int | None`). `pytest` únicamente para desarrollo.
5. **Inmutabilidad y tipos.** Registros como `@dataclass(frozen=True)`, anotaciones de tipo en todo el código, sin variables globales mutables.
6. **Diagnósticos, no excepciones.** Los errores del programa fuente se registran como `Diagnostic` y el análisis continúa. Las excepciones se reservan para errores de uso (archivo inexistente) o para `NotImplementedError`.
7. **Nada de adelantarse.** No implementes el lexer, el parser ni la semántica, aunque sea «fácil». Si algo necesita lógica real para compilar, deja un stub documentado.

---

## 3. Estructura del repositorio

```
mini-c/
├── README.md                 # enunciado general, uso y convenciones
├── CLAUDE.md                 # este archivo
├── pyproject.toml            # paquete "minic", requires-python >=3.10, script "minic", pytest en [dev]
├── requirements.txt          # solo herramientas de desarrollo (pytest)
├── .gitignore
├── src/
│   └── minic/
│       ├── __init__.py
│       ├── __main__.py       # python -m minic <archivo.mc>
│       ├── main.py           # CLI: argumentos, lectura, impresión, códigos de salida
│       ├── compiler.py       # coordinador: encadena las etapas disponibles
│       ├── source/
│       │   ├── source_text.py       # SourceText(text, path); from_file() con UTF-8 y newline=""
│       │   └── source_position.py   # SourcePosition(index, line, column), uso interno
│       ├── diagnostics/
│       │   ├── diagnostic.py        # Diagnostic(code, severity, message, line, column)
│       │   ├── diagnostic_code.py   # códigos LEX/SYN/SEM de la SRS y sus mensajes
│       │   └── diagnostic_bag.py    # colección ordenada de diagnósticos
│       ├── lexer/
│       │   ├── token.py             # Token(type, lexeme, literal, line, column)
│       │   ├── token_type.py        # las 15 categorías como constantes str
│       │   ├── lexical_rules.py     # KEYWORDS, SINGLE, DOUBLE, clases de caracteres
│       │   ├── lexer_result.py      # LexerResult(tokens, diagnostics) — NamedTuple
│       │   └── lexer.py             # Lexer: métodos con NotImplementedError
│       ├── parser/
│       │   ├── parser_result.py     # ParserResult(program, diagnostics)
│       │   └── parser.py            # Parser: descendente recursivo, métodos stub
│       ├── syntax_tree/             # (no "ast": evita tapar el módulo estándar ast)
│       │   ├── node.py              # Node base con line/column
│       │   ├── program.py           # Program(statements)
│       │   ├── statements.py        # VariableDeclaration, Assignment, WhileStatement
│       │   └── expressions.py       # IntegerLiteral, IdentifierExpression, BinaryExpression, ComparisonExpression
│       ├── semantic/
│       │   ├── symbol.py            # Symbol(id, name, type, initialized, declared_line)
│       │   ├── symbol_table.py      # SymbolTable: declare, lookup, mark_initialized (stubs)
│       │   ├── semantic_result.py   # SemanticResult(symbols, diagnostics)
│       │   └── semantic_analyzer.py # SemanticAnalyzer: métodos stub
│       └── output/
│           ├── token_printer.py      # format_token (stub)
│           └── diagnostic_printer.py # format_diagnostic (stub)
├── tests/
│   ├── test_structure.py     # los paquetes importan; contratos con los campos correctos
│   ├── lexer/                # vacío con README: pruebas del proyecto del lexer
│   ├── parser/               # ídem
│   └── semantic/             # ídem
└── examples/
    ├── valid/example01.mc    # int x = 10; while (x != 0) { x = x - 1; }
    └── invalid/example01.mc  # x ! = 0;\ny=2;
```

Cada `__init__.py` exporta solo la API pública de su paquete. Los módulos de etapas futuras llevan un docstring que indica **en qué proyecto se implementan**.

---

## 4. Especificación de Mini C (resumen de la SRS)

### 4.1 Léxico (capítulo IV, §4.4)

| Tipo | Escritura o patrón |
|---|---|
| `KW_INT`, `KW_WHILE` | `int`, `while` (las únicas reservadas) |
| `IDENTIFIER` | `[A-Za-z_][A-Za-z0-9_]*` (ASCII, distingue mayúsculas) |
| `INTEGER_LITERAL` | `[0-9]+` (sin signo; valor en base 10, sin cota) |
| `ASSIGN`, `PLUS`, `MINUS` | `=`, `+`, `-` |
| `EQUAL_EQUAL`, `NOT_EQUAL` | `==`, `!=` |
| `LPAREN`, `RPAREN`, `LBRACE`, `RBRACE`, `SEMICOLON` | `(`, `)`, `{`, `}`, `;` |
| `EOF` | fin de la fuente; lexema vacío |

- **Token:** `Token(type: str, lexeme: str, literal: int | None, line: int, column: int)`. `literal` es el valor solo en `INTEGER_LITERAL`; en los demás es `None`. `line` y `column` (desde 1) indican el **inicio** del lexema.
- **Posiciones:** espacio, `\t`, `\r` y `\n` se consumen sin producir tokens. Cada carácter suma una columna; solo `\n` abre una línea nueva.
- **Prioridades:** primero se consume el nombre completo y después se consultan las reservadas. `DOUBLE` se consulta antes que `SINGLE` (máxima coincidencia).
- **Recuperación:** ante un carácter sin categoría se registra `Diagnostic("LEX001", "error", "Carácter no reconocido: '<c>'", línea, columna)`, se consume ese carácter y se continúa. Siempre hay exactamente un `EOF`.
- **API:** `tokens, diagnostics = Lexer(source).scan()`.

### 4.2 Gramática (SRS §14)

```
programa     → instruccion* EOF
instruccion  → declaracion | asignacion | cicloWhile
declaracion  → KW_INT IDENTIFIER ";" | KW_INT IDENTIFIER "=" expresion ";"
asignacion   → IDENTIFIER "=" expresion ";"
cicloWhile   → KW_WHILE "(" condicion ")" bloque
bloque       → "{" instruccion* "}"
condicion    → expresion "==" expresion | expresion "!=" expresion
expresion    → termino (("+" | "-") termino)*
termino      → INTEGER_LITERAL | IDENTIFIER | "(" expresion ")"
```

Precedencia: `( )` antes que `+ -`, y estos antes que `== !=`. `+` y `-` asocian a la izquierda.

- **API futura:** `program, diagnostics = Parser(tokens).parse()`, con un método por no terminal (`parse_program`, `parse_statement`, `parse_declaration`, `parse_assignment`, `parse_while`, `parse_block`, `parse_condition`, `parse_expression`, `parse_term`) y utilidades `peek`, `advance`, `check`, `expect`.

### 4.3 AST (SRS §16)

`Program` · `Statement` → `VariableDeclaration`, `Assignment`, `WhileStatement` · `Expression` → `IntegerLiteral`, `IdentifierExpression`, `BinaryExpression`, `ComparisonExpression`. Todos los nodos son dataclasses congeladas con `line` y `column`.

### 4.4 Semántica (SRS §17–18)

- **Symbol:** `Symbol(id: int, name: str, type: str, initialized: bool, declared_line: int)`. El único tipo es `"INT"`.
- **Reglas:** declaración previa, no redeclaración en el mismo ámbito, inicialización antes de leer, y la condición de `while` debe ser una comparación.
- **API futura:** `symbols, diagnostics = SemanticAnalyzer(program).analyze()`.

### 4.5 Diagnósticos (SRS §19)

| Código | Mensaje base | Etapa |
|---|---|---|
| `LEX001` | carácter no reconocido | lexer |
| `SYN001` | se esperaba `;` | parser |
| `SYN002` | se esperaba `)` | parser |
| `SYN003` | se esperaba `}` | parser |
| `SEM001` | variable no declarada | semántica |
| `SEM002` | variable redeclarada | semántica |
| `SEM003` | variable no inicializada | semántica |
| `SEM004` | operación semánticamente inválida | semántica |

`Diagnostic(code, severity, message, line, column)`, con severidad `"error"`. `diagnostic_code.py` define estas constantes y una función de mensaje por código.

### 4.6 Características excluidas

`if`, `else`, `for`, funciones, `main`, `return`, `printf`, `*`, `/`, `%`, `<`, `>`, `<=`, `>=`, `&&`, `||`, arreglos, cadenas, `float`, `bool`, comentarios. Palabras como `if` o `printf` son identificadores; símbolos como `*` o `<` producen `LEX001`.

---

## 5. Interfaz de terminal

```
python -m minic <archivo.mc>        # o: minic <archivo.mc>
```

- **Sin diagnósticos:** un token por línea con sus campos separados por un espacio, `TIPO 'lexema' línea columna`, y al final `Tokens preparados para el analizador sintáctico.`
- **Con diagnósticos:** un diagnóstico por línea, `CÓDIGO severidad línea:columna mensaje`, y al final `La fuente contiene errores léxicos.` En ese caso no se imprimen tokens.
- **Códigos de salida:** 0 sin diagnósticos, 1 con errores del programa fuente, 2 si falta el argumento o el archivo no se puede leer.
- **En este esqueleto:** `main` valida los argumentos y lee el archivo (esto sí se implementa). Si la etapa aún no existe, informa en stderr «Etapa léxica no implementada todavía» y sale con código 3. No imprimas tokens falsos.
- `compiler.py` expone `compile_source(text, stages=("lexer",))` y encadena solo las etapas pedidas. Cuando existan parser y semántica, el formato de salida de esas etapas se definirá en su proyecto.

---

## 6. Pruebas del esqueleto

`tests/test_structure.py` debe verificar, sin depender de analizadores implementados:

- que todos los paquetes y clases públicas se importan;
- que `Token`, `Diagnostic` y `Symbol` tienen exactamente los campos y el orden de la sección 4, y son inmutables;
- que `TokenType` contiene las 15 categorías y que `KEYWORDS`, `SINGLE` y `DOUBLE` coinciden con §4.1;
- que `diagnostic_code` define los 8 códigos;
- que `Lexer("").scan()`, `Parser([]).parse()` y `SemanticAnalyzer(...).analyze()` levantan `NotImplementedError`;
- que la CLI devuelve 2 sin argumento o con archivo inexistente, y 3 con un archivo válido mientras el lexer no exista.

`python -m pytest` debe pasar completo sobre el esqueleto.

---

## 7. Estilo y convenciones

- Código y nombres en inglés (coinciden con la SRS). Docstrings, mensajes de diagnóstico, README y comentarios, en español.
- Un módulo por responsabilidad; funciones pequeñas; nada de `print` fuera de `main.py` y `output/`.
- Tipos: `list[Token]`, `int | None`, `NamedTuple` para los resultados de cada etapa (permiten `a, b = resultado`).
- Formato con el estilo de PEP 8; no agregues herramientas nuevas (linters, formateadores) sin preguntarme.
- Cada stub incluye en su docstring qué debe hacer, qué recibe, qué devuelve y la sección del folleto o de la SRS que lo define.

---

## 8. Forma de trabajar conmigo

1. Antes de crear archivos, **resume el plan** (lista de archivos y contratos) y espera mi confirmación.
2. Si falta información o hay dos interpretaciones posibles, **pregunta**; no la inventes.
3. Al terminar, ejecuta `python -m pytest` y `python -m minic examples/valid/example01.mc`, y reporta qué se creó, qué pruebas pasaron y qué quedó como stub.
4. No hagas commits ni cambies la estructura de carpetas sin pedírmelo.
5. Hoja de ruta posterior (no ahora): proyecto 1 lexer → proyecto 2 parser y AST → proyecto 3 semántica y tabla de símbolos. Cada proyecto rellena sus stubs sin cambiar los contratos ya definidos.
