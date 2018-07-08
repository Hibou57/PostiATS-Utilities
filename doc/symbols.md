Postiats/ATS2 built‑in symbols
==============================================================================

Before anything
------------------------------------------------------------------------------

Postiats defines some symbols aside identifier lexical units.

The data for this document mainly come from `pats_symbol.sats`,
`pats_symbol.dats` and `pats_trans1_syndef.dats`. Multiple others files are
also involved, but are not listed here.

Most built‑in symbols are not subject to redefinition. Ex. if you re‑declare
the built‑in `true_bool` to anything possible, Postiats will still interpret
it the same way, as a boolean true‑pattern. The only exceptions are 1)
configuration variables which may not be really symbols but are listed here,
since Postiats source talks about it as symbols 2) the sorts which may be
redeclared (ex. `sortdef addr = bool`), even if one should never do this.

This document is about some identifiers referred to as symbol. A lexical unit
of the same text may also exists. Ex. `symbol_AT` has the same text as the
`T_AT` lexical unit and this document don’t tell anything about "@" as `T_AT`,
only about "@" as `symbol_AT`.


Syntactical symbols
------------------------------------------------------------------------------

  * `symbol_ADD`, "+": syntactic operator for adjusting precedence.
  * `symbol_BACKSLASH`, "\": temporary binary operator from a function even in
    patterns; may also be static and dynamic identifier
  * `symbol_SUB`, "-": syntactic operator for adjusting precedence.
  * `symbol_TUPZ`, "tupz", creates a flat tuple from a syntactical list.

Note "tupz" is to be used as "tupz!".


Symbols which can also be regular identifiers
------------------------------------------------------------------------------

  * `symbol_AT`, "@": static identifier.
  * `symbol_EQ`, "=": dynamic identifier, keyword in the statics.
  * `symbol_GTLT`, "><": dynamic identifier.
  * `symbol_GT`, ">": static and dynamic identifier.
  * `symbol_LT`, "<": static identifier
  * `symbol_TILDE`, "~": static and dynamic identifier.


Type operators
------------------------------------------------------------------------------

These operators alter the meaning of a type, hence they only appear in a
static expression.

  * `symbol_AMPERBANG`, "&!": read-write, invar(kind=3) type operator.
  * `symbol_AMPERQMARK`, "&?": write-only, invar(kind=2) type operator.
  * `symbol_AMPERSAND`, "&": read-only, invar(kind=1) type operator.
  * `symbol_BANG`, "!": dereference, invar(kind=0) type operator, static and
    dynamic identifier
  * `symbol_GTGT`, ">>": transitional type operator (a type changes into
    another upon function return).
  * `symbol_QMARKBANG`, "?!": top(kind=1) type operator.
  * `symbol_QMARK`, "?": top(kind=0) type operator.


Special static symbols
------------------------------------------------------------------------------

  * `symbol_MINUSGT`, "->": static special identifier (functional arrow).
  * `symbol_EQEQ`, "==": built‑in static equality operator.


Dynamic operators
------------------------------------------------------------------------------

  * `symbol_COLONEQ`, ":=": assign operator
  * `symbol_COLONEQCOLON`, ":=:": exhange operator


Pattern elements
------------------------------------------------------------------------------

  * `symbol_UNDERSCORE`, "_": wildward pattern, uninitialized dynamic
    expression (topized dynamic expression); not fully supported.
  * `symbol_VBOX`, "vbox": vbox pattern (the box you can’t left empty).
  * `symbol_TRUE_BOOL`, "true_bool": boolean‑true pattern.
  * `symbol_FALSE_BOOL`, "false_bool": boolean‑false pattern.


Sorts
------------------------------------------------------------------------------

The symbols are what’s after `symbol_`, in lower‑case.

  * `symbol_ADDR`
  * `symbol_BOOL`
  * `symbol_CLS`
  * `symbol_EFF`
  * `symbol_FLOAT`
  * `symbol_INT`
  * `symbol_PROP`
  * `symbol_REAL`
  * `symbol_STRING`
  * `symbol_T0YPE`
  * `symbol_TKIND`
  * `symbol_TYPE`
  * `symbol_TYPES`
  * `symbol_VIEW`
  * `symbol_VIEWT0YPE`, same as `symbol_VT0YPE`
  * `symbol_VIEWTYPE`, same as `symbol_VTYPE`
  * `symbol_VT0YPE`
  * `symbol_VTYPE`


Built‑in macfuns
------------------------------------------------------------------------------

The symbols are what’s after `symbol_`, in lower‑case.

  * `symbol_CAR`
  * `symbol_CDR`
  * `symbol_ISCONS`
  * `symbol_ISLIST`
  * `symbol_ISNIL`


Special dynamic functions (syndef)
------------------------------------------------------------------------------

The symbols are what’s after `symbol_`, in lower‑case. The symbol is used
with an "!" appended. Ex. `println! "Some text"`.

  * `symbol_FPRINT`
  * `symbol_FPRINTLN`
  * `symbol_FPRINT_NEWLINE`
  * `symbol_GPRINT`
  * `symbol_GPRINTLN`
  * `symbol_GPRINT_NEWLINE`
  * `symbol_PRERR`
  * `symbol_PRERRLN`
  * `symbol_PRERR_NEWLINE`
  * `symbol_PRINT`
  * `symbol_PRINTLN`
  * `symbol_PRINT_NEWLINE`


Environment variables
------------------------------------------------------------------------------

The symbols are what’s after `symbol_`, in upper‑case. If one of these is
not defined, Postiats falls‑back to an environment variable of the same
name less the initial "P". Ex. if `PATSHOME`, it will try to fall‑back to
`ATSHOME`.

  * `symbol_PATSCONTRIB`
  * `symbol_PATSHOME`
  * `symbol_PATSHOMELOCS`
  * `symbol_PATSRELOCROOT`


Configuration defines
------------------------------------------------------------------------------

The symbols are what’s after `symbol_`, in upper‑case. You use it as defines.
Ex. `#define ATS_DYNLOADFLAG 1`.

  * `symbol_ATS_DYNLOADFLAG` // global scope, int type, defaults to 1.
  * `symbol_ATS_DYNLOADNAME` // global scope, string type, defaults to nothing.
  * `symbol_ATS_EXTERN_PREFIX` // file scope, string type, defaults to "atspre_".
  * `symbol_ATS_MAINATSFLAG` // global scope, int type, defaults to 0.
  * `symbol_ATS_PACKNAME`: global scope, string type, defaults to "ATSLIB.prelude".
  * `symbol_ATS_STATIC_PREFIX` // global scope, string type, defaults to none.


Virtual
------------------------------------------------------------------------------

This one is a virtual symbol, it is not lexical unit from sources, it’s
created after syntax analysis: spaces may appears between "[" and "]" (but not
before "[" !).

  * `symbol_LRBRACKETS`, "[]".


For error messages only
------------------------------------------------------------------------------

These ones are only referred to by `ats_e1xpval.dats`.

  * `symbol_NEG` // ~ // only for error
  * `symbol_MUL` // * // only for error
  * `symbol_DIV` // / // only for error
  * `symbol_GTEQ` // >= // only for error
  * `symbol_LTEQ` // <= // only for error
  * `symbol_LTGT` // <> // only for error
  * `symbol_BANGEQ` // != // only for error
  * `symbol_LTLT` // << // only for error
  * `symbol_LAND` // && // only for error
  * `symbol_LOR` // || // only for error
  * `symbol_DEFINED` // only for error
  * `symbol_UNDEFINED` // only for error


Unused
------------------------------------------------------------------------------

These ones are defined bu nowhere referred to (at least as symbol).

  * `symbol_LAMAT`, "lam@"
  * `symbol_LLAMAT`, "llam@"
  * `symbol__STDIN__`, "__STDIN__"
  * `symbol__STRING__`, "__STRING__"
