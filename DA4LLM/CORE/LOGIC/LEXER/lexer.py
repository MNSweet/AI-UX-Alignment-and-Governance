"""Lexer for the deliberately small DA4LLM CORE POC language."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from ...model import LexError


class TokenKind(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    BOOLEAN = auto()
    NULL = auto()
    EQUAL = auto()
    NEWLINE = auto()
    EOF = auto()


KEYWORDS = {
    "MODULE", "VERSION", "PROCEDURE", "SET", "CALL_CAPABILITY",
    "WITH", "AS", "ON_UNAVAILABLE", "CONTINUE", "HALT", "RETURN", "END",
}

TOKEN_PATTERN = re.compile(
    r"(?P<SPACE>[ \t]+)|"
    r"(?P<COMMENT>\#[^\n]*)|"
    r"(?P<STRING>\"(?:\\.|[^\"\\])*\")|"
    r"(?P<FLOAT>-?(?:0|[1-9]\d*)\.\d+)|"
    r"(?P<INTEGER>-?(?:0|[1-9]\d*))|"
    r"(?P<EQUAL>=)|"
    r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_.-]*)|"
    r"(?P<NEWLINE>\n)|"
    r"(?P<MISMATCH>.)"
)


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    text: str
    value: Any
    line: int
    column: int


def tokenize(source: str) -> tuple[Token, ...]:
    tokens: list[Token] = []
    line = 1
    line_start = 0
    for match in TOKEN_PATTERN.finditer(source):
        group = match.lastgroup
        text = match.group()
        column = match.start() - line_start + 1
        if group in {"SPACE", "COMMENT"}:
            continue
        if group == "NEWLINE":
            tokens.append(Token(TokenKind.NEWLINE, text, None, line, column))
            line += 1
            line_start = match.end()
            continue
        if group == "STRING":
            tokens.append(Token(TokenKind.STRING, text, ast.literal_eval(text), line, column))
            continue
        if group == "FLOAT":
            tokens.append(Token(TokenKind.FLOAT, text, float(text), line, column))
            continue
        if group == "INTEGER":
            tokens.append(Token(TokenKind.INTEGER, text, int(text), line, column))
            continue
        if group == "EQUAL":
            tokens.append(Token(TokenKind.EQUAL, text, text, line, column))
            continue
        if group == "IDENTIFIER":
            upper = text.upper()
            if upper in KEYWORDS:
                tokens.append(Token(TokenKind.KEYWORD, upper, upper, line, column))
            elif upper in {"TRUE", "FALSE"}:
                tokens.append(Token(TokenKind.BOOLEAN, text, upper == "TRUE", line, column))
            elif upper == "NULL":
                tokens.append(Token(TokenKind.NULL, text, None, line, column))
            else:
                tokens.append(Token(TokenKind.IDENTIFIER, text, text, line, column))
            continue
        raise LexError(f"Unexpected character {text!r} at line {line}, column {column}")
    if not tokens or tokens[-1].kind is not TokenKind.NEWLINE:
        tokens.append(Token(TokenKind.NEWLINE, "\n", None, line, 1))
    tokens.append(Token(TokenKind.EOF, "", None, line + 1, 1))
    return tuple(tokens)
