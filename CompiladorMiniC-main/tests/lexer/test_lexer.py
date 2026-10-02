"""Pruebas del analizador léxico de Mini C según la skill analizador-lexico-mini-c."""

from minic.diagnostics.diagnostic import Diagnostic
from minic.lexer.lexer import Lexer
from minic.lexer.token import Token
from minic.lexer.token_type import TokenType
from minic.output.diagnostic_printer import format_diagnostic
from minic.output.token_printer import format_token


def test_section_7_case_1() -> None:
    source = "int2 = 12abc;\nwhilex == -5"
    tokens, diagnostics = Lexer(source).scan()

    assert diagnostics == []

    expected = [
        Token(TokenType.IDENTIFIER, "int2", None, 1, 1),
        Token(TokenType.ASSIGN, "=", None, 1, 6),
        Token(TokenType.INTEGER_LITERAL, "12", 12, 1, 8),
        Token(TokenType.IDENTIFIER, "abc", None, 1, 10),
        Token(TokenType.SEMICOLON, ";", None, 1, 13),
        Token(TokenType.IDENTIFIER, "whilex", None, 2, 1),
        Token(TokenType.EQUAL_EQUAL, "==", None, 2, 8),
        Token(TokenType.MINUS, "-", None, 2, 11),
        Token(TokenType.INTEGER_LITERAL, "5", 5, 2, 12),
        Token(TokenType.EOF, "", None, 2, 13),
    ]

    assert tokens == expected

    formatted = [format_token(t) for t in tokens]
    expected_output = [
        "IDENTIFIER 'int2' 1 1",
        "ASSIGN '=' 1 6",
        "INTEGER_LITERAL '12' 1 8",
        "IDENTIFIER 'abc' 1 10",
        "SEMICOLON ';' 1 13",
        "IDENTIFIER 'whilex' 2 1",
        "EQUAL_EQUAL '==' 2 8",
        "MINUS '-' 2 11",
        "INTEGER_LITERAL '5' 2 12",
        "EOF '' 2 13",
    ]
    assert formatted == expected_output


def test_section_7_case_2_with_errors() -> None:
    source = "int x = @;\nx ! = 0; // fin"
    tokens, diagnostics = Lexer(source).scan()

    expected_tokens = [
        Token(TokenType.KW_INT, "int", None, 1, 1),
        Token(TokenType.IDENTIFIER, "x", None, 1, 5),
        Token(TokenType.ASSIGN, "=", None, 1, 7),
        Token(TokenType.SEMICOLON, ";", None, 1, 10),
        Token(TokenType.IDENTIFIER, "x", None, 2, 1),
        Token(TokenType.ASSIGN, "=", None, 2, 5),
        Token(TokenType.INTEGER_LITERAL, "0", 0, 2, 7),
        Token(TokenType.SEMICOLON, ";", None, 2, 8),
        Token(TokenType.IDENTIFIER, "fin", None, 2, 13),
        Token(TokenType.EOF, "", None, 2, 16),
    ]
    assert tokens == expected_tokens

    expected_diagnostics = [
        Diagnostic("LEX001", "error", "Carácter no reconocido: '@'", 1, 9),
        Diagnostic("LEX001", "error", "Carácter no reconocido: '!'", 2, 3),
        Diagnostic("LEX001", "error", "Carácter no reconocido: '/'", 2, 10),
        Diagnostic("LEX001", "error", "Carácter no reconocido: '/'", 2, 11),
    ]
    assert diagnostics == expected_diagnostics

    formatted_diagnostics = [format_diagnostic(d) for d in diagnostics]
    expected_diag_str = [
        "LEX001 error 1:9 Carácter no reconocido: '@'",
        "LEX001 error 2:3 Carácter no reconocido: '!'",
        "LEX001 error 2:10 Carácter no reconocido: '/'",
        "LEX001 error 2:11 Carácter no reconocido: '/'",
    ]
    assert formatted_diagnostics == expected_diag_str


def test_all_15_token_types() -> None:
    source = "int while my_var_1 007 = + - == != ( ) { } ;"
    tokens, diagnostics = Lexer(source).scan()
    assert diagnostics == []

    types = [t.type for t in tokens]
    assert types == [
        TokenType.KW_INT,
        TokenType.KW_WHILE,
        TokenType.IDENTIFIER,
        TokenType.INTEGER_LITERAL,
        TokenType.ASSIGN,
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.EQUAL_EQUAL,
        TokenType.NOT_EQUAL,
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.LBRACE,
        TokenType.RBRACE,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]
    assert tokens[3].literal == 7


def test_positions_and_newlines() -> None:
    # \t cuenta como 1 columna
    # \r solo es un blanco (consume columna, no abre linea)
    source = "\tint\r\nx"
    tokens, _ = Lexer(source).scan()
    # \t está en col 1 -> int empieza en col 2
    assert tokens[0] == Token(TokenType.KW_INT, "int", None, 1, 2)
    # luego \r (col 5), \n (abre línea 2, col 1) -> x en (2, 1)
    assert tokens[1] == Token(TokenType.IDENTIFIER, "x", None, 2, 1)


def test_number_followed_by_letters() -> None:
    tokens, _ = Lexer("123abc456").scan()
    assert tokens[0] == Token(TokenType.INTEGER_LITERAL, "123", 123, 1, 1)
    assert tokens[1] == Token(TokenType.IDENTIFIER, "abc456", None, 1, 4)


def test_empty_source() -> None:
    tokens, diagnostics = Lexer("").scan()
    assert diagnostics == []
    assert tokens == [Token(TokenType.EOF, "", None, 1, 1)]


def test_whitespace_only() -> None:
    tokens, diagnostics = Lexer("   \t\r\n  ").scan()
    assert diagnostics == []
    assert tokens == [Token(TokenType.EOF, "", None, 2, 3)]
