"""Analizador sintáctico descendente recursivo de Mini C.

Se implementa en el **proyecto 2**. Hay un método por no terminal de la
gramática (SRS §14) y utilidades para recorrer los tokens.
"""

from minic.diagnostics.diagnostic_bag import DiagnosticBag
from minic.lexer.token import Token
from minic.parser.parser_result import ParserResult
from minic.syntax_tree.expressions import Expression
from minic.syntax_tree.program import Program
from minic.syntax_tree.statements import (
    Assignment,
    Statement,
    VariableDeclaration,
    WhileStatement,
)


class Parser:
    """Convierte la lista de tokens en un AST.

    Uso: ``program, diagnostics = Parser(tokens).parse()``.
    """

    def __init__(self, tokens: list[Token]) -> None:
        """Recibe los tokens del lexer, terminados en ``EOF``."""
        self._tokens = tokens
        self._current = 0
        self._diagnostics = DiagnosticBag()

    def parse(self) -> ParserResult:
        """Analiza el programa completo y devuelve el AST y los diagnósticos.

        Llama a ``parse_program`` y empaqueta el resultado.

        Devuelve:
            ``ParserResult(program, diagnostics)``.
        """
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.parse")

    # --- No terminales (SRS §14) -------------------------------------------

    def parse_program(self) -> Program:
        """``programa → instruccion* EOF``.

        Repite ``parse_statement`` hasta encontrar ``EOF``.
        """
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.parse_program")

    def parse_statement(self) -> Statement | None:
        """``instruccion → declaracion | asignacion | cicloWhile``.

        Decide por el token actual: ``KW_INT``, ``IDENTIFIER`` o ``KW_WHILE``.
        Devuelve ``None`` si no pudo reconocer una instrucción y tuvo que
        recuperarse.
        """
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.parse_statement")

    def parse_declaration(self) -> VariableDeclaration:
        """``declaracion → KW_INT IDENTIFIER ";" | KW_INT IDENTIFIER "=" expresion ";"``.

        Si falta ``;`` registra ``SYN001``.
        """
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.parse_declaration")

    def parse_assignment(self) -> Assignment:
        """``asignacion → IDENTIFIER "=" expresion ";"``.

        Si falta ``;`` registra ``SYN001``.
        """
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.parse_assignment")

    def parse_while(self) -> WhileStatement:
        """``cicloWhile → KW_WHILE "(" condicion ")" bloque``.

        Si falta ``)`` registra ``SYN002``.
        """
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.parse_while")

    def parse_block(self) -> tuple[Statement, ...]:
        """``bloque → "{" instruccion* "}"``.

        Si falta ``}`` registra ``SYN003``.
        """
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.parse_block")

    def parse_condition(self) -> Expression:
        """``condicion → expresion ("==" | "!=") expresion``.

        Devuelve una ``ComparisonExpression``. ``==`` y ``!=`` tienen menor
        precedencia que ``+`` y ``-``.
        """
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.parse_condition")

    def parse_expression(self) -> Expression:
        """``expresion → termino (("+" | "-") termino)*``.

        Construye ``BinaryExpression`` asociando a la izquierda:
        ``a - b - c`` equivale a ``(a - b) - c``.
        """
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.parse_expression")

    def parse_term(self) -> Expression:
        """``termino → INTEGER_LITERAL | IDENTIFIER | "(" expresion ")"``.

        Si falta el ``)`` de cierre registra ``SYN002``.
        """
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.parse_term")

    # --- Utilidades --------------------------------------------------------

    def peek(self) -> Token:
        """Devuelve el token actual sin consumirlo."""
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.peek")

    def advance(self) -> Token:
        """Consume y devuelve el token actual; nunca avanza más allá de ``EOF``."""
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.advance")

    def check(self, token_type: str) -> bool:
        """Indica si el token actual es de tipo ``token_type``, sin consumirlo."""
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.check")

    def expect(self, token_type: str, code: str, message: str) -> Token | None:
        """Consume el token si es de tipo ``token_type``.

        Si no lo es, registra el diagnóstico ``code`` con ``message`` en la
        posición del token actual y devuelve ``None`` sin detener el análisis.
        """
        raise NotImplementedError("TODO: proyecto 2 — implementar Parser.expect")
