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

Postiats also has predefined symbols, which are not listed here. These symbols
are not keywords. Predefined symbols are not necessarily symbols, they may be
made of word characters.

Keywords are not necessarily words, they may be made of symbolic characters.

Some keywords are the same as predefined symbols. An ATS2 colorizer could
hardly be perfect without some syntax analyses.


Reference keywords list
------------------------------------------------------------------------------

Some keywords actually designated multiple concrete keywords, possibly
synonymous as much as possibly not.


  * `T_ABSTYPE`
  * `T_AND`
  * `T_AS`
  * `T_ASSUME`
  * `T_ATLBRACE`
  * `T_ATLPAREN`
  * `T_BANG`
  * `T_BAR`
  * `T_CASE`
  * `T_CLASSDEC`
  * `T_COLON`
  * `T_COMMA`
  * `T_DATASORT`
  * `T_DATATYPE`
  * `T_DOT`
  * `T_ELSE`
  * `T_END`
  * `T_EOF`
  * `T_EQ`
  * `T_EQGT`
  * `T_EXCEPTION`
  * `T_EXTCODE`
  * `T_EXTERN`
  * `T_EXTVAR`
  * `T_EXTYPE`
  * `T_FIXITY`
  * `T_FORSTAR`
  * `T_FUN`
  * `T_GT`
  * `T_GTDOT`
  * `T_GTLT`
  * `T_IF`
  * `T_IFCASE`
  * `T_IMPLEMENT`
  * `T_IN`
  * `T_LBRACE`
  * `T_LBRACKET`
  * `T_LOCAL`
  * `T_LPAREN`
  * `T_MACDEF`
  * `T_NONFIX`
  * `T_OF`
  * `T_OVERLOAD`
  * `T_QUOTELBRACE`
  * `T_QUOTELPAREN`
  * `T_RBRACE`
  * `T_RBRACKET`
  * `T_REASSUME`
  * `T_REC`
  * `T_RPAREN`
  * `T_SCASE`
  * `T_SEMICOLON`
  * `T_SIF`
  * `T_SORTDEF`
  * `T_SRPASSERT`
  * `T_SRPCODEGEN2`
  * `T_SRPDEFINE`
  * `T_SRPDYNLOAD`
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
  * `T_SRPSTALOAD`
  * `T_SRPTHEN`
  * `T_SRPUNDEF`
  * `T_STACST`
  * `T_STADEF`
  * `T_STATIC`
  * `T_SYMELIM`
  * `T_SYMINTR`
  * `T_THEN`
  * `T_TKINDEF`
  * `T_TRY`
  * `T_TYPEDEF`
  * `T_VAL`
  * `T_VAR`
  * `T_WHEN`
  * `T_WHILESTAR`
  * `T_WITH`


Expanded keywords list — informational
------------------------------------------------------------------------------

Multiple items may be synonymous or may be not. It depends.


  * `T_ABSTYPE`: "abstbox", "abstype", "abst@ype", "abst0ype", "abstflat",
    "absprop" | "absview", "absviewtype", "absvtbox", "absvtype" ,
    "absvt@ype", "absviewt@ype", "absviewt0ype", "absvt0ype", "absvtflat"
  * `T_AND`: "and"
  * `T_AS`: "as"
  * `T_ASSUME`: "assume", "absimpl"
  * `T_ATLBRACE`: "@{"
  * `T_ATLPAREN`: "@("
  * `T_BANG`: "!"
  * `T_BAR`: "|"
  * `T_CASE`: "case", "case+", "case-"
  * `T_CLASSDEC`: "classdec"
  * `T_COLON`: ":"
  * `T_COMMA`: ","
  * `T_DATASORT`: "datasort"
  * `T_DATATYPE`: "datatype", "dataprop", "dataview", "dataviewtype",
    "datavtype"
  * `T_DOT`: "."
  * `T_ELSE`: "else"
  * `T_END`: "end"
  * `T_EOF`: EOF
  * `T_EQ`: "="
  * `T_EQGT`: "=>"
  * `T_EXCEPTION`: "exception"
  * `T_EXTCODE`: "%{"
  * `T_EXTERN`: "extern"
  * `T_EXTVAR`: "extvar"
  * `T_EXTYPE`: "extype"
  * `T_FIXITY`: "infix", "infixl", "infixr", "prefix", "postfix"
  * `T_FORSTAR`: "for*"
  * `T_FUN`: "fn" | "fnx" | "fun" | "prfn" | "prfun", "praxi", "castfn"
  * `T_GT`: ">"
  * `T_GTDOT`: ">."
  * `T_GTLT`: "><"
  * `T_IF`: "if"
  * `T_IFCASE`: "ifcase"
  * `T_IMPLEMENT`: "implmnt", "implement", "primplement", "primplmnt"
  * `T_IN`: "in"
  * `T_LBRACE`: "{"
  * `T_LBRACKET`: "["
  * `T_LOCAL`: "local"
  * `T_LPAREN`: "("
  * `T_MACDEF`: "macdef", "macrodef"
  * `T_NONFIX`: "nonfix"
  * `T_OF`: "of"
  * `T_OVERLOAD`: "overload"
  * `T_QUOTELBRACE`: "'{"
  * `T_QUOTELPAREN`: "'("
  * `T_RBRACE`: "}"
  * `T_RBRACKET`: "]"
  * `T_REASSUME`: "reassume", "absreimpl"
  * `T_REC`: "rec"
  * `T_RPAREN`: ")"
  * `T_SCASE`: "scase"
  * `T_SEMICOLON`: ";"
  * `T_SIF`: "sif"
  * `T_SORTDEF`: "sortdef"
  * `T_SRPASSERT`: "#assert"
  * `T_SRPCODEGEN2`: "#codegen2"
  * `T_SRPDEFINE`: "#define"
  * `T_SRPDYNLOAD`: "dynload", "#dynload"
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
  * `T_SRPSTALOAD`: "staload", "#staload"
  * `T_SRPTHEN`: "#then"
  * `T_SRPUNDEF`: "#undef"
  * `T_STACST`: "sta", "stacst"
  * `T_STADEF`: "stadef"
  * `T_STATIC`: "static"
  * `T_SYMELIM`: "symelim"
  * `T_SYMINTR`: "symintr"
  * `T_THEN`: "then"
  * `T_TKINDEF`: "tkindef"
  * `T_TRY`: "try"
  * `T_TYPEDEF`: "propdef", "viewdef", "typedef", "viewtypedef", "vtypedef"
  * `T_VAL`: "val", "val+", "val-", "prval"
  * `T_VAR`: "var", "prvar"
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
