"""Las 15 categorías de token de Mini C (capítulo IV, §4.4)."""


class TokenType:
    """Constantes ``str`` con el nombre de cada categoría.

    No se instancia: se usa como espacio de nombres, por ejemplo
    ``TokenType.IDENTIFIER``.
    """

    KW_INT = "KW_INT"
    KW_WHILE = "KW_WHILE"
    IDENTIFIER = "IDENTIFIER"
    INTEGER_LITERAL = "INTEGER_LITERAL"
    ASSIGN = "ASSIGN"
    PLUS = "PLUS"
    MINUS = "MINUS"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    SEMICOLON = "SEMICOLON"
    EOF = "EOF"

    ALL: tuple[str, ...] = (
        KW_INT,
        KW_WHILE,
        IDENTIFIER,
        INTEGER_LITERAL,
        ASSIGN,
        PLUS,
        MINUS,
        EQUAL_EQUAL,
        NOT_EQUAL,
        LPAREN,
        RPAREN,
        LBRACE,
        RBRACE,
        SEMICOLON,
        EOF,
    )
    """Las 15 categorías en el orden de la tabla del folleto."""
