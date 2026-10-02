"""Analizador semántico de Mini C.

Se implementa en el **proyecto 3**. Recorre el AST y aplica las reglas de la
SRS §17–18 con ayuda de ``SymbolTable``.
"""

from minic.diagnostics.diagnostic_bag import DiagnosticBag
from minic.semantic.semantic_result import SemanticResult
from minic.semantic.symbol_table import SymbolTable
from minic.syntax_tree.expressions import Expression
from minic.syntax_tree.program import Program
from minic.syntax_tree.statements import (
    Assignment,
    Statement,
    VariableDeclaration,
    WhileStatement,
)


class SemanticAnalyzer:
    """Verifica las reglas semánticas de un programa ya analizado.

    Uso: ``symbols, diagnostics = SemanticAnalyzer(program).analyze()``.
    """

    def __init__(self, program: Program) -> None:
        """Recibe la raíz del AST producida por el parser."""
        self._program = program
        self._table = SymbolTable()
        self._diagnostics = DiagnosticBag()

    def analyze(self) -> SemanticResult:
        """Recorre todas las instrucciones del programa y devuelve el resultado.

        Devuelve:
            ``SemanticResult(symbols, diagnostics)``.
        """
        raise NotImplementedError("TODO: proyecto 3 — implementar SemanticAnalyzer.analyze")

    def _visit_statement(self, statement: Statement) -> None:
        """Despacha según el tipo concreto de instrucción."""
        raise NotImplementedError("TODO: proyecto 3 — implementar SemanticAnalyzer._visit_statement")

    def _visit_declaration(self, node: VariableDeclaration) -> None:
        """Verifica el inicializador (si existe) y declara la variable.

        Redeclarar en el mismo ámbito registra ``SEM002``.
        """
        raise NotImplementedError("TODO: proyecto 3 — implementar SemanticAnalyzer._visit_declaration")

    def _visit_assignment(self, node: Assignment) -> None:
        """Verifica el valor y marca la variable como inicializada.

        Asignar a una variable no declarada registra ``SEM001``.
        """
        raise NotImplementedError("TODO: proyecto 3 — implementar SemanticAnalyzer._visit_assignment")

    def _visit_while(self, node: WhileStatement) -> None:
        """Verifica la condición con ``_check_condition`` y luego el cuerpo."""
        raise NotImplementedError("TODO: proyecto 3 — implementar SemanticAnalyzer._visit_while")

    def _check_condition(self, condition: Expression) -> None:
        """Exige que la condición del ``while`` sea una ``ComparisonExpression``.

        Si no lo es registra ``SEM004``. Luego verifica ambos lados.
        """
        raise NotImplementedError("TODO: proyecto 3 — implementar SemanticAnalyzer._check_condition")

    def _visit_expression(self, expression: Expression) -> None:
        """Verifica cada lectura de variable dentro de la expresión.

        Variable no declarada: ``SEM001``. Declarada pero sin valor: ``SEM003``.
        """
        raise NotImplementedError("TODO: proyecto 3 — implementar SemanticAnalyzer._visit_expression")
