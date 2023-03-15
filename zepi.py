#!/usr/bin/env python3

def is_numeric(ch): return ch in set("0123456789")
def is_letter(ch): return ch in set("abcdefghijklmnopqrstuvwxyz")
def is_symbolic(ch): return ch in set("+-*/")

def is_numeric_or_letter(ch): return is_numeric(ch) or is_letter(ch)
def is_letter_or_symbolic(ch): return is_letter(ch) or is_symbolic(ch)
def is_numeric_or_letter_or_symbolic(ch): return is_numeric(ch) or is_letter(ch) or is_symbolic(ch)

def is_whitespace(ch): return ch == ' '
def is_open_paren(ch): return ch == '('
def is_close_paren(ch): return ch == ')'

class TokenizeFailed(Exception):
    def __str__(self):
        return "Tokenize failed: " + super().__str__()

class MagicFailed(Exception):
    def __str__(self):
        return "Magic failed: " + super().__str__()

def read_num(s):
    if not is_numeric(s[0]):
        raise TokenizeFailed(f"Invalid number: {s}")

    i = 0
    while i < len(s):
        if not is_numeric(s[i]):
            break
        i = i + 1
    return (int(s[:i]), s[i:])

class Symbol(str):
    pass

def read_symbol(s):
    if not is_letter_or_symbolic(s[0]):
        raise TokenizeFailed(f"Invalid symbol: {s}")

    i = 0
    while i < len(s):
        if not is_numeric_or_letter_or_symbolic(s[i]):
            break
        i = i + 1

    return (Symbol(s[:i]), s[i:])

def read_one(s):
    """
    > read_one("123 456 789")
    (123, ' 456 789')

    > read_one("(123 456) 789")
    ([123, 456], ' 789')
    """
    i = 0
    while i < len(s) and is_whitespace(s[i]):
        i = i + 1

    if i == len(s):
        return None, ""

    if is_numeric(s[i]):
        return read_num(s[i:])

    if is_letter(s[i]):
        return read_symbol(s[i:])

    if is_open_paren(s[i]):
        return read_list(s[i+1:])

    raise TokenizeFailed(f"Cannot tokenize character: {s[i]}")

class L(list):
    def __init__(self, *items):
        super(L, self).__init__(items)

    def __repr__(self):
        # Option with commas:
        #
        #     return "L(" + super().__repr__()[1:-1] + ")"
        return "(" + " ".join(repr(x) for x in self) + ")"

    pass

def print_every_list_like_in_clojure():

    def repr_space(items):
        return "(" + " ".join(repr(x) for x in items) + ")"

    list.__repr__ = repr_space

    pass

def read_list(s):
    """
    > read_list("123 456)")
    ([123, 456], '')
    """
    tokens = L()

    while s != "" and s[0] != ')':
        token, s = read_one(s)
        if token == None:
            raise TokenizeFailed("Unbalanced parens")
        tokens.append(token)

    if s == "" or s[0] != ')':
        raise ValueError("Unbalanced parens")

    return tokens, s[1:]

def read_all(s):
    """
    > read_all("123 3455     ")
    [123, 3455]
    """
    tokens = []

    while s != "":
        token, s = read_one(s)
        if token == None:
            break
        tokens.append(token)

def rep(magic):
    try:
        s = input("> ")
    except EOFError:
        print()
        return "BREAK"
    except KeyboardInterrupt:
        print()
        return "BREAK"
    else:
        if s[0] == "!":
            # we're gonna try magic
            try:
                magic_command = s.split()[0]
                magic[magic_command](s)
            except MagicFailed as e:
                print(e)
        else:
            try:
                token, _ = read_one(s)
                print(token)
            except TokenizeFailed as e:
                print(e)

def repl(magic=None):
    if not magic:
        magic = {}
    while True:
        r = rep(magic)
        if r == "BREAK":
            break

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == "repl":
        repl()
