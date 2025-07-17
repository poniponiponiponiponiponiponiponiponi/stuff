use crate::errors;
use crate::context::Context;

#[derive(Debug, Clone)]
pub enum TokenType {
  // Single-character tokens.
  LeftParen, RightParen, LeftBrace, RightBrace,
  Comma, Dot, Minus, Plus, Semicolon, Slash, Star,

  // One or two character tokens.
  Bang, BangEqual,
  Equal, EqualEqual,
  Greater, GreaterEqual,
  Less, LessEqual,

  // Literals.
  Identifier, String, Number,

  // Keywords.
  And, Class, Else, False, Fun, For, If, Nil, Or,
  Print, Return, Super, This, True, Var, While,

  Eof
}

#[derive(Debug, Clone)]
pub enum Literal {
    None,
    String(String),
    Number(f64),
    Identifier
}

#[derive(Debug, Clone)]
pub struct Token {
    token_type: TokenType,
    lexeme: String,
    literal: Literal,
    line: usize,
}

impl Token {

}

#[derive(Debug)]
pub struct Scanner<'a> {
    source: &'a str,
    start: usize,
    current: usize,
    line: usize,
    tokens: Vec<Token>
}

fn get_keyword(s: &str) -> Option<TokenType> {
    match s {
        "and" => Some(TokenType::And),
        "class" => Some(TokenType::Class),
        "else" => Some(TokenType::Else),
        "false" => Some(TokenType::False),
        "for" => Some(TokenType::For),
        "fun" => Some(TokenType::Fun),
        "if" => Some(TokenType::If),
        "nil" => Some(TokenType::Nil),
        "or" => Some(TokenType::Or),
        "print" => Some(TokenType::Print),
        "return" => Some(TokenType::Return),
        "super" => Some(TokenType::Super),
        "this" => Some(TokenType::This),
        "true" => Some(TokenType::True),
        "var" => Some(TokenType::Var),
        "while" => Some(TokenType::While),
        _ => None
    }
}

impl<'a> Scanner<'a> {
    pub fn from(s: &str) -> Scanner<'_> {
        Scanner {
            source: s,
            start: 0,
            current: 0,
            line: 1,
            tokens: Vec::new()
        }
    }

    pub fn is_at_end(&self) -> bool {
        self.source.len() <= self.current
    }

    pub fn scan_tokens(&mut self, ctx: &mut Context) -> Vec<Token> {
        while !self.is_at_end() {
            self.start = self.current;
            self.scan_token(ctx);
        }

        self.tokens.push(Token {
            token_type: TokenType::Eof,
            lexeme: "".to_string(),
            literal: Literal::None,
            line: self.line
        });

        self.tokens.clone()
    }

    pub fn advance(&mut self) -> char {
        let ret = self.source.as_bytes()[self.current] as char;
        self.current += 1;
        ret
    }

    pub fn add_token(&mut self, token_type: TokenType) {
        self.add_token_literal(token_type, Literal::None);
    }

    pub fn add_token_literal(&mut self, token_type: TokenType, literal: Literal) {
        let substr = &self.source.as_bytes()[self.start..self.current];
        let text = String::from_utf8_lossy(substr).into_owned();
        self.tokens.push(Token {
            token_type: token_type,
            lexeme: text,
            literal: literal,
            line: self.line
        });
    }

    fn match_char(&mut self, expected: char) -> bool {
        if self.is_at_end() {
            return false;
        }
        if self.source.as_bytes()[self.current] as char != expected {
            return false;
        }

        self.current += 1;
        true
    }

    fn peek(&self) -> char {
        if self.is_at_end() {
            return '\0';
        }
        return self.source.as_bytes()[self.current] as char;
    }

    fn peek_next(&self) -> char {
        if self.current+1 >= self.source.len() {
            return '\0';
        }

        self.source.as_bytes()[self.current+1] as char
    }

    fn string(&mut self, ctx: &mut Context) {
        while self.peek() != '"' && !self.is_at_end() {
            if self.peek() == '\n' {
                self.line += 1;
            }
            self.advance();
        }

        if self.is_at_end() {
            errors::error(ctx, self.line, "Unterminated string");
        }

        // the closing "
        self.advance();
        
        let val = &self.source.as_bytes()[self.start+1..self.current-1];
        let val = Literal::String(String::from_utf8_lossy(val).into_owned());
        self.add_token_literal(TokenType::String, val);
    }

    fn number(&mut self, ctx: &mut Context) {
        while self.peek().is_digit(10) {
            self.advance();
        }

        if self.peek() == '.' && self.peek_next().is_digit(10) {
            // consume '.'
            self.advance();

            while self.peek().is_digit(10) {
                self.advance();
            }
        }

        let substr = &self.source.as_bytes()[self.start..self.current];
        let val = String::from_utf8_lossy(substr).into_owned();
        let val = Literal::Number(val.parse().unwrap());
        self.add_token_literal(TokenType::Number, val);
    }

    fn identifier(&mut self) {
        while self.peek().is_ascii_alphabetic() || self.peek() == '_' {
            self.advance();
        }

        let s = &self.source[self.start..self.current];
        if let Some(keyword) = get_keyword(s) {
            self.add_token(keyword);
        } else {
            self.add_token(TokenType::Identifier);
        }
    }

    pub fn scan_token(&mut self, ctx: &mut Context) {
        let c = self.advance();
        match c {
            '(' => self.add_token(TokenType::LeftParen),
            ')' => self.add_token(TokenType::RightParen),
            '{' => self.add_token(TokenType::LeftBrace),
            '}' => self.add_token(TokenType::RightBrace),
            ',' => self.add_token(TokenType::Comma),
            '.' => self.add_token(TokenType::Dot),
            '-' => self.add_token(TokenType::Minus),
            '+' => self.add_token(TokenType::Plus),
            ';' => self.add_token(TokenType::Semicolon),
            '*' => self.add_token(TokenType::Star),
            '!' if self.match_char('=') => self.add_token(TokenType::BangEqual),
            '!' => self.add_token(TokenType::Bang),
            '=' if self.match_char('=') => self.add_token(TokenType::EqualEqual),
            '=' => self.add_token(TokenType::Equal),
            '<' if self.match_char('<') => self.add_token(TokenType::LessEqual),
            '<' => self.add_token(TokenType::Less),
            '>' if self.match_char('>') => self.add_token(TokenType::GreaterEqual),
            '>' => self.add_token(TokenType::Greater),
            '/' if self.match_char('/') => {
                while self.peek() != '\n' && !self.is_at_end() {
                    self.advance();
                }
            },
            '"' => self.string(ctx),
            '/' => self.add_token(TokenType::Slash),
            ' ' | '\r' | '\t' => (),
            '\n' => self.line += 1,
            _ if c.is_digit(10) => self.number(ctx),
            _ if c.is_ascii_alphabetic() || c == '_' => self.identifier(),
            _ => errors::error(ctx, self.line, "Unexpected character"),
        }
    }
}
