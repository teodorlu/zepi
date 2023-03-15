# Zepi

    $ python zepi.py repl
    > (+ 1 2 (* 3 4))
    15

Roam notes: https://roamresearch.com/#/app/teod/page/nPPgnPW04

## Motivation

If we don't know the past, we'll repeat it. If we don't know our foundations, we'll remake them.

So, let's make a little language and see how that feels.

**Q: I want a good Python-based lisp, what should I look at?**

http://hylang.org/

**Q: Why Zepi?**

Because I like maing my own tools, and a programming language is an interesting challenge!

## How to run zepi

The most straightforward way is with the `repl` subcommand:

    python zepi.py repl

If you want gnu-style help with line editing, and command history, wrap it with
[rlwrap]:

[rlwrap]: https://github.com/hanslub42/rlwrap

    rlwrap python zepi.py repl

`rlwrap` provides things you might already be expecting:

1. Use arrow left and arrow right to move the cursor to edit text
2. Use arrow up to select the last command
3. Use `ctrl+R` to search in previously entered commands

If you want readline editing and self-reloading, use the `./repl` shell wrapper:

    ./repl

This puts you into a special zepi REPL that can also reload the zepi interpreter.
To reload the zepi interpreter, use the `!zreload` magic command:

    > !zreload

This is how I develop zepi :)
