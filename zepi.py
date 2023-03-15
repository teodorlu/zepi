#!/usr/bin/env python3

# we'll allow these dependencies because we're not cavemen :)
import functools
import operator

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

class EvalFailed(Exception):
    def __str__(self):
        return "Eval failed: " + super().__str__()

class Integer(int):
    def eval(self):
        return self

def read_num(s):
    if not is_numeric(s[0]):
        raise TokenizeFailed(f"Invalid number: {s}")

    i = 0
    while i < len(s):
        if not is_numeric(s[i]):
            break
        i = i + 1
    return (Integer(int(s[:i])), s[i:])

class Symbol(str):
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return "Symbol(" + super().__repr__() + ")"

    def __str__(self):
        return super().__str__()

    def eval(self):
        if self.s == "*":
            return Fn.varargs_fn(operator.mul, 1)
        elif self.s == "+":
            return Fn.varargs_fn(operator.add, 0)
        elif self.s == "/":
            def divide(*args):
                if len(args) != 2:
                    raise EvalFailed(f"/ takes 2 arguments, got {len(args)}")
                return args[0]/args[1]
            return Fn(divide) # varargs / is kinda weird, avoid it

        raise EvalFailed(f"Unbound symbol: {self.s}")

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

    if is_letter_or_symbolic(s[i]):
        return read_symbol(s[i:])

    if is_open_paren(s[i]):
        return read_list(s[i+1:])

    raise TokenizeFailed(f"No tokenizer found for character: {s[i]}")

class L(list):
    def __init__(self, *items):
        # self.items = items
        # print("ITEMS: ", repr(items))
        super(L, self).__init__(items)

    def __repr__(self):
        return "(" + " ".join(repr(x) for x in self) + ")"

    def __str__(self):
        return "(" + " ".join(str(x) for x in self) + ")"

    def eval(self):
        items = [x for x in self]
        if len(items) == 0:
            return L()
        else:
            f = items[0].eval()
            args = [i.eval() for i in items [1:]]
            return f.apply(args)

    pass

class Fn:
    def __init__(self, f):
        self.f = f

    def apply(self, args):
        return self.f(*args)

    @staticmethod
    def varargs_fn(function, initial):
        def varags(*args):
            return functools.reduce(function, args, initial)
        return Fn(varags)


# def apply(fn, args):

#     def apply(self, args):
#         if self.s == "*":
#             return functools.reduce(operator.mul, args, 1)

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

def read_all_NOT_IN_USE(s):
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
            # let's try magic
            try:
                magic_command = s.split()[0]
                magic[magic_command](s)
            except MagicFailed as e:
                print(e)
        else:
            try:
                token, _ = read_one(s)
                print("token: ", token)
                evaled = token.eval()
                print("evaled: ", evaled)
            except TokenizeFailed as e:
                print(e)
            except EvalFailed as e:
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
