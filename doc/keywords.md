Postiats keywords
==============================================================================

Before anything
------------------------------------------------------------------------------

Here, is a reference list of ATS2 keywords based on lexical productions, an
expanded list of these and a list of synonymous groups.

This document is about a keywords reference list, not a keyword based
reference of ATS2.

The reference list of keywords is given as a list of lexical productions, as
described in “lexemes.md”. This is important since there may be synonymous and
lexical productions are not just simple strings.

The second list is informational only and is derived from the first list and
the rules given in “lexemes.md”. It is informational only, because it lacks
the exact lexical rules.

The third list, informational too, groups synonymous. There are no singleton
in this list, so if a keyword has no synonymous, then it is not in the third
list. When a keyword production designates multiple semantic constructs whose
introductory keywords has no synonymous, it is not listed in the third list
neither.

The first list is inferred from `pats_parsing_kwds.dats` and
`pats_parsing_decl.dats`, with the hope there is no omission, nothing was
overlooked, since there is no clearly distinguished list of keywords in
Postiats source (many are missing, in `pats_parsing_kwds.dats`).

Postiats also has predefined identifiers, which are not listed here. These
identifiers are not keywords.

Keywords are not necessarily words, they may be made of symbolic characters,
although the ones introducing a declaration are words‑like (except one).

Some keywords are the same as predefined identifiers. An ATS2 colorizer could
hardly be perfect without some syntax analyses, atlhough it is not too hard
to make it good enough.


Reference keywords list
------------------------------------------------------------------------------

The keywords are given using references to lexical productions, the texts in
the list is not the actual keywords. The second list, later, gives the texts
of the actual keywords.

To ease its possible uses, the list is split‑down into sub‑lists by
categories.

Some keywords actually designated multiple concrete keywords, possibly
synonymous as much as possibly not.


### Static declaration keywords

  * `T_ABSTYPE`
  * `T_ASSUME`
  * `T_CLASSDEC`
  * `T_DATASORT`
  * `T_DATATYPE`
  * `T_EXCEPTION`
  * `T_EXTYPE`
  * `T_FIXITY`
  * `T_MACDEF`
  * `T_NONFIX`
  * `T_OVERLOAD`
  * `T_REASSUME`
  * `T_SORTDEF`
  * `T_SRPSTALOAD`
  * `T_STACST`
  * `T_STADEF`
  * `T_SYMELIM`
  * `T_SYMINTR`
  * `T_TKINDEF`
  * `T_TYPEDEF`


### Dynamic declaration keywords

  * `T_EXTCODE`
  * `T_EXTERN`
  * `T_EXTVAR`
  * `T_FUN`
  * `T_IMPLEMENT`
  * `T_LOCAL`
  * `T_SRPDYNLOAD`
  * `T_STATIC` — yes, dynamic!
  * `T_VAL`
  * `T_VAR`


### Preprocessor keywords

Note `T_SRPSTALOAD` and `T_SRPDYNLOAD` are not listed here.

  * `T_SRPASSERT`
  * `T_SRPCODEGEN2`
  * `T_SRPDEFINE`
  * `T_SRPELIF`
  * `T_SRPELIFDEF`
  * `T_SRPELIFNDEF`
  * `T_SRPELSE`
  * `T_SRPENDIF`
  * `T_SRPERROR`
  * `T_SRPIF`
  * `T_SRPIFDEF`
  * `T_SRPIFNDEF`
  * `T_SRPINCLUDE`
  * `T_SRPPRAGMA`
  * `T_SRPPRERR`
  * `T_SRPPRINT`
  * `T_SRPREQUIRE`
  * `T_SRPTHEN`
  * `T_SRPUNDEF`


### Expression keywords

  * `T_AND` — not top‑level! (mutual references)
  * `T_AS`
  * `T_ATLBRACE`
  * `T_ATLPAREN`
  * `T_BANG`
  * `T_BAR`
  * `T_CASE`
  * `T_COLON`
  * `T_COMMA`
  * `T_DOT` — used at top‑level too.
  * `T_ELSE`
  * `T_END`
  * `T_EOF`
  * `T_EQ`
  * `T_EQGT`
  * `T_FORSTAR`
  * `T_GT`
  * `T_GTDOT`
  * `T_GTLT`
  * `T_IF`
  * `T_IFCASE`
  * `T_IN`
  * `T_LBRACE` — used at top‑level too.
  * `T_LBRACKET` — used at top‑level too.
  * `T_LPAREN` — used at top‑level too.
  * `T_OF`
  * `T_QUOTELBRACE`
  * `T_QUOTELPAREN`
  * `T_RBRACE`
  * `T_RBRACKET`
  * `T_REC`
  * `T_RPAREN`
  * `T_SCASE`
  * `T_SEMICOLON`
  * `T_SIF`
  * `T_THEN`
  * `T_TRY`
  * `T_WHEN`
  * `T_WHILESTAR`
  * `T_WITH`


Expanded keywords list — informational
------------------------------------------------------------------------------

Multiple items may be synonymous or may be not; it depends. The third list,
later, tells about synonymous.

The list is split‑down into sub‑lists the same way as the previous list.


### Static declaration keywords

  * `T_ABSTYPE`: "abstbox", "abstype", "abst@ype", "abst0ype", "abstflat",
    "absprop", "absview", "absviewtype", "absvtbox", "absvtype", "absvt@ype",
    "absviewt@ype", "absviewt0ype", "absvt0ype", "absvtflat"
  * `T_ASSUME`: "assume", "absimpl"
  * `T_CLASSDEC`: "classdec"
  * `T_DATASORT`: "datasort"
  * `T_DATATYPE`: "datatype", "dataprop", "dataview", "dataviewtype",
    "datavtype"
  * `T_EXCEPTION`: "exception"
  * `T_EXTYPE`: "extype"
  * `T_FIXITY`: "infix", "infixl", "infixr", "prefix", "postfix"
  * `T_MACDEF`: "macdef", "macrodef"
  * `T_NONFIX`: "nonfix"
  * `T_OVERLOAD`: "overload"
  * `T_REASSUME`: "reassume", "absreimpl"
  * `T_SORTDEF`: "sortdef"
  * `T_SRPSTALOAD`: "staload", "#staload"
  * `T_STACST`: "sta", "stacst"
  * `T_STADEF`: "stadef"
  * `T_SYMELIM`: "symelim"
  * `T_SYMINTR`: "symintr"
  * `T_TKINDEF`: "tkindef"
  * `T_TYPEDEF`: "propdef", "viewdef", "typedef", "viewtypedef", "vtypedef"


### Dynamic declaration keywords

  * `T_EXTCODE`: "%{"
  * `T_EXTERN`: "extern"
  * `T_EXTVAR`: "extvar"
  * `T_FUN`: "fn", "fnx", "fun", "prfn", "prfun", "praxi", "castfn"
  * `T_IMPLEMENT`: "implmnt", "implement", "primplement", "primplmnt"
  * `T_LOCAL`: "local"
  * `T_SRPDYNLOAD`: "dynload", "#dynload"
  * `T_STATIC`: "static"
  * `T_VAL`: "val", "val+", "val-", "prval"
  * `T_VAR`: "var", "prvar"


### Preprocessor keywords

Note "#staload" and "#dynload" are not listed here.

  * `T_SRPASSERT`: "#assert"
  * `T_SRPCODEGEN2`: "#codegen2"
  * `T_SRPDEFINE`: "#define"
  * `T_SRPELIF`: "#elif"
  * `T_SRPELIFDEF`: "#elifdef"
  * `T_SRPELIFNDEF`: "#elifndef"
  * `T_SRPELSE`: "#else"
  * `T_SRPENDIF`: "#endif"
  * `T_SRPERROR`: "#error"
  * `T_SRPIF`: "#if"
  * `T_SRPIFDEF`: "#ifdef"
  * `T_SRPIFNDEF`: "#ifndef"
  * `T_SRPINCLUDE`: "#include"
  * `T_SRPPRAGMA`: "#pragma"
  * `T_SRPPRERR`: "#prerr"
  * `T_SRPPRINT`: "#print"
  * `T_SRPREQUIRE`: "#require"
  * `T_SRPTHEN`: "#then"
  * `T_SRPUNDEF`: "#undef"


### Expression keywords

Some of these keywords are the same as some predefined identifiers. This
is where some care should be taken by colorizer designers.

  * `T_AND`: "and"
  * `T_AS`: "as"
  * `T_ATLBRACE`: "@{"
  * `T_ATLPAREN`: "@("
  * `T_BANG`: "!"
  * `T_BAR`: "|"
  * `T_CASE`: "case", "case+", "case-"
  * `T_COLON`: ":"
  * `T_COMMA`: ","
  * `T_DOT`: "."
  * `T_ELSE`: "else"
  * `T_END`: "end"
  * `T_EOF`: EOF
  * `T_EQ`: "="
  * `T_EQGT`: "=>"
  * `T_FORSTAR`: "for*"
  * `T_GT`: ">"
  * `T_GTDOT`: ">."
  * `T_GTLT`: "><"
  * `T_IF`: "if"
  * `T_IFCASE`: "ifcase"
  * `T_IN`: "in"
  * `T_LBRACE`: "{"
  * `T_LBRACKET`: "["
  * `T_LPAREN`: "("
  * `T_OF`: "of"
  * `T_QUOTELBRACE`: "'{"
  * `T_QUOTELPAREN`: "'("
  * `T_RBRACE`: "}"
  * `T_RBRACKET`: "]"
  * `T_REC`: "rec"
  * `T_RPAREN`: ")"
  * `T_SCASE`: "scase"
  * `T_SEMICOLON`: ";"
  * `T_SIF`: "sif"
  * `T_THEN`: "then"
  * `T_TRY`: "try"
  * `T_WHEN`: "when"
  * `T_WHILESTAR`: "while*"
  * `T_WITH`: "with"


Synonymous groups — informational
------------------------------------------------------------------------------

  * "assume", "absimpl"
  * "reassume", "absreimpl"
  * "dynload", "#dynload"
  * "staload", "#staload"
  * "sta", "stacst"
  * "abstbox", "abstype"
  * "abst@ype", "abst0ype", "abstflat"
  * "absviewtype", "absvtbox", "absvtype"
  * "absvt@ype", "absviewt@ype", "absviewt0ype", "absvt0ype", "absvtflat"
  * "dataviewtype", "datavtype"
  * "primplement", "primplmnt"
  * "viewtypedef", "vtypedef"

Note although "primplement" and "primplmnt" are synonymous, "implement" and
"implmnt" are not synonymous!

As a side note, “extern” **may** be a synonymous for “static”, “extype” or
“extvar”. Also "|" **may** be a synonymous for ";" in some cases.
