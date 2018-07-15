ATS2 lexical units
==============================================================================

In this document, "?" means optional, "*" means zero or more, "+" means one or
more, "|" means an alternative. They appear without quotes. Parentheses —
outside of quotes — are used for grouping.

Each section comes with examples.

This document is based on the low level “lexemes-ref.md”.


Characters (literal)
------------------------------------------------------------------------------

A character literal is an escape or unescaped character (except the single
quote) enclosed in single quotes.

Postiats is not Unicode aware, so characters whose code is greater than
255 cannot be represented with this construct (it would be seen as an
unclosed character literal, because the character would be multi‑bytes).

An escaped character may be a symbolic character or a character code. A
character code may be octal or hexadecimal.

  * "'" `CHAR` "'"
  * "'" \\ `X` `HEX`+ "'"
  * "'" \\ `OCT`+ "'"
  * "'" \\ `SPECIAL` "'"

Where:

  * `CHAR` is any 8 bits characters except the single quote.
  * `HEX`+ is one or more of "0" to "9" and "A" to "F", case insensitive.
  * `OCT`+ is one or more of "0" to "7".
  * `X` is "x", case insensitive.
  * `SPECIAL` is one of ntvbrfa\\?'"([{

Where:

  * \\a is ASCII 7, bell.
  * \\b is ASCII 8, backspace.
  * \\f is ASCII 12, line‑feed.
  * \\n is ASCII 10, new‑line.
  * \\r is ASCII 13, carriage‑return.
  * \\t is ASCII 9, horizontal tab.
  * \\v is ASCII 11, vertical tab.
  * \\?'"()[]{} stands for their‑own.

Any of ([{ needs to be escaped because these characters preceded by a single
quote, has a special meaning in ATS2 (not required in string literals, while
still valid). The single quote needs to be escaped because it delimits
character literals, similarly the double quote in string literals. When there
is no need to escape these, it is not required to be escaped. The others need
to be escaped for readability. Using another symbol than those, is invalid.
Ex. '\\h' is not valid and is not 'h'.

Character codes allow to cover more than the above. There is no limit for the
number of digits, unlike with string literals. Also note if a code is bigger
than 255, it is silently truncated to 8 bits, without a warning or error
from Postiats.

Note unlike with integers, an hexadecimal character code does not have a zero
before the x and an octal character code is octal even if it does not starts
with a zero. There is no decimal character code.

Remember ex. 'è' is not valid, as it’s a multi‑bytes character. It is **not**
the same with string literals where if a source file is UTF‑8 encoded, then
the string literal is implicitly UTF‑8 encoded too. Hence, "è" is valid and is
a two bytes string literal.

It is not illegal for character literal to contain the end of line, although
this may be erroneous depending on the end of line convention a source file is
saved with (on Windows, the end of line is made of two characters). This is
pathological and should be avoided.

**Examples:**

        // All represent the same character, a double quote.
        val c = '\"'
        val c = '"'
        val c = "\x22"
        val c = "\42"


Comments
------------------------------------------------------------------------------

Comments come in four flavors.

  * C++ line comments: starts with a "//" and ends with the end of the line.
  * C/C++ block comments: starts with a "/\*" and ends with a closing "\*/".
  * ML block comments: starts with a "(\*" and ends with a closing "\*)",
    recursively, unlike with C/C++ block comments.
  * ATS2 rest comment: starts with a "////" and ends with the end of the file.

Comments are ignored but are not like blanks.

"////" is like a forced EOF.

**Examples:**

        static fun my_fun( (*void*) ): int // With an ML comment.
        static fun my_fun2( /*void*/ ): int // With a C++ comment.
        (* foo (* bar *) recursive ML comment *)
        //// Anything ignored up to end of file.
        !!!! ?????? ....... ,,,,,, real EOF comes here.


External code (embedded foreign language)
------------------------------------------------------------------------------

An embedded foreign language block is opened always at the beginning of a line
and closed at the beginning of a later line, too. Its embedding position may
be optionally specified, relative to the generated target language. The
foreign language is expected to be the same as the target language, although
no rule enforces it.

  * Open: "%{" `POSITION`? `OFFSET`?
  * Close: "%}"

Where:

  * `POSITION` is either "#" or "^" or "$" or nothing.
  * `OFSSET` is "2", the only allowed value.

Positions meaning with offset:

  * "#": unspecified (used from statics).
  * "^": at the beginning.
  * "^2": right after blocks with "^".
  * "$": at the end.
  * "$2": right before blocks with "$".
  * Nothing or any other character: in the middle.

The offset may be specified only with "^" or "$". Beginning, middle and end
refers to the target language generated file.

"#" is to be used in statics files ("\*.sats" files) for embedding in dynamics
files (\*.dats files) which `staload` it (*staload* is an ATS2 keyword). This
embedding is at an unspecified position.

**Examples:**

        %{^
        #include <stdio.h>
        %}

        %{^2
        #include "./my-include.h"
        %}

        %{#
        // Will be embedded in any DATS file staloading this file.
        void f (void) { }
        %}

        %{$
        /* Some epilogue */
        %}


Floats
------------------------------------------------------------------------------

Floats come in two bases, sharing a common suffix, and with an exponent part
which is always decimal whatever the base. Unlike with integers, there is no
octal floats.

Using hexadecimal floats may improve precision, since the binary
representation of a decimal float may be not exact. Although less readable,
float constants are better specified in hexadecimal than decimal.

Floats are made of an integral part, a fractional part and an exponent part.
Both former are optional with the **requirement at least one is provided**.
With hexadecimal float, the exponent part is required, after the C language
standard. With decimal floats, the exponent part is optional.

  * Decimal: `DEC`* ("." `DEC`*)? (`E` `SIGN` `DEC`+)? `FL`?
  * Hexadecimal: "0" `X` `HEX`* ("." `HEX`*)? `P` `SIGN` `DEC`+ `FL`?

Where:

  * `DEC`* is zero or more of "0" to "9".
  * `HEX`* is zero or more of "0" to "9" and "A" to "F", case insensitive.
  * `SIGN` is "+" or "-" or nothing, "+" is the default.
  * `FL`? is an optional "F" or "L", case insensitive, none is the default.
  * `E` is "E", case insensitive.
  * `P` is "P", case insensitive.
  * `X` is "x", case insensitive.

Suffix meaning:

  * "F": `float` type.
  * "L": `ldouble` type.
  * No suffix: `double` type.

Floats are distinguished from integers by either the "." of the fractional
part or the "P" or "E" of the exponent part or both. Note it’s "P" for
hexadecimal floats ("E" would be an hexadecimal digit).

The `X` is not repeated for the fractional part of hexadecimal float, it only
appears for the integral part, even if it’s empty (ex. "0x.1P0" where the
integral part is empty but "x" is still there).

If a decimal float is preceded by at least one space and its integer part is
zero, it is allowed to omit it, although it is better avoided, to avoid visual
confusion with integer record selectors. **If it’s not** preceded by a space,
then it is not a float, it’s a dot integer identifier, that is, a field
selector where the label is an integer, as always with tuples and as sometimes
with records.

**Examples:**

        val v = 0.0
        val v = 1.0
        val v = 0. // 0.0
        val v = 1. // 1.0
        val v = .1 // 0.1
        val v:float = 1.0f // Without the "F" suffix, it does not type‑check.
        val v:ldouble = 1.0l // Without the "L" suffix, it does not type‑check.
        val v:double = 1.0 // With any suffix, it does not type‑check.
        val v = 0xF.1P0 // 15 + 1/16.
        val v = 15.0625 // 15 + 1/16.
        val t = @('a', 'b', 'c', 'd') // Prerequisite for next line.
        val v = t.2 // Not a float, a dot integer identifier.


Identifiers
------------------------------------------------------------------------------

This is the longest section of this document and is sub‑divided in
sub‑sections.


### General identifiers format

Identifiers come in two main flavors with subtleties and additional derived
kinds. The two main flavors are alphanumeric identifiers and symbolic
identifiers. The subtleties are with symbolic identifiers: some prefix of it
will be identifiers on their own, leaving the rest alone. The derived kinds
are with alphanumeric identifiers with a "[" or "<" or "!" appended or a "$"
or a "#" prepended. Then, there are the identifiers like alphanumeric with an
added at‑sign in the middle.

  * Alphanumeric identifier: `FIRST` `REST`*
  * Symbolic identifier: "$"? `SYMBOLIC`+ | "$"

Where:

  * `FIRST` is "a" to "z" or "A" to "Z" or "_", case **sensitive**.
  * `REST`* is zero or more of `FIRST` or "0" to "9" or "'" or "$".
  * `SYMBOLIC`+ is one or more of %&+-./:=@~\`^|\*!?<># .

"$" is not a `SYMBOLIC` character, but a symbolic identifier may starts with
it or it may be a symbolic identifier alone.

Use of symbolic identifiers is more restricted than use of alphanumeric
identifiers.

Symbolic identifiers can contain the characters which open and close C/C++
like comments. If it starts with "//" or "/\*", it opens a comment; if
contains "//" or "/\*" and does not start with it, it does not open a comment.
This should be used with care to not prevent readability.

Later, alphanumeric identifiers will be referred to as `ALNUM` and
symbolic identifiers will be referred to as `SYMBOL` (to not be confused with
`SYMBOLIC` characters).

Some identifiers are keywords, built‑ins or special in some other ways, this
is the subject of other documents and is not covered here. What matters here,
is how identifiers are extracted from a source.

Additional restrictions are explained in later sub‑sections.

**Examples:**

        extern val foo: int
        extern val foo1a: int
        extern val foo$1a: int // Note the dollar sign in the middle.
        extern val foo_1a: int
        //
        symintr ++
        symintr $*
        symintr -//       // Valid, but may be avoided.
        symintr -/*       // Valid, but may be avoided.


### Regular decorated alphanumeric identifiers

Additionally to `ALNUM`, are the ones of the kinds below:

  * "$" `ALNUM`
  * "#" `ALNUM`
  * "\\" `ALNUM` — there may be spaces between "\\" and `ALNUM`.
  * `ALNUM` "<"
  * `ALNUM` "["
  * `ALNUM` "!"

"\\" `ALNUM` is not really a lexical unit, it is rather parsed from lexical
units but you can see it as a lexical unit.

These kinds cannot be created by the user; all valid identifiers of these
kinds, are predefined and not listed in this document:

  * "$" `ALNUM`
  * "#" `ALNUM`
  * `ALNUM` "!"


### Irregular decorated alphanumeric identifiers

Beside `ALNUM`, some decorated `ALNUM` are seen as‑is whatever follows it but
not whatever precedes it. These decorated `ALNUM` cannot be created by the
user, they belong to a fixed set:

  * abst@ype
  * absviewt@ype
  * absvt@ype
  * addr@
  * case-
  * case+
  * fix@
  * fold@
  * for*
  * free@
  * lam@
  * llam@
  * prop-
  * prop+
  * t0ype-
  * t0ype+
  * t@ype
  * t@ype-
  * t@ype+
  * type-
  * type+
  * val-
  * val+
  * view-
  * view@
  * view+
  * viewt0ype-
  * viewt0ype+
  * viewt@ype
  * viewt@ype-
  * viewt@ype+
  * viewtype-
  * viewtype+
  * vt0ype-
  * vt0ype+
  * vt@ype
  * vt@ype-
  * vt@ype+
  * vtype-
  * vtype+
  * while*

Whatever follows, it’s the same. Ex. "abst@ype0" will be parsed as "abst@ype"
and "0", it is still "abst@ype". The same with another example like "val+",
"val+a" will be parsed as "val+" and "a".

This is not whatever precedes, however. Ex. "zabst@ype" will be parsed as
"zabst" and "@" and "ype", but "0abst@ype" will be parsed as "0" and
"abst@ype". This is because "zabst" forms a valid `ALNUM` and "0abst" don’t.

These identifiers are recognizable by the symbolic character they contains.
It’s this way only these. Ex. "foo@bar" will be parsed as "foo" and "@" and
"bar", because "foo@bar" does not belong to this list. Similarly, "foo+" will
be parsed as "foo" and "+", because of the same reason.


### Reserved symbolic identifiers

Beside `SYMBOL`, some `SYMBOL` has a fixed meaning in ATS2. These `SYMBOL`
cannot be redefined by the user, they belong to a fixed set:

  * \`
  * ~
  * <
  * =
  * =<
  * =<>
  * =>
  * =>>
  * =/=>
  * =/=>>
  * \>
  * \><
  * \>.
  * |
  * -<
  * -<>
  * ->
  * :
  * :<
  * !
  * ?
  * .
  * .<
  * .<>.
  * ..
  * ...
  * @
  * $
  * \#
  * %

See also the sections “Other tokens” and “Exceptions”.


### Dot integer identifier

A dot identifier is made of a dot, not preceded by a space and followed by
a decimal digits sequence. It designate a member of a tuple or also possibly
a member of a record.

**Example:**

        val t = @('a', 'b', 'c', 'd') // Prerequisite for the example.
        val v = t.2 // Dot integer identifier.


Integers
------------------------------------------------------------------------------

Integers come in three bases which shares a common suffix.

  * Octal: "0" `OCT`+ `LU`?
  * Decimal: `DEC`+ `LU`?
  * Hexadecimal: "0" `X` `HEX`+ `LU`?
  * Zero: "0"

Where:

  * `OCT`+ is one or more of "0" to "7".
  * `DEC`+ is one or more of "0" to "9".
  * `HEX`+ is one or more of "0" to "9" and "A" to "F", case insensitive.
  * `LU`? is an optional "L" or "U", case insensitive.
  * `X` is "x", case insensitive.

The "L" and "U" suffixes mean the same as in the C language.

There is no binary integers.

**Examples:**

        // All represent the same value.
        val v = 0377
        val v = 0xFF
        val v = 255


Strings
------------------------------------------------------------------------------

A string literal is very close to a character literal, detailed in a section
you can jump to later. The differences are:

  * Hexadecimal codes are limited to two digits: characters beyond are
    characters on their own. Similarly with octal codes which are limited to
    three digits.
  * A string literal is opened and closed with a double quote.
  * You don’t have to mind if a string contains a multi‑bytes character,
    although you may have to mind about the string encoding which will be the
    same as that of the source file.
  * In addition to the escaped sequence of character literals, within a string
    literal, the end of line can be escaped (with a back‑slash), which removes
    it from the string content.

Note within string literals spanning multiple lines, comments are not parsed,
they are just character data as any other. This is so, obviously, up to the
closing double‑quote.

**Examples:**

        val s = "Ça fait du café" // With two multi‑bytes characters.
        val s = "abc\ndef" // "abc\ndef", whatever the EOL convention.
        val s = "abc
        def" // "abc\ndef" on *NIX or "abc\r\ndef" on Windows.
        val s = "abc\
        def" // "abcdef".

Other tokens
------------------------------------------------------------------------------

These ones are always parsed as‑is, whatever follows but not always whatever
precedes:

  * \`(
  * ,
  * ,(
  * ;
  * '(
  * '[
  * '{
  * (
  * )
  * [
  * ]
  * {
  * }
  * @(
  * @[
  * @{
  * \\
  * #[
  * %(

The longest matches first.

For the tokens of this list starting with "@", "#", "%" and "\`": these tokens
will not be parsed as this if they are preceded (without blanks) by a symbolic
identifier. For the tokens of this list starting with a "'", there will not be
parsed as this if they are preceded (without blanks) by an alphanumeric
identifier.


Exceptions
------------------------------------------------------------------------------

These, which match some non‑identifier lexical units, **may** also be used in
place of alphanumeric identifiers (they are ambiguous lexical units):

  * ~
  * <
  * =
  * \>
  * \><
  * ->
  * !
  * ?
  * @
  * \\
  * %
  * addr
  * fold
  * free
  * prop
  * type
  * view
  * viewtype
  * vtype


Error conditions
------------------------------------------------------------------------------

  * A C‑like block comment must be closed.
  * An ML‑like block comment must be closed.
  * An external code block must be closed.
  * A character literal must be closed.
  * A string literal must be closed.
  * An escaped character must be one of the predefined.
  * A float cannot have both its integral and fractional parts empty.
  * A float exponent — if present or required — must not be empty.
  * An hexadecimal float has a required exponent.
  * An hexadecimal cannot have an empty hexadecimal digits string.

