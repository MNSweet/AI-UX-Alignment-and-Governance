"""Parser for the DA4LLM CORE POC language."""

from __future__ import annotations

from pathlib import Path

from ...model import CapabilityStatement, Literal, LogicModule, ParseError, ReturnStatement, SetStatement
from ..LEXER import Token, TokenKind, tokenize


LITERAL_TYPES = {
    TokenKind.STRING: "string", TokenKind.INTEGER: "integer", TokenKind.FLOAT: "float",
    TokenKind.BOOLEAN: "boolean", TokenKind.NULL: "null",
}


class Parser:
    def __init__(self, tokens: tuple[Token, ...], source: Path):
        self.tokens = tokens
        self.source = source
        self.position = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.position]

    def advance(self) -> Token:
        token = self.current
        self.position += 1
        return token

    def skip_newlines(self) -> None:
        while self.current.kind is TokenKind.NEWLINE:
            self.advance()

    def expect_keyword(self, keyword: str) -> Token:
        token = self.current
        if token.kind is not TokenKind.KEYWORD or token.value != keyword:
            raise ParseError(f"Expected {keyword} at line {token.line}, found {token.text!r}")
        return self.advance()

    def expect_kind(self, kind: TokenKind, description: str) -> Token:
        token = self.current
        if token.kind is not kind:
            raise ParseError(f"Expected {description} at line {token.line}, found {token.text!r}")
        return self.advance()

    def end_line(self) -> None:
        self.expect_kind(TokenKind.NEWLINE, "end of line")
        self.skip_newlines()

    def parse(self) -> LogicModule:
        self.skip_newlines()
        self.expect_keyword("MODULE")
        name = self.expect_kind(TokenKind.IDENTIFIER, "module name").value
        self.expect_keyword("VERSION")
        version = self.expect_kind(TokenKind.STRING, "quoted module version").value
        self.end_line()
        self.expect_keyword("PROCEDURE")
        procedure = self.expect_kind(TokenKind.IDENTIFIER, "procedure name").value
        self.end_line()
        statements = []
        while not (self.current.kind is TokenKind.KEYWORD and self.current.value == "END"):
            if self.current.kind is TokenKind.EOF:
                raise ParseError("Procedure is missing END")
            statements.append(self.parse_statement())
            self.end_line()
        self.expect_keyword("END")
        self.end_line()
        if self.current.kind is not TokenKind.EOF:
            raise ParseError(f"Unexpected content at line {self.current.line}")
        return LogicModule(name, version, procedure, tuple(statements), self.source)

    def parse_statement(self):
        token = self.current
        if token.kind is not TokenKind.KEYWORD:
            raise ParseError(f"Expected opcode at line {token.line}, found {token.text!r}")
        if token.value == "SET":
            return self.parse_set()
        if token.value == "CALL_CAPABILITY":
            return self.parse_capability()
        if token.value == "RETURN":
            return self.parse_return()
        raise ParseError(f"Unknown or misplaced opcode {token.value} at line {token.line}")

    def parse_set(self) -> SetStatement:
        line = self.expect_keyword("SET").line
        name = self.expect_kind(TokenKind.IDENTIFIER, "variable name").value
        self.expect_kind(TokenKind.EQUAL, "=")
        token = self.current
        if token.kind not in LITERAL_TYPES:
            raise ParseError(f"Expected literal at line {token.line}, found {token.text!r}")
        self.advance()
        return SetStatement(name, Literal(token.text, token.value, LITERAL_TYPES[token.kind], token.line), line)

    def parse_capability(self) -> CapabilityStatement:
        line = self.expect_keyword("CALL_CAPABILITY").line
        capability = self.expect_kind(TokenKind.STRING, "quoted capability name").value
        payload = None
        result = None
        behavior = "HALT"
        if self.current.kind is TokenKind.KEYWORD and self.current.value == "WITH":
            self.advance()
            payload = self.expect_kind(TokenKind.IDENTIFIER, "payload variable").value
        if self.current.kind is TokenKind.KEYWORD and self.current.value == "AS":
            self.advance()
            result = self.expect_kind(TokenKind.IDENTIFIER, "result variable").value
        if self.current.kind is TokenKind.KEYWORD and self.current.value == "ON_UNAVAILABLE":
            self.advance()
            choice = self.current
            if choice.kind is not TokenKind.KEYWORD or choice.value not in {"CONTINUE", "HALT"}:
                raise ParseError(f"Expected CONTINUE or HALT at line {choice.line}")
            behavior = self.advance().value
        return CapabilityStatement(capability, payload, result, behavior, line)

    def parse_return(self) -> ReturnStatement:
        line = self.expect_keyword("RETURN").line
        variable = self.expect_kind(TokenKind.IDENTIFIER, "return variable").value
        return ReturnStatement(variable, line)


def parse(source_text: str, source: Path | str = Path("<memory>")) -> LogicModule:
    return Parser(tokenize(source_text), Path(source)).parse()
