"""Pruebas del esqueleto: importaciones, contratos y CLI.

No dependen de ningún analizador implementado (CLAUDE.md §6).
"""

import dataclasses
import importlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
VALID_EXAMPLE = ROOT / "examples" / "valid" / "example01.mc"

PACKAGES = [
    "minic",
    "minic.main",
    "minic.compiler",
    "minic.source",
    "minic.diagnostics",
    "minic.lexer",
    "minic.parser",
    "minic.syntax_tree",
    "minic.semantic",
    "minic.output",
]

PUBLIC_API = {
    "minic": ["compile_source", "CompilationResult"],
    "minic.source": ["SourceText", "SourcePosition"],
    "minic.diagnostics": ["Diagnostic", "DiagnosticBag", "diagnostic_code"],
    "minic.lexer": ["Lexer", "LexerResult", "Token", "TokenType"],
    "minic.parser": ["Parser", "ParserResult"],
    "minic.syntax_tree": [
        "Node",
        "Program",
        "Statement",
        "VariableDeclaration",
        "Assignment",
        "WhileStatement",
        "Expression",
        "IntegerLiteral",
        "IdentifierExpression",
        "BinaryExpression",
        "ComparisonExpression",
    ],
    "minic.semantic": ["SemanticAnalyzer", "SemanticResult", "Symbol", "SymbolTable"],
    "minic.output": ["format_token", "format_diagnostic"],
}


def field_names(cls: type) -> list[str]:
    return [field.name for field in dataclasses.fields(cls)]


# --- Importaciones -----------------------------------------------------------


@pytest.mark.parametrize("module_name", PACKAGES)
def test_package_imports(module_name: str) -> None:
    importlib.import_module(module_name)


@pytest.mark.parametrize("module_name, names", PUBLIC_API.items())
def test_public_api_is_exported(module_name: str, names: list[str]) -> None:
    module = importlib.import_module(module_name)
    for name in names:
        assert hasattr(module, name), f"{module_name} no exporta {name}"


# --- Registros ---------------------------------------------------------------


def test_token_fields() -> None:
    from minic.lexer import Token

    assert field_names(Token) == ["type", "lexeme", "literal", "line", "column"]


def test_diagnostic_fields() -> None:
    from minic.diagnostics import Diagnostic

    assert field_names(Diagnostic) == ["code", "severity", "message", "line", "column"]


def test_symbol_fields() -> None:
    from minic.semantic import Symbol

    assert field_names(Symbol) == ["id", "name", "type", "initialized", "declared_line"]


def test_records_are_immutable() -> None:
    from minic.diagnostics import Diagnostic
    from minic.lexer import Token
    from minic.semantic import Symbol

    records = [
        (Token("IDENTIFIER", "x", None, 1, 1), "lexeme"),
        (Diagnostic("LEX001", "error", "m", 1, 1), "message"),
        (Symbol(1, "x", "INT", False, 1), "initialized"),
    ]
    for record, attribute in records:
        with pytest.raises(dataclasses.FrozenInstanceError):
            setattr(record, attribute, "otro")


def test_ast_nodes_are_frozen_and_carry_position() -> None:
    from minic.syntax_tree import IntegerLiteral, Program

    literal = IntegerLiteral(10, line=1, column=9)
    program = Program((), line=1, column=1)
    assert (literal.line, literal.column) == (1, 9)
    with pytest.raises(dataclasses.FrozenInstanceError):
        program.statements = ()  # type: ignore[misc]


def test_stage_results_unpack() -> None:
    from minic.lexer import LexerResult
    from minic.parser import ParserResult
    from minic.semantic import SemanticResult

    assert LexerResult._fields == ("tokens", "diagnostics")
    assert ParserResult._fields == ("program", "diagnostics")
    assert SemanticResult._fields == ("symbols", "diagnostics")
    tokens, diagnostics = LexerResult([], [])
    assert tokens == [] and diagnostics == []


# --- Reglas léxicas ----------------------------------------------------------


def test_token_types() -> None:
    from minic.lexer import TokenType

    expected = {
        "KW_INT",
        "KW_WHILE",
        "IDENTIFIER",
        "INTEGER_LITERAL",
        "ASSIGN",
        "PLUS",
        "MINUS",
        "EQUAL_EQUAL",
        "NOT_EQUAL",
        "LPAREN",
        "RPAREN",
        "LBRACE",
        "RBRACE",
        "SEMICOLON",
        "EOF",
    }
    assert len(TokenType.ALL) == 15
    assert set(TokenType.ALL) == expected
    for name in expected:
        assert getattr(TokenType, name) == name


def test_lexical_tables() -> None:
    from minic.lexer import lexical_rules

    assert dict(lexical_rules.KEYWORDS) == {"int": "KW_INT", "while": "KW_WHILE"}
    assert dict(lexical_rules.DOUBLE) == {"==": "EQUAL_EQUAL", "!=": "NOT_EQUAL"}
    assert dict(lexical_rules.SINGLE) == {
        "=": "ASSIGN",
        "+": "PLUS",
        "-": "MINUS",
        "(": "LPAREN",
        ")": "RPAREN",
        "{": "LBRACE",
        "}": "RBRACE",
        ";": "SEMICOLON",
    }
    assert lexical_rules.WHITESPACE == frozenset(" \t\r\n")


def test_lexical_tables_are_read_only() -> None:
    from minic.lexer import lexical_rules

    with pytest.raises(TypeError):
        lexical_rules.KEYWORDS["if"] = "KW_IF"  # type: ignore[index]


# --- Diagnósticos ------------------------------------------------------------


def test_diagnostic_codes() -> None:
    from minic.diagnostics import diagnostic_code

    expected = ("LEX001", "SYN001", "SYN002", "SYN003", "SEM001", "SEM002", "SEM003", "SEM004")
    assert diagnostic_code.ALL_CODES == expected
    for code in expected:
        assert getattr(diagnostic_code, code) == code


def test_lex001_message() -> None:
    from minic.diagnostics import diagnostic_code

    assert diagnostic_code.unrecognized_character("!") == "Carácter no reconocido: '!'"


def test_diagnostic_bag_keeps_order() -> None:
    from minic.diagnostics import DiagnosticBag

    bag = DiagnosticBag()
    assert len(bag) == 0 and not bag.has_errors()
    bag.report("LEX001", "a", 1, 1)
    bag.report("LEX001", "b", 2, 1)
    assert [d.message for d in bag] == ["a", "b"]
    assert bag.has_errors()


# --- Etapas pendientes -------------------------------------------------------


def test_lexer_is_stub() -> None:
    from minic.lexer import Lexer

    with pytest.raises(NotImplementedError):
        Lexer("").scan()


def test_parser_is_stub() -> None:
    from minic.parser import Parser

    with pytest.raises(NotImplementedError):
        Parser([]).parse()


def test_semantic_analyzer_is_stub() -> None:
    from minic.semantic import SemanticAnalyzer
    from minic.syntax_tree import Program

    with pytest.raises(NotImplementedError):
        SemanticAnalyzer(Program((), line=1, column=1)).analyze()


def test_compile_source_rejects_invalid_stages() -> None:
    from minic import compile_source

    with pytest.raises(ValueError):
        compile_source("", stages=("parser",))


# --- CLI ---------------------------------------------------------------------


def test_cli_without_argument_returns_2() -> None:
    from minic.main import main

    assert main([]) == 2


def test_cli_with_missing_file_returns_2(tmp_path: Path) -> None:
    from minic.main import main

    assert main([str(tmp_path / "no_existe.mc")]) == 2


def test_cli_with_valid_file_returns_3_while_lexer_missing(capsys: pytest.CaptureFixture[str]) -> None:
    from minic.main import main

    assert main([str(VALID_EXAMPLE)]) == 3
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Etapa léxica no implementada todavía" in captured.err


def test_python_dash_m_entry_point() -> None:
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    completed = subprocess.run(
        [sys.executable, "-m", "minic", str(VALID_EXAMPLE)],
        capture_output=True,
        text=True,
        env=env,
    )
    assert completed.returncode == 3
