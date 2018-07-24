ATS2 big lines syntax
==============================================================================

The big lines of ATS2 syntax is described here with a purposely simple but real
model. The model was checked running a rather formal parser on a reasonably
large and representative set of sources. It defines a boundary based
segmentation of ATS2 sources. Each rule is in the form of a product name
followed by an equal‑sign follow by boundaries delimiting “…” parts which may
contains “any” sequence of tokens. The “…” are there to say there may be
anything between two boundaries, it may even be empty. Matching these rules is
not enough to be valid ATS2, but these rules are enough to have a grasp on a
source file and have an quick and easy overview of ATS2 syntax. These rules
are also enough for a “first‑pass” or “first‑level” parsing of the ATS2
language.

The keywords are subject to the lexical rules described in “lexemes-guide.md”.


Reading the rules of the big lines syntax
------------------------------------------------------------------------------

The meaning of the rules is better explained with examples, incrementally.

Explained just next, in short there are:

  * Boundaries
  * Implied end boundaries
  * Semicolon end boundaries
  * Optional part boundaries
  * Repeatable part boundaries


**Boundaries:** `LET_EXP = let … in … end` means a `LET_EXP` starts with
`let` and has two “…” required parts whose boundaries are `in` and `end`. Note
a “…” part may be empty although the syntax of inner parts — which is not yet
documented — may forbid it.

**Implied end boundaries:** `FORSTAR_EXP = "for*" … => … IMPEND` means the
second part has no explicit end boundary, its end is implied: the
`FORSTAR_EXP` ends with the outer expression containing it or with any outer
boundaries which follows it. An example of the first case may be the closing
`)` of an outer expression; an example of the second case may be a `typedef`
declaration following it or the `in` boundary of an outer `LET_EXP` or the end
of the source file. The rest is as explained before.

**Semicolon end boundaries:** `ABSTYPE_DECL = abstype … "and"* … ";"?` means
the end boundary is very like an implied boundary (explained before), just
that it also accepts a semi‑colon as an end marker, as much as an implied end.
Additionally, the semi‑colon may appear multiple time.

**Optional part boundaries:** `IF_EXP = if … then … else? … IMPEND` means
the `else` starting the third part, is optional, thus the third part is
optional; that is, it may as much be `if … then … else …` or `if … then …`
(which is actually valid under conditions). The rest is as explained before.

**Reaptable part boundaries:** `SCASE_EXP = scase … of … "|"* … IMPEND`
means `|` is an optional boundaries (as explained before) which can be
repeated; that is, it may as much be `scase … of …` or `scase … of … | …` or
`scase … of … | … | …`. The repetition applies to the part it ends in the
rule (here, the second part). The rest is as explained before.

The parser mentioned before uses additional sanity rules which are not
described here.


Rules index and outline
------------------------------------------------------------------------------

The rules are subdivided in five groups where rules share noticeable
similarities.

  1. Expressions, with explicit begin and end boundaries.
  2. Expressions, with implied end boundaries.
  3. Declarations blocks, with explicit begin and end boundaries.
  4. Declarations, with explicit or implied semi‑colon.
  5. Declarations, like in #4 and repeatable with the `"and"` keyword.


In the following sub‑sections, keywords and symbols in rules, are shown
wrapped in double‑quotes to avoid ambiguities. When a name in all upper‑case
appears in place of a keyword, it means it may be one from a list of keywords
which is given in the construct’s dedicated section. Otherwise, if the keyword
is unique, then it is given directly in the rule. Even where there is no risk
of ambiguity, keywords are still wrapped in double‑quotes, to ease searching
by avoiding irrelevant matches.

The meaning of each rule is given later, each in its own section. The title
of the sections are that of the rule. Ex. to learn more about
`let … in … end`, go to (later) the section whose title is `LET_EXP`. In
each of these sections, the corresponding rule is recalled.

To search for a keyword in this document, search for it wrapped in
double‑quotes and follow the tracks you get from where it drives you. You may
have multiple matches.


### Expressions

With explicit begin and end boundaries:

        ATLBRACE_EXP =         "@{" … "}"
        ATLBRACKET_EXP =       "@[" … "]"
        ATLPAREN_EXP =         "@(" … ")"
        BEGIN_EXP =         "begin" … "end"
        BQUOTELPAREN_EXP =     "`(" … ")"
        COMMALPAREN_EXP =      ",(" … ")"
        HASHLBRACKET_EXP =     "#[" … "]"
        IDENT_arr_EXP =    ALNUM"[" … "]"
        IDENT_tmp_EXP =    ALNUM"<" … ">"
        LBRACE_EXP =            "{" … "}"
        LBRACKET_EXP =          "[" … "]"
        LET_EXP =             "let" … "in" … "end"
        LPAREN_EXP =            "(" … ")"
        QUOTELBRACE_EXP =      "'{" … "}"
        QUOTELBRACKET_EXP =    "'[" … "]"
        QUOTELPAREN_EXP =      "'(" … ")"
        SYMLT_EXP             SYMLT … ">"
        WHERE_EXP =         "where" … "end"


with implied end boundaries:

        ADDRAT_EXP =     "addr@" … IMPEND
        CASE_EXP =          CASE … "of" … "|"* … IMPEND
        FIX_EXP =          "fix" … IMPEND
        FOLDAT_EXP =     "fold@" … IMPEND
        FOR_EXP =          "for" … IMPEND
        FORSTAR_EXP =     "for*" … "=>" … IMPEND
        FREEAT_EXP =     "free@" … IMPEND
        IFCASE_EXP =    "ifcase" … "|"* … IMPEND
        IF_EXP =            "if" … then … "else"? … IMPEND
        LAM_EXP =          "lam" … IMPEND
        OP_EXP =            "op" … IMPEND
        SCASE_EXP =      "scase" … "of" … "|"* … IMPEND
        SIF_EXP =          "sif" … "then" … "else" … IMPEND
        TRY_EXP =          "try" … "with" … IMPEND
        VIEWAT_EXP =     "view@" … IMPEND
        WHILE_EXP =      "while" … IMPEND
        WHILESTAR_EXP = "while*" … "=>" … IMPEND


The `WHERE_EXP` construct is a special case, as explained in its section.


### Declarations blocks

With explicit begin and end boundaries.

        LOCAL_DECL   = "local" … "in" … "end"
        SRPCOND_DECL = SRPCOND … "#then"? … SRPELCOND? … "#else"? … "#endif"


Note `"let" … "in" … "end"` too, contains declarations, in its first part,
although this first part may be empty and the construct is an expression.


### Declarations

With explicit or implied semi‑colon:

        CLASSDEC_DECL =     "classdec" … ":"? … ";"?
        EXTCODE_DECL =       "extcode" … ";"?
        EXTERN_DECL =         "extern" … ";"?
        EXTTYPE_DECL =       "exttype" … ";"?
        EXTVAR_DECL =         "extvar" … ";"?
        FIXITY_DECL =           FIXITY … ";"?
        IMPLEMENT_DECL =     IMPLEMENT … ";"?
        NONFIX_DECL =         "nonfix" … ";"?
        OVERLOAD_DECL =     "overload" … "with" … ";"?
        SRPASSERT_DECL =     "#assert" … ";"?
        SRPCODEGEN2_DECL = "#codegen2" … ";"?
        SRPDEFINE_DECL =     "#define" … ";"?
        SRPDYNLOAD_DECL =   SRPDYNLOAD … ";"?
        SRPERROR_DECL =       "#error" … ";"?
        SRPINCLUDE_DECL =   "#include" … ";"?
        SRPPRAGMA_DECL =     "#pragma" … ";"?
        SRPPRERR_DECL =       "#prerr" … ";"?
        SRPPRINT_DECL =       "#print" … ";"?
        SRPREQUIRE_DECL =   "#require" … ";"?
        SRPSTALOAD_DECL =   SRPSTALOAD … ";"?
        SRPUNDEF_DECL =       "#undef" … ";"?
        STATIC_DECL =         "static" … ";"?
        SYMELIM_DECL =       "symelim" … ";"?
        SYMINTR_DECL =       "symintr" … ";"?
        TKINDEF_DECL =       "tkindef" … ";"?

        ASSUME_DECL = ASSUME … ";"?
        REASSUME_DECL = REASSUME … ";"?


Similarly and repeatable with the `"and"` keyword:

        ABSTYPE_DECL =       ABSTYPE … "and"* … ";"?
        DATASORT_DECL =   "datasort" … "and"* … ";"?
        DATATYPE_DECL =     DATATYPE … "and"* … ";"?
        EXCEPTION_DECL = "exception" … "and"* … ";"?
        FUN_DECL =               FUN … "and"* … ";"?
        MACDEF_DECL =         MACDEF … "and"* … ";"?
        REC_DECL =             "rec" … "and"* … ";"?
        SORTDEF_DECL =     "sortdef" … "and"* … ";"?
        STACST_DECL =         STACST … "and"* … ";"?
        STADEF_DECL =       "stadef" … "and"* … ";"?
        TYPEDEF_DECL =       TYPEDEF … "and"* … ";"?
        VAL_DECL =               VAL … "and"* … ";"?
        VAR_DECL =               VAR … "and"* … ";"?


Note the boundary for the first part of `CLASSDEC_DECL`, is a colon, not a
semi‑colon (it may visually looks similar).

Constructs with all empty parts are a special case: it does end on its own
but with what follows it and contains it. Ex. `static fn (): int` is a
`STATIC_DECL` containing the `FUN_DECL` which follows it. In particular, the
`REC_DECL` must only appears as such, ex. as `val rec a = …` or
`macdef rec …`, also but the other with `STATIC_DECL` (and not only), which can
only contains another declaration. Remember the rules given here so far, are
just outlines, and there are additional validity conditions required by the
language.


ABSTYPE_DECL
------------------------------------------------------------------------------

        ABSTYPE_DECL = ABSTYPE … "and"* … ";"?

Declaration; static; abstract; type;

Where `ABSTYPE` may be one of:

  * "abstbox"
  * "abstype"
  * "abst@ype"
  * "abst0ype"
  * "abstflat"
  * "absprop"
  * "absview"
  * "absviewtype"
  * "absvtbox"
  * "absvtype"
  * "absvt@ype"
  * "absviewt@ype"
  * "absviewt0ype"
  * "absvt0ype"
  * "absvtflat"

Abstract prop, type, view or viewtype. These are special cases of
`STACST_DECL` which is more versatile but less expresses the intent.


ADDRAT_EXP
------------------------------------------------------------------------------

        ADDRAT_EXP = "addr@" … IMPEND

Expression; dynamic;

Given a `var` named `v`, `addr@ v` returns the address of `v` or sort `addr`.
A proof of the view of something at that location will also be needed to make
anything out of it. See also `VIEWAT_EXP`.

Example:

        var i:int = 0
        val i_ref = ref_make_viewptr{int}(view@(i) | addr@(i))


ASSUME_DECL
------------------------------------------------------------------------------

        ASSUME_DECL = ASSUME … ";"?

Declaration; static;

Where `ASSUME` may be one of:

  * "assume"
  * "absimpl"


ATLBRACE_EXP
------------------------------------------------------------------------------

        ATLBRACE_EXP = "@{" … "}"

Expression; static; dynamic; flat;

Expression for flat records types and values. It has two forms, one defining a
type (static) and one defining a value of that type (dynamic). The sort
of a flat record is `t@ype`.

Example:

        typedef t = @{a=int, b=int}
        val u = @{a=1, b=2}
        val v:t = @{a=1, b=2}
        val x = u.a


The field names may identifiers or natural numbers expressed as decimal. When
all fields a numbers and when there starts at zero and increase one by one, a
flat tuple may be used instead. A flat tuple is a special case of a flat
record. See also `ATLPAREN_EXP`.

Example:

        typedef t = @{1=int, 2=int, a=int, b=int}
        extern val v:t
        val x = v.a
        val y = v.1


ATLBRACKET_EXP
------------------------------------------------------------------------------

        ATLBRACKET_EXP = "@[" … "]"

Expression; static; dynamic; flat;

Expression for flat one‑dimmnsion arrays types and values. It has two forms,
one defining a type (static) and one defining a value of that type (dynamic).
The sort of a flat array is `t@ype`.

The expression `@[t][n]` means the type of an array of `n` element of type
`t`. The expression `@[t](a, b, …)` (without really a “…”) means a literal
for an array of elements of type `t` initialized with `a`, `b` and so on.

Example:

        typedef t = @[int][3]
        var v:t = @[int](1, 2, 3)
        val a = v[0]

An array type is mono–dimensional only, even you don’t get a syntax error
trying otherwise. To be accessible, an array needs to be allocated in a `var`,
not a `val`, although you don’t get a type error when trying otherwise. In
the example above, the array is statically allocated, no heap allocation is
involved.

The elements may be all initialized with the same value:

        typedef t = @[int][3]
        var v:t = @[int](5) // |1…2] is 5


ATLPAREN_EXP
------------------------------------------------------------------------------

        ATLPAREN_EXP = "@(" … ")"

Expression; static; dynamic; flat;

Expression for flat tuples types and values. It has two forms, one defining a
type (static) and one defining a value of that type (dynamic).  The sort
of a flat tuple is `t@ype`.

Example:

        typedef t = @{a=int, b=int}
        val u = @{a=1, b=2}
        val v:t = @{a=1, b=2}


The field names are natural numbers, starting at zero and increasing one by
one. Field selectors must be expression using the decimal notation, no other
base is allowed. A field selector is a special lexical unit. A flat tuple
is a special case of a flat record. See also `ATLBRACE_EXP`.

Example:

        typedef t = @(int, char)
        val u = @(1, 'a')
        val v:t = @(1, 'a')
        val i = u.0
        val c = u.1


BEGIN_EXP
------------------------------------------------------------------------------

        BEGIN_EXP = "begin" … "end"

Expression; dynamic;

Expression of void type. It contains a sequence of void expressions,
semi‑colon separated. Unlike with declarations, the semi‑colons are required.
There may be an extraneous semi‑colon at the end. The same can be written
using an `LPAREN_EXP`, but a `BEGIN_EXP` more expresses the intent.

Example:

        val () = begin print! "a"; println! "b" end
        val () = (print! "a"; println! "b") // Same as this.

        implement main0() = begin
           println! "Hello ...";
           println! "... world!";
        end


BQUOTELPAREN_EXP
------------------------------------------------------------------------------

        BQUOTELPAREN_EXP = "`(" … ")"

Expression;


CASE_EXP
------------------------------------------------------------------------------

        CASE_EXP = CASE … "of" … "|"* … IMPEND

Expression;

Where `CASE` is one of:

  * "case"
  * "case+"
  * "case-"


CLASSDEC_DECL
------------------------------------------------------------------------------

        CLASSDEC_DECL = "classdec" … ":"? … ";"?

Declaration; static;


COMMALPAREN_EXP
------------------------------------------------------------------------------

        COMMALPAREN_EXP = ",(" … ")"

Expression;


DATASORT_DECL
------------------------------------------------------------------------------

        DATASORT_DECL = "datasort" … "and"* … ";"?

Declaration; static;


DATATYPE_DECL
------------------------------------------------------------------------------

        DATATYPE_DECL = DATATYPE … "and"* … ";"?

Declaration; static; algebraic; dynamic; constructor;

Where `DATATYPE` may be one of:

  * "datatype"
  * "dataprop"
  * "dataview"
  * "dataviewtype"
  * "datavtype"

Defines an algebraic type of prop, type, view or viewtype sort. The type
belongs to the dynamic but the constructors belong to the dynamic. There is
no associated versatile variant as there are with `ABSTYPE_DECL` and
`TYPEDEF_DECL`.


EXCEPTION_DECL
------------------------------------------------------------------------------

        EXCEPTION_DECL = "exception" … "and"* … ";"?

Declaration; static; dynamic;


EXTCODE_DECL
------------------------------------------------------------------------------

        EXTCODE_DECL = "extcode" … ";"?

Declaration; static; dynamic;


EXTERN_DECL
------------------------------------------------------------------------------

        EXTERN_DECL = "extern" … ";"?

Declaration; dynamic;


EXTTYPE_DECL
------------------------------------------------------------------------------

        EXTTYPE_DECL = "exttype" … ";"?

Declaration; static;


EXTVAR_DECL
------------------------------------------------------------------------------

        EXTVAR_DECL = "extvar" … ";"?

Declaration; dynamic;


FIX_EXP
------------------------------------------------------------------------------

        FIX_EXP = "fix" … IMPEND

Expression;


FIXITY_DECL
------------------------------------------------------------------------------

        FIXITY_DECL = FIXITY … ";"?

Declaration; dynamic;

Where `FIXITY` may be one of:

  * "infix"
  * "infixl"
  * "infixr"
  * "prefix"
  * "postfix"


FOLDAT_EXP
------------------------------------------------------------------------------

        FOLDAT_EXP = "fold@" … IMPEND

Expression;


FOR_EXP
------------------------------------------------------------------------------

        FOR_EXP = "for" … IMPEND

Expression;


FORSTAR_EXP
------------------------------------------------------------------------------

        FORSTAR_EXP = "for*" … "=>" … IMPEND

Expression;


FREEAT_EXP
------------------------------------------------------------------------------

        FREEAT_EXP = "free@" … IMPEND

Expression;


FUN_DECL
------------------------------------------------------------------------------

        FUN_DECL = FUN … "and"* … ";"?

Declaration; dynamic;

Where `FUN` is one of:

  * "fn"
  * "fnx"
  * "fun"
  * "prfn"
  * "prfun"
  * "praxi"
  * "castfn"


HASHLBRACKET_EXP
------------------------------------------------------------------------------

        HASHLBRACKET_EXP = "#[" … "]"

Expression;


IDENT_arr_EXP
------------------------------------------------------------------------------

        IDENT_arr_EXP = ALNUM"[" … "]"

Expression;


IDENT_tmp_EXP
------------------------------------------------------------------------------

        IDENT_tmp_EXP = ALNUM"<" … ">"

Expression;


IFCASE_EXP
------------------------------------------------------------------------------

        IFCASE_EXP = "ifcase" … "|"* … IMPEND

Expression;


IF_EXP
------------------------------------------------------------------------------

        IF_EXP = "if" … then … "else"? … IMPEND

Expression;


IMPLEMENT_DECL
------------------------------------------------------------------------------

        IMPLEMENT_DECL = IMPLEMENT … ";"?

Declaration; dynamic;

Where `IMPLEMENT` is one of:

  * "implmnt"
  * "implement"
  * "primplement"
  * "primplmnt"


LAM_EXP
------------------------------------------------------------------------------

        LAM_EXP = "lam" … IMPEND

Expression;


LBRACE_EXP
------------------------------------------------------------------------------

        LBRACE_EXP = "{" … "}"

Expression;


LBRACKET_EXP
------------------------------------------------------------------------------

        LBRACKET_EXP = "[" … "]"

Expression;


LET_EXP
------------------------------------------------------------------------------

        LET_EXP = "let" … "in" … "end"

Expression;


LOCAL_DECL
------------------------------------------------------------------------------

        LOCAL_DECL   = "local" … "in" … "end"

Declaration; static; dynamic;


LPAREN_EXP
------------------------------------------------------------------------------

        LPAREN_EXP = "(" … ")"

Expression;

For sequence of void expressios, see also `BEGIN_EXP`.


MACDEF_DECL
------------------------------------------------------------------------------

        MACDEF_DECL = MACDEF … "and"* … ";"?

Declaration;

Where `MACDEF` may be one of:

  * "macdef"
  * "macrodef"


NONFIX_DECL
------------------------------------------------------------------------------

        NONFIX_DECL = "nonfix" … ";"?

Declaration; dynamic;


OP_EXP
------------------------------------------------------------------------------

        OP_EXP = "op" … IMPEND

Expression;


OVERLOAD_DECL
------------------------------------------------------------------------------

        OVERLOAD_DECL = "overload" … "with" … ";"?

Declaration; dynamic;


QUOTELBRACE_EXP
------------------------------------------------------------------------------

        QUOTELBRACE_EXP = "'{" … "}"

Expression;


QUOTELBRACKET_EXP
------------------------------------------------------------------------------

        QUOTELBRACKET_EXP = "'[" … "]"

Expression;


QUOTELPAREN_EXP
------------------------------------------------------------------------------

        QUOTELPAREN_EXP = "'(" … ")"

Expression;


REASSUME_DECL
------------------------------------------------------------------------------

        REASSUME_DECL = REASSUME … ";"?

Declaration; static;

Where `REASSUME` may be one of:

  * "reassume"
  * "absreimpl"


REC_DECL
------------------------------------------------------------------------------

        REC_DECL = "rec" … "and"* … ";"?

Declaration;


SCASE_EXP
------------------------------------------------------------------------------

        SCASE_EXP = "scase" … "of" … "|"* … IMPEND

Expression;


SIF_EXP
------------------------------------------------------------------------------

        SIF_EXP = "sif" … "then" … "else" … IMPEND

Expression;


SORTDEF_DECL
------------------------------------------------------------------------------

        SORTDEF_DECL = "sortdef" … "and"* … ";"?

Declaration; static;


SRPASSERT_DECL
------------------------------------------------------------------------------

        SRPASSERT_DECL = "#assert" … ";"?

Declaration;


SRPCODEGEN2_DECL
------------------------------------------------------------------------------

        SRPCODEGEN2_DECL = "#codegen2" … ";"?

Declaration;


SRPCOND_DECL
------------------------------------------------------------------------------

        SRPCOND_DECL = SRPCOND … "#then"? … SRPELCOND? … "#else"? … "#endif"

Declaration;

Where `SRPCOND` may be one of:

  * "#if"
  * "#ifdef"
  * "#ifndef"

And where `SRPELCOND` may be one of:

  * "#elif"
  * "#elifdef"
  * "#elifndef"


SRPDEFINE_DECL
------------------------------------------------------------------------------

        SRPDEFINE_DECL = "#define" … ";"?


Declaration;

SRPDYNLOAD_DECL
------------------------------------------------------------------------------

        SRPDYNLOAD_DECL = SRPDYNLOAD … ";"?

Declaration; dynamic;

Where `SRPDYNLOAD` is one of:

  * "dynload"
  * "#dynload"


SRPERROR_DECL
------------------------------------------------------------------------------

        SRPERROR_DECL = "#error" … ";"?

Declaration;


SRPINCLUDE_DECL
------------------------------------------------------------------------------

        SRPINCLUDE_DECL = "#include" … ";"?

Declaration;


SRPPRAGMA_DECL
------------------------------------------------------------------------------

        SRPPRAGMA_DECL = "#pragma" … ";"?

Declaration;


SRPPRERR_DECL
------------------------------------------------------------------------------

        SRPPRERR_DECL = "#prerr" … ";"?

Declaration;


SRPPRINT_DECL
------------------------------------------------------------------------------

        SRPPRINT_DECL = "#print" … ";"?

Declaration;


SRPREQUIRE_DECL
------------------------------------------------------------------------------

        SRPREQUIRE_DECL = "#require" … ";"?

Declaration;


SRPSTALOAD_DECL
------------------------------------------------------------------------------

        SRPSTALOAD_DECL = SRPSTALOAD … ";"?

Declaration; static; dynamic;

Where `SRPSTALOAD` may be one of:

  * "staload"
  * "#staload"


SRPUNDEF_DECL
------------------------------------------------------------------------------

        SRPUNDEF_DECL = "#undef" … ";"?

Declaration;


STACST_DECL
------------------------------------------------------------------------------

        STACST_DECL = STACST … "and"* … ";"?

Declaration; static; abstract;

Where `STACST` may be one of:

  * "sta"
  * "stacst"

Abstract static expression. Abstract: the value does not matter and there is
none, only the introduced identity (name) and its declared sort, do.
`ABSTYPE_DECL` has more specialized keywords better expressing the intent.

This has little to be compared with the usual meaning of “constant”, rather
think of it as if it was named “absdef”.


STADEF_DECL
------------------------------------------------------------------------------

        STADEF_DECL = "stadef" … "and"* … ";"?

Declaration; static; aliasing;

Versatile static expression aliasing. `TYPEDEF_DECL` has more specialized
keywords better expressing the intent.


STATIC_DECL
------------------------------------------------------------------------------

        STATIC_DECL = "static" … ";"?

Declaration; dynamic;


SYMELIM_DECL
------------------------------------------------------------------------------

        SYMELIM_DECL = "symelim" … ";"?

Declaration; dynamic;


SYMINTR_DECL
------------------------------------------------------------------------------

        SYMINTR_DECL = "symintr" … ";"?

Declaration; dynamic;


SYMLT_EXP
------------------------------------------------------------------------------

        SYMLT_EXP = SYMLT … ">"

Expression;

Where `SYMLT` may be one of:

  * ":<"
  * "=<"
  * "-<"


TKINDEF_DECL
------------------------------------------------------------------------------

        TKINDEF_DECL = "tkindef" … ";"?

Declaration; static;


TRY_EXP
------------------------------------------------------------------------------

        TRY_EXP = "try" … "with" … IMPEND

Expression;


TYPEDEF_DECL
------------------------------------------------------------------------------

        TYPEDEF_DECL = TYPEDEF … "and"* … ";"?

Declaration; static; aliasing; type;

Where `TYPEDEF` may be one of:

  * "propdef"
  * "typedef"
  * "viewdef"
  * "viewtypedef"
  * "vtypedef"

Prop, type, view or viewtype expression aliasing. Specialized cases of
`STADEF_DECL` which is more versatile but less expresses the intent.


VAL_DECL
------------------------------------------------------------------------------

        VAL_DECL = VAL … "and"* … ";"?

Declaration; dynamic;

Where `VAL` is one of:

  * "val"
  * "val+"
  * "val-"
  * "prval"


VAR_DECL
------------------------------------------------------------------------------

        VAR_DECL = VAR … "and"* … ";"?

Declaration; dynamic;

Where `VAR` is one of:

  * "var"
  * "prvar"


VIEWAT_EXP
------------------------------------------------------------------------------

        VIEWAT_EXP = "view@" … IMPEND

Expression; dynamic;

Given a `var` `v:t`, `view@(v)` returns a proof of a view of a `t` at `v`.
See also `ADDRAT_EXP`.

Example:

        var i:int
        prval pf = view@ i


WHERE_EXP
------------------------------------------------------------------------------

        WHERE_EXP = "where" … "end"


WHILE_EXP
------------------------------------------------------------------------------

        WHILE_EXP = "while" … IMPEND

Expression;


WHILESTAR_EXP
------------------------------------------------------------------------------

        WHILESTAR_EXP = "while*" … "=>" … IMPEND

Expression;

