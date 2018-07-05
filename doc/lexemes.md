Postiats lexical rules
==============================================================================

Before anything
------------------------------------------------------------------------------

The rules described here, are hoped to be exact. But **it is not required to
know it exactly to be able to use Postiats**. This document is provided to be
part of a reference documentation I always missed, and because it can be
useful for many kinds of applications dealing with Postiats source. If you
find an issue, feel free to tell about.

In the rules described, the order of the tests are relevant.

The input is handled as a bytes sequence, not as Unicode. Similarly with the
text lexical literals: if a source file is UTF‑8 encoded, then the string
literals in it will also be. This is not necessarily an issue, this may even
be convenient. This may be an issue only when computing string lengths. Don’t
mind, it’s a good exercise to define an appropriate one in ATS2.

Comments do not count as a space and are not like zero width space neither.

A star sign indicates zero or more. A plus sign indicates one or more. The
notation “{m,n}” indicates *m* to *n* repetitions (any one in the range). A
question mark indicates an optional element, like if it was “{0,1}”. A “—”
introduces a comment.

The lexical rules presents some corner cases consequence which can be ignored
(see the first paragraph) while still may be worth to know for some people.

The rules here only document valid lexical units, not invalid ones. It is so
to avoid this document to be overly complicated and anyway, if a lexical unit
is wrong, it will very probably end in an error elsewhere, like with the
grammar, so this is not really silently ignoring errors.

The informations in this document are inferred from mainly `pats_lexing.sats`,
`pats_lexing.dats`, `pats_symbol.sats`, `pats_symbol.dats` and
`pats_lexing_token.dats`. The names are near to exactly the same as in
Postiats source, but not exactly.

The names starting with `T_` are that of terminal products (for lexemes, this
is not the grammar). The names no starting with `T_` take part in other
products up to a terminal product.


Character categories
------------------------------------------------------------------------------

  * `SPACE`: " " "\n" "\r" "\v" "\f" "\r".
  * `ESCAPED`: "n" "t" "v" "b" "r" "f" "a" "\\" "?" "'" '"' "(" "[" "{".
  * `XDIGIT`: "0" to "9", "a" to "f", "A" to "F".
  * `DIGIT`: "0" to "9".
  * `OCTAL`: "0" to "7".
  * `IC`: input character: any character, including EOL.
  * `IC_LQ`: any character, less quote (single‑quote).
  * `IC_LDQ`: any character, less double‑quote.
  * `IC_LEOL`: any character, less EOL.
  * `IDENTFST`: "a" to "z", "A" to "Z", "_"
  * `IDENTRST`: `IDENTFST` "0" to "9" "'" "$"
  * `SYMBOLIC`: " % & + - . / : = @ ~ \` ^ | * ! ? < > # " — less blanks.
  * `X`: "x" "X"
  * `P`: "p" "P"
  * `E`: "e" "E"
  * `SIGN`: "-" "+"
  * `FL`: "f" "F" "l" "L" — float suffix.
  * `LU`: "L" "l" "U" "u" — integer suffix.

Other caracters used (outise of comments and text literals), not alphanumeric
and neither in `SYMBOLIC`, are: "(" ")" "[" "]" "{" "}" "," ";".


Special handling of `IDENT_sym`
------------------------------------------------------------------------------

The products are listed later, but before going further, this one must be
introduced. `IDENT_sym` is a sequence of `SYMBOLIC`. Just after it is read
from input, it is tested to determine if it will be turned into something else
or not.

When it starts with a question mark which is followed by a greater‑than sign,
it is turned into a question mark; what follows the question mark remains
available for later input.

Else, if it starts with a slash, then it is tested for a comment and if it’s
a comment, the input which follows in `IDENT_sym` and after, is consumed
accordingly.

Otherwise, it’s an `IDENT_sym`.

To summarize:

  * `IDENT_sym`: `SYMBOLIC`*
  * If it starts with "?>" then parse "?".
  * If it starts with "/*" then parse a `COMMENT_block_c`.
  * If it starts with "////" then parse a `T_COMMENT_rest`.
  * If it starts with "//" then parse a `T_COMMENT_line`.

Where:

  * `COMMENT_block_c`: "/*" `IC`* "*/" — not recursive! (unlike ML comments)
  * `T_COMMENT_rest`: "////" `IC`* EOF — up to the end of the source file.
  * `T_COMMENT_line`: "//" `IC_LEOL`* EOL — up to the end of the line.


### Corner case

A **corner case** consequence of these rules may be exposed with this
example `IDENT_sym`: “$//”.

Say a DATS source contains this:

        val $// = 1

It looks like the statement is not terminated, broken by a comment. But it
is not, `$//` is the name of the introduced `val` and its value is `1`. Try to
check it, it will pass. Try to insert a space between “$” and “//”, it will
not pass.

That’s so because although this `IDENT_sym` contains “//”, it does not
start with it, so to Postiats, it’s not a comment, it’s a symbolic identifier.
Still note not all symbolic identifiers may be freely used anywhere and some
have a special meaning to Postiats. Possible Postiats parse errors will tell
you.


### Recommandation

After the above, it can be suggested to always have a space before a comment
which does not start with the current line.


Lexical productions
------------------------------------------------------------------------------

First skip `SPACE`*, but don’t forget it there was one (if there was), since
a product needs to know it. For two other products, it is needed to know if
the current location is at the start of the line. If there is spaces before,
this is not the start of the line.

Then, test these an parse the first which fully match, then resume skipping
space, testing, parse and so on iteratively.

As explained in “Note #1” later, some identifier are further tested. The test
is simpler than the one with `IDENT_sym`. Note when the identifier is an
`IDENT_sym`, then this comes an additional test.

Keep in mind the order matters.

**This list is not a list of the keywords!**


  * `COMMENT_block_ml`: "(*" `COMMENT_block_ml` "*)" — recursive.
  * `T_LPAREN`: "("
  * `T_RPAREN`: ")"
  * `T_LBRACKET`: "["
  * `T_RBRACKET`: "]"
  * `T_LBRACE`: "{"
  * `T_RBRACE`: "}"
  * `T_COMMALPAREN`: ",("
  * `T_COMMA`: ","
  * `T_SEMICOLON`: ";"
  * `T_ATLPAREN`: "@("
  * `T_ATLBRACKET`: "@["
  * `T_ATLBRACE`: "@{"
  * `T_IDENT_sym`: "@" `SYMBOLIC`* — see note #1.
  * `T_COLONLT`: ":<" — see note #2.
  * `T_IDENT_sym`: ":" `SYMBOLIC`* — see note #1.
  * `T_IDENT_sym`: "." `SYMBOLIC`+ — see note #1.
  * `T_FLOAT_dec`: `SPACE` "." `DIGIT`+ (`E` `SIGN`? `DIGIT`+)? `FL`? — see
    note #6.
  * `T_DOTINT`: "." `DIGIT`+
  * `T_IDENT_dlr`: "$" `IDENTFST` `IDENTRST`* — see note #1.
  * `T_IDENT_sym`: "$" `SYMBOLIC`* — see note #1.
  * `T_HASHLBRACKET`: "#["
  * `T_IDENT_srp`: "#" `IDENTFST` `IDENTRST`* — see note #1.
  * `T_IDENT_sym`: "#" `SYMBOLIC`* — see note #1.
  * `T_PERCENTLPAREN`: "%("
  * `T_EXTCODE`: SOL "%{" ("#" | "^" "2"? | "$" "2"?)? `IC`* SOL "%}"
  * `T_IDENT_sym`: "%" `SYMBOLIC`* — see note #1.
  * `T_QUOTELPAREN`: "'("
  * `T_QUOTELBRACKET`: "'["
  * `T_QUOTELBRACE`: "'{"
  * `T_CHAR`: "'\\" `ESCAPED` "'"
  * `T_CHAR`: "'\\" `X` `XDIGIT`+ "'"
  * `T_CHAR`: "'\\" `OCTAL`+ "'"
  * `T_CHAR`: "'" `IC_LQ` "'"
  * `T_STRING`: '"' ("\\" EOL|"\\" `ESCAPED`|"\\" `X` `XDIGIT`{1,2}|"\\"
    `OCTAL`{1,3}|`IC_LDQ`)* '"' — see note #4.
  * `T_BQUOTELPAREN`: "\`(" — macro syntax
  * `T_IDENT_sym`: "\`" `SYMBOLIC`* — see note #1.
  * `T_BACKSLASH`: "\\"
  * `T_IDENT_tmp`: `IDENTFST` `IDENTRST`* "<"
  * `T_IDENT_arr`: `IDENTFST` `IDENTRST`* "["
  * `T_IDENT_ext`: `IDENTFST` `IDENTRST`* "!"
  * `ABST0YPE`: "abst@ype" — see note #2.
  * `ABSVIEWT0YPE`: "absvt@ype" — see note #2.
  * `ABSVIEWT0YPE`: "absviewt@ype" — see note #2.
  * `CASE_pos`: "case+" — see note #2.
  * `CASE_neg`: "case-" — see note #2.
  * `CASE`: "case" — see note #7.
  * `PROP_pos`: "prop+" — see note #2.
  * `PROP_neg`: "prop-" — see note #2.
  * `PROP`: "prop" — see note #7.
  * `T0YPE_pos`: "t@ype+" — see note #2.
  * `T0YPE_neg`: "t@ype-" — see note #2.
  * `T0YPE`: "t@ype" — see note #2.
  * `TYPE_pos`: "type+" — see note #2.
  * `TYPE_neg`: "type-" — see note #2.
  * `TYPE`: "type" — see note #7.
  * `T0YPE_pos`: "t0ype+" — see note #2.
  * `T0YPE_neg`: "t0ype-" — see note #2.
  * `T9YPE`: "t0ype" — see note #7.
  * `VIEWT0YPE_pos`: "vt@ype+" — see note #2.
  * `VIEWT0YPE_neg`: "vt@ype-" — see note #2.
  * `VIEWT0YPE`: "vt@ype" — see note #2.
  * `VIEWT0YPE_pos`: "vtype+" — see note #2.
  * `VIEWT0YPE_neg`: "vtype-" — see note #2.
  * `VIEWT0YPE`: "vtype" — see note #7.
  * `VIEWT0YPE_pos`: "vt0ype+" — see note #2.
  * `VIEWT0YPE_neg`: "vt0ype-" — see note #2.
  * `VIEWT0YPE`: "vt0ype" — see note #7.
  * `T_VIEWAT`: "view@" — see note #2.
  * `VIEW_pos`: "view+" — see note #2.
  * `VIEW_neg`: "view-" — see note #2.
  * `VIEW`: "view" — see note #7.
  * `VIEWT0YPE_pos`: "viewt@ype+" — see note #2.
  * `VIEWT0YPE_neg`: "viewt@ype-" — see note #2.
  * `VIEWT0YPE`: "viewt@ype" — see note #2.
  * `VIEWTYPE_pos`: "viewtype+" — see note #2.
  * `VIEWTYPE_neg`: "viewtype-" — see note #2.
  * `VIEWTYPE`: "viewtype" — see note #7.
  * `VIEWT0YPE_pos`: "viewt0ype+" — see note #2.
  * `VIEWT0YPE_neg`: "viewt0ype-" — see note #2.
  * `VIEWT0YPE`: "viewt0ype" — see note #7.
  * `VAL_pos`: "val+" — see note #2.
  * `VAL_neg`: "val-" — see note #2.
  * `VAL`: "val" — see note #7.
  * `T_FORSTAR`: "for*" — see note #2.
  * `T_FOR`: "for" — see note #7.
  * `T_WHILESTAR`: "while*" — see note #2.
  * `T_WHILE`: "while" — see note #7.
  * `T_ADDRAT`: "addr@" — see note #2.
  * `T_ADDR`: "addr" — see note #7.
  * `T_FOLDAT`: "fold@" — see note #2.
  * `T_FOLD`: "fold" — see note #7.
  * `T_FREEAT`: "free@" — see note #2.
  * `T_FREE`: "free" — see note #7.
  * `LAMAT`: "lam@" — see note #2.
  * `LAM`: "lam" — see note #7.
  * `LLAMAT`: "llam@" — see note #2.
  * `LLAM`: "llam" — see note #7.
  * `FIXAT`: "fix@" — see note #2.
  * `FIX`: "fix" — see note #7.
  * `T_IDENT_alp`: `IDENTFST` `IDENTRST`* — see note #1.
  * `T_IDENT_sym`: `SYMBOLIC`+: — see note #1.
  * `T_FLOAT_hex`: "0" `X` `XDIGIT`* "." `XDIGIT`* (`P` `SIGN`? `DIGIT`+)?
     `FL`? — see note #3.
  * `T_FLOAT_hex`: "0" `X` `P` `SIGN`? `DIGIT`+ `FL`? — see note #3.
  * `T_INT_hex`: "0" `X` `XDIGIT`* `LU`? — see note #3.
  * `T_INT_oct`: "0" `OCTAL`+ `LU`?
  * `T_FLOAT_dec`: "0" "." `DIDIT`* (`E` `SIGN`? `DIGIT`+)? `FL`? — see
    note #3 and note #5.
  * `T_FLOAT_dec`: "0" `E` `SIGN`? `DIGIT`+ `FL`? — see note #5.
  * `T_INTZERO`: "0"
  * `T_FLOAT_dec`: `DIGIT`+ "." `DIDIT`* (`E` `SIGN`? `DIGIT`+)? `FL`? — see
    note #3.
  * `T_FLOAT_dec`: `DIGIT`+ `E` `SIGN`? `DIGIT`+ `FL`?
  * `T_INT_dec`: `DIGIT`+
  * `T_EOF`: EOF
  * `T_ERR`: `IC` — any character which matched nothing.


### Note #1

if the identifier belongs to a predefined symbol table defined later,
then it is turned into the production after that table. Ex. if an
`IDENT_sym` is “->” then is will be turned into `T_MINUSGT` (introduced
later in this document) which has a special meaning


### Note #2

This is so, whatever follows.

Three examples to have in mind:

  * `case+foo` will be parsed as `case+` and `foo`.
  * `viewt@ypefoo` will be parsed as `viewt@ype` and `foo`.
  * `:<>` will be parsed as `:<` and `>`

The first and even more the second kind of case, are **corner case** worth to
know.

On the contrary, `viewtypefoo` or `viewt0ypefoo` will be parsed as a single
identifier.


### Note #3

With numeric literals, some parts may be empty. You may prefer to not make
use of it, but it is worth to know it’s intended and you should not be
surprised Postiats does not complain with these.

Ex. `0x.` is a valid hexadecimal floating point number, although its integer
and fractional parts are both empty. It’s evaluated as if it was `0x0.0`.
The empty parts are evaluated to zero.


### Note #4

Extraneous digits in a character code, are treated as characters in the
string. Ex. `"\xABC"` is a string made of the character whose code is
`0xAB` and the character “C”. Similarly with octal character code, except
if beyond three character, not two. There is not decimal character code, it’s
either hexadecimal or octal.


### Note #5

Decimal: there is no octal floating point.


### Note #6

There must be a space before the dot. Two examples to have in mind:

  * `foo .123` will be parsed as the identifier `foo` and the float `0.123`.
  * `foo.123` will be parsed as the identifier `foo` and the dot‑identifier
    `.123`.


### Note #7

Not followed by an `IDENTRST`. Ex. `viewtypefoo` or `viewt0ypefoo` will be
parsed as a single identifier, not as `viewtype` or `viewt0ype` and `foo`.


Predefined symbols
------------------------------------------------------------------------------

These symbols are predefined and tested as explained in “Note #1” in the
previous section. The comments were extracted as‑is from `pats_lexing.sats`
and some other files.

Note with some tokens, there is a correspondence with multiple strings.
Ex. `T_DLRARRPSZ` which may be parsed from "$arrpsz" or "$arrptrsize": these
are **synonymous**.

Some productions defined in this list, are also defined in the previous
list, ex. `ABST0YPE`. Rules are added, this is not contradictory.

**This list is not a list of the keywords!**

The list is split in two, after the prefix, but it’s in the same table.

Here, order does not matter.

List for terminal products:

  * `T_AND`: "and"
  * `T_AS`: "as" — for refas-pattern
  * `T_ASSUME`: "assume", "absimpl" — for implementing abstypes
  * `T_AT`: "@"
  * `T_BANG`: "!"
  * `T_BAR`: "|"
  * `T_BEGIN`: "begin" — initiating a sequence
  * `T_BQUOTE`: "`"
  * `T_CLASSDEC`: "classdec"
  * `T_COLON`: ":"
  * `T_DATASORT`: "datasort"
  * `T_DLRARRPSZ`: "$arrpsz", "$arrptrsize"
  * `T_DLRBREAK`: "$break"
  * `T_DLRCONTINUE`: "$continue"
  * `T_DLRD2CTYPE`: "$d2ctype" — $d2ctype(foo/foo<...>)
  * `T_DLREFFMASK`: "$effmask"
  * `T_DLREXTERN`: "$extern"
  * `T_DLREXTFCALL`: "$extfcall" — externally named fun-call
  * `T_DLREXTKIND`: "$extkind"
  * `T_DLREXTMCALL`: "$extmcall" — externally named method-call
  * `T_DLREXTVAL`: "$extval" — externally named value
  * `T_DLREXTYPE`: "$extype" — externally named type
  * `T_DLREXTYPE_STRUCT`: "$extype_struct" — externally named struct
  * `T_DLRLITERAL`: "$literal"
  * `T_DLRMYFILENAME`: "$myfilename"
  * `T_DLRMYFUNCTION`: "$myfunction"
  * `T_DLRMYLOCATION`: "$mylocation"
  * `T_DLRRAISE`: "$raise" — raising exceptions
  * `T_DLRSHOWTYPE`: "$showtype" — for debugging purpose
  * `T_DLRSOLASSERT`: "$solver_assert" — assert(d2e_prf)
  * `T_DLRSOLVERIFY`: "$solver_verify" — verify(s2e_prop)
  * `T_DLRTEMPENVER`: "$tempenver" — for adding environvar
  * `T_DLRTYREP`: "$tyrep" — $tyrep(SomeType)
  * `T_DLRVARARG`: "$vararg" — variadicity support
  * `T_DO`: "do"
  * `T_DOLLAR`: "$"
  * `T_DOT`: "."
  * `T_DOTDOT`: ".."
  * `T_DOTDOTDOT`: "..."
  * `T_DOTLTGTDOT`: ".<>." — for empty termetric
  * `T_DOTLT`: ".<" — opening termetric
  * `T_ELSE`: "else"
  * `T_END`: "end"
  * `T_EQ`: "="
  * `T_EQGT`: "=>"
  * `T_EQGTGT`: "=>>"
  * `T_EQLT`: "=<"
  * `T_EQLTGT`: "=<>"
  * `T_EQSLASHEQGT`: "=/=>"
  * `T_EQSLASHEQGTGT`: "=/=>>"
  * `T_EXCEPTION`: "exception"
  * `T_EXTERN`: "extern"
  * `T_EXTVAR`: "extvar" — externally named variable
  * `T_EXTYPE`: "extype" — externally named type
  * `T_GTDOT`: ">." — closing termetric
  * `T_GT`: ">" — for closing a tmparg
  * `T_GTLT`: "><"
  * `T_HASH`: "#"
  * `T_IFCASE`: "ifcase" — (dynamic) ifcase
  * `T_IF`: "if" — (dynamic) if
  * `T_IMPORT`: "import" — for importing packages
  * `T_IN`: "in"
  * `T_LET`: "let"
  * `T_LOCAL`: "local"
  * `T_LT`: "<" — for opening a tmparg
  * `T_MINUSGT`: "->"
  * `T_MINUSLT`: "-<"
  * `T_MINUSLTGT`: "-<>"
  * `T_NONFIX`: "nonfix"
  * `T_OF`: "of"
  * `T_OP`: "op" — HX: taken from ML
  * `T_OVERLOAD`: "overload"
  * `T_PERCENT`: "%"
  * `T_QMARK`: "?"
  * `T_REASSUME`: "reassume", "absreimpl" — for re-assuming abstypes
  * `T_REC`: "rec"
  * `T_SCASE`: "scase" — static case
  * `T_SIF`: "sif" — static if
  * `T_SORTDEF`: "sortdef"
  * `T_SRPASSERT`: "#assert"
  * `T_SRPCODEGEN2`: "#codegen2" — for level-2 codegen
  * `T_SRPCODEGEN3`: "#codegen3" — for level-3 codegen
  * `T_SRPDEFINE`: "#define"
  * `T_SRPDYNLOAD`: "dynload", "#dynload"
  * `T_SRPELIFDEF`: "#elifdef"
  * `T_SRPELIF`: "#elif"
  * `T_SRPELIFNDEF`: "#elifndef"
  * `T_SRPELSE`: "#else"
  * `T_SRPENDIF`: "#endif"
  * `T_SRPERROR`: "#error"
  * `T_SRPIFDEF`: "#ifdef"
  * `T_SRPIF`: "#if"
  * `T_SRPIFNDEF`: "#ifndef"
  * `T_SRPINCLUDE`: "#include"
  * `T_SRPPRAGMA`: "#pragma" — general pragma
  * `T_SRPPRERR`: "#prerr" — outpui to stderr
  * `T_SRPPRINT`: "#print" — output to stdout
  * `T_SRPREQUIRE`: "#require"
  * `T_SRPSTALOAD`: "staload", "#staload"
  * `T_SRPTHEN`: "#then"
  * `T_SRPUNDEF`: "#undef"
  * `T_STACST`: "sta", "stacst"
  * `T_STADEF`: "stadef"
  * `T_STATIC`: "static"
  * `T_SYMELIM`: "symelim" — symbol elimination
  * `T_SYMINTR`: "symintr" — symbol introduction
  * `T_THEN`: "then"
  * `T_TILDE`: "~" — often for 'not', 'free', etc.
  * `T_TKINDEF`: "tkindef" — for introducting tkinds
  * `T_TRY`: "try"
  * `T_WHEN`: "when"
  * `T_WHERE`: "where"
  * `T_WITH`: "with"


List for non‑terminal products:

  * `ABSPROP`: "absprop"
  * `ABST0YPE`: "abst0ype", "abstflat"
  * `ABSTYPE`: "abstbox", "abstype"
  * `ABSVIEW`: "absview"
  * `ABSVIEWT0YPE`: "absviewt0ype", "absvt0ype", "absvtflat"
  * `ABSVIEWTYPE`: "absviewtype", "absvtbox", "absvtype"
  * `CASTFN`: "castfn"
  * `DATAPROP`: "dataprop"
  * `DATATYPE`: "datatype"
  * `DATAVIEW`: "dataview"
  * `DATAVTYPE`: "dataviewtype", "datavtype"
  * `DLRDELAY`: "$delay"
  * `DLREFFMASK_ALL`: "$effmask_all"
  * `DLREFFMASK_EXN`: "$effmask_exn"
  * `DLREFFMASK_NTM`: "$effmask_ntm"
  * `DLREFFMASK_REF`: "$effmask_ref"
  * `DLREFFMASK_WRT`: "$effmask_wrt"
  * `DLRLDELAY`: "$ldelay"
  * `DLRLST`: "$list", "$lst"
  * `DLRLST_T`: "$list_t", "$lst_t"
  * `DLRLST_VT`: "$list_vt", "$lst_vt"
  * `DLRREC`: "$rec", "$record"
  * `DLRREC_T`: "$record_t", "$rec_t"
  * `DLRREC_VT`: "$record_vt", "$rec_vt"
  * `DLRTUP_T`: "$tuple_t", "$tup_t"
  * `DLRTUP`: "$tup", "$tuple"
  * `DLRTUP_VT`: "$tuple_vt", "$tup_vt"
  * `DLRVCOPYENV_VT`: "$vcopyenv_vt"
  * `DLRVCOPYENV_V`: "$vcopyenv_v"
  * `FN`: "fn" — non-recursive
  * `FNX`: "fnx" — mutual tail-rec.
  * `FUN`: "fun" — general-recursive
  * `IMPLEMENT`: "implement" — 1
  * `IMPLMNT`: "implmnt" — 0
  * `INFIX`: "infix"
  * `INFIXL`: "infixl"
  * `INFIXR`: "infixr"
  * `MACDEF`: "macdef"
  * `MACRODEF`: "macrodef"
  * `POSTFIX`: "postfix"
  * `PRAXI`: "praxi"
  * `PREFIX`: "prefix"
  * `PRFN`: "prfn"
  * `PRFUN`: "prfun"
  * `PRIMPLMNT`: "primplement", "primplmnt" — ~1
  * `PROPDEF`: "propdef"
  * `PRVAL`: "prval"
  * `PRVAR`: "prvar"
  * `TYPEDEF`: "typedef"
  * `VAR`: "var"
  * `VIEWDEF`: "viewdef"
  * `VIEWTYPEDEF`: "viewtypedef", "vtypedef"
  * `WITHPROP`: "withprop"
  * `WITHTYPE`: "withtype"
  * `WITHVIEWTYPE`: "withviewtype", "withvtype"
  * `WITHVIEW`: "withview"


Derived from other products
------------------------------------------------------------------------------

Here, order does not matter.

  * `T_ABSTYPE`: `ABSTYPE` | `ABST0YPE` | `ABSPROP` | `ABSVIEW` | `ABSVIEWTYPE`
    | `ABSVIEWT0YPE`
  * `T_CASE`: `CASE` | `CASE_pos` | `CASE_neg`
  * `T_COMMENT_block`: `COMMENT_block_c` | `COMMENT_block_ml`
  * `T_DATATYPE`: `DATATYPE` | `DATAPROP` | `DATAVIEW` | `DATAVTYPE`
  * `T_DLRDELAY`: `DLRDELAY` | `DLRLDELAY`
  * `T_DLREFFMASK_ARG`: `DLREFFMASK_NTM` | `DLREFFMASK_EXN` | `DLREFFMASK_REF`
    | `DLREFFMASK_WRT` | `DLREFFMASK_ALL`
  * `T_DLRLST`: `DLRLST` | `DLRLST_T` | `DLRLST_VT`
  * `T_DLRREC`: `DLRREC` | `DLRREC_T` | `DLRREC_VT`
  * `T_DLRTUP`: `DLRTUP` | `DLRTUP_T` | `DLRTUP_VT`
  * `T_DLRVCOPYENV`: `DLRVCOPYENV_V` | `DLRVCOPYENV_VT`
  * `T_ERR` — additional rules not described is this document.
  * `T_FIX`: `FIX` | `FIXAT`
  * `T_FIXITY`: `INFIX` | `INFIXL` | `INFIXR` | `PREFIX` | `POSTFIX`
  * `T_FUN`: `FN` | `FNX` | `FUN` | `PRFN` | `PRFUN` | `PRAXI` | `CASTFN`
  * `T_IMPLEMENT`: `IMPLMNT` | `IMPLEMENT` | `PRIMPLMNT`
  * `T_LAM`: `LAM` | `LAMAT` | `LLAM` | `LLAMAT`
  * `T_MACDEF`: `MACDEF` | `MACRODEF`
  * `T_TYPEDEF`: `PROPDEF` | `VIEWDEF` | `TYPEDEF` | `VIEWTYPEDEF`
  * `T_TYPE`: `TYPE` | `TYPE_pos` | `TYPE_neg` | `T0YPE` | `T0YPE_pos`
    | `T0YPE_neg` | `PROP` | `PROP_pos` | `PROP_neg` | `VIEW` | `VIEW_pos`
    | `VIEW_neg` | `VIEWTYPE` | `VIEWTYPE_pos` | `VIEWTYPE_neg` | `VIEWT0YPE`
    | `VIEWT0YPE_pos` | `VIEWT0YPE_neg`
  * `T_VAL`: `VAL` | `VAL_pos` | `VAL_neg` | `PRVAL`
  * `T_VAR`: `VAR` | `PRVAR`
  * `T_WITHTYPE`: `WITHTYPE` | `WITHPROP` | `WITHVIEW` | `WITHVIEWTYPE`

The multiple alternatives are not synonymous!
