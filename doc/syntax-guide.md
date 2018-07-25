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
source file and have a quick and easy overview of ATS2 syntax. These rules
are also enough for a “first‑pass” or “first‑level” parsing of the ATS2
language.

The keywords are subject to the lexical rules described in “lexemes-guide.md”.

The semantic description comming with the constructs, is intended to be terce.
For more, there are [Introduction to Programming in ATS](http://ats-lang.sourceforge.net/DOCUMENT/INT2PROGINATS/HTML/HTMLTOC/book1.html)
and [A Tutorial on Programming Features in ATS](http://ats-lang.sourceforge.net/DOCUMENT/ATS2TUTORIAL/HTML/HTMLTOC/book1.html).

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
a “…” part may be empty although the inner syntax of parts — which is not yet
documented — may forbid it.

**Implied end boundaries:** `FORSTAR_EXP = "for*" … => … IMPEND` means the
second part has no explicit end boundary, its end is implied: the
`FORSTAR_EXP` ends with the outer expression containing it or with any outer
boundaries which follows it. An example of the first case may be the closing
`)` of an outer expression; an example of the second case may be a `typedef`
declaration following it or the `in` boundary of an outer `LET_EXP` or the end
of the source file. The rest is as explained before.

**Semicolon end boundaries:** `ABSTYPE_DECL = abstype … "and"* … ";"?` means
the end boundary is very like an implied end boundary (explained before), just
that it also accepts a semicolon as an end marker, as much as an implied end.
Additionally, the semicolon may appear multiple times.

**Optional part boundaries:** `IF_EXP = if … then … else? … IMPEND` means
the `else` starting the third part, is optional, thus the third part is
optional; that is, it may as much be `if … then … else …` or `if … then …`
(which is actually valid under conditions). The rest is as explained before.

**Reaptable part boundaries:** `SCASE_EXP = scase … of … "|"* … IMPEND`
means `|` is an optional boundary (as explained before) which can be
repeated; that is, it may as much be `scase … of …` or `scase … of … | …` or
`scase … of … | … | …`. The repetition applies to the part it ends in the
rule (here, the second part). The rest is as explained before.

The parser mentioned before uses additional kind of rules which are not
described here.


Rules index and outline
------------------------------------------------------------------------------

The rules are subdivided in five groups where rules share noticeable
similarities.

  1. Expressions, with explicit begin and end boundaries.
  2. Expressions, with implied end boundaries.
  3. Declarations blocks, with explicit begin and end boundaries.
  4. Declarations, with explicit or implied semicolon.
  5. Declarations, like in #4 and repeatable with the `"and"` keyword.


In the following sub‑sections, keywords and symbols in rules, are shown
wrapped in double‑quotes to avoid ambiguities. When a name in all upper‑case
appears in place of a keyword, it means it may be one from a list of keywords
which is given in the construct’s dedicated section. Otherwise, if the keyword
is unique, then it is given directly in the rule. Even where there is no risk
of ambiguity, keywords are still wrapped in double‑quotes, to ease searching
by avoiding irrelevant matches.

The meaning of each rule is given later, each in its own section. The title
of the sections are that of the rules. Ex. to learn more about
`let … in … end`, go to (later) the section whose title is `LET_EXP`. In
each of these sections, the corresponding rule is recalled.

To search for a keyword in this document, search for it wrapped in
double‑quotes and follow the tracks you get from where it drives you. You may
have multiple matches.

Not all keywords appear yet, and some only partially appears, because their
use cannot be expressed with the simple syntactic model used: they take part
in parts inner syntax.


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


With implied end boundaries:

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


`ALNUM"["` and `ALNUM"<"` are atomic lexial units, no space is allowed between
`ALNUM` and the symbol. This is shown expanded for clarity.

The `WHERE_EXP` construct is a special case, as will be explained in its
section.


### Declarations blocks

With explicit begin and end boundaries.

        LOCAL_DECL   = "local" … "in" … "end"
        SRPCOND_DECL = SRPCOND … "#then"? … SRPELCOND* … "#else"? … "#endif"


Note `"let" … "in" … "end"` too, contains declarations, in its first part,
although this first part may be empty and the construct is an expression.


### Declarations

With explicit or implied semicolon:

        ASSUME_DECL =           ASSUME … "=" … ";"?
        CLASSDEC_DECL =     "classdec" … ":"? … ";"?
        EXTCODE_DECL =       "extcode" … ";"?
        EXTERN_DECL =         "extern" … ";"?
        EXTTYPE_DECL =       "exttype" … ";"?
        EXTVAR_DECL =         "extvar" … ";"?
        FIXITY_DECL =           FIXITY … ";"?
        IMPLEMENT_DECL =     IMPLEMENT … ";"?
        NONFIX_DECL =         "nonfix" … ";"?
        OVERLOAD_DECL =     "overload" … "with" … ";"?
        REASSUME_DECL =       REASSUME … ";"?
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
semicolon (it may visually looks similar).

Semicolon ended constructs with all empty parts are a special case: it does
end on its own but with what follows it and contains it. Ex. `static fn ():
int` is a `STATIC_DECL` containing the `FUN_DECL` which follows it. In
particular, the `REC_DECL` must only appears as such, ex. as `val rec a = …`
or `macdef rec …`, and `STATIC_DECL` (and not only) can only contains another
declaration. Remember the rules given here so far, are just an outline, there
are additional validity conditions required by the language.


ABSTYPE_DECL
------------------------------------------------------------------------------

        ABSTYPE_DECL = ABSTYPE … "and"* … ";"?

Tags: declaration; static; abstract; type;

Where `ABSTYPE` may be one of:

  * `"abstbox"`
  * `"abstype"`
  * `"abst@ype"`
  * `"abst0ype"`
  * `"abstflat"`
  * `"absprop"`
  * `"absview"`
  * `"absviewtype"`
  * `"absvtbox"`
  * `"absvtype"`
  * `"absvt@ype"`
  * `"absviewt@ype"`
  * `"absviewt0ype"`
  * `"absvt0ype"`
  * `"absvtflat"`

Abstract prop, type, view or viewtype. These are special cases of
`STACST_DECL` which is more versatile but less expresses the intent.


ADDRAT_EXP
------------------------------------------------------------------------------

        ADDRAT_EXP = "addr@" … IMPEND

Tags: expression; dynamic;

Given a `var` named `v`, `addr@ v` returns the address of `v` of sort `addr`.
A proof of the view of something at that location will also be needed to make
something out of it. See also `VIEWAT_EXP`.

Example:

        var i:int = 0
        val i_ref = ref_make_viewptr{int}(view@(i) | addr@(i))


ASSUME_DECL
------------------------------------------------------------------------------

        ASSUME_DECL = ASSUME … ";"?

Tags: declaration; static; abstract;

Where `ASSUME` may be one of:

  * `"assume"`
  * `"absimpl"`

Assume equality of two static abstract constants of the same sort. See also
`REASSUME_DECL`.

Example:

        absprop p
        absprop q
        assume p = q

        abstype t
        abstype u
        assume t = u


ATLBRACE_EXP
------------------------------------------------------------------------------

        ATLBRACE_EXP = "@{" … "}"

Tags: expression; static; dynamic; flat;

Expression for flat records types and values. It has two forms, one defining a
type (static) and one defining a value of that type (dynamic). The sort
of a flat record is `t@ype`.

Example:

        typedef t = @{a=int, b=int}
        val u = @{a=1, b=2}
        val v:t = @{a=1, b=2}
        val x = u.a


The field names may be identifiers or natural numbers expressed as decimal.
When all fields are numbers and starts at zero and increase one by one, a flat
tuple may be used instead. A flat tuple is a special case of flat record. See
also `ATLPAREN_EXP`.

Example:

        typedef t = @{1=int, 2=int, a=int, b=int}
        extern val v:t
        val x = v.a
        val y = v.1


ATLBRACKET_EXP
------------------------------------------------------------------------------

        ATLBRACKET_EXP = "@[" … "]"

Tags: expression; static; dynamic; flat;

Expression for flat one‑dimension arrays types and values. It has two forms,
one defining a type (static) and one defining a value of that type (dynamic).
The sort of a flat array is `t@ype`.

The expression `@[t][n]` means the type of an array of `n` elements of type
`t`. The expression `@[t](a, b, …)` (without really a “…”) means a literal
for an array of elements of type `t` initialized with `a`, `b` and so on.

Example:

        typedef t = @[int][3]
        var v:t = @[int](1, 2, 3)
        val a = v[0]

An array type is mono–dimensional only, even if you don’t get a syntax error
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

Tags: expression; static; dynamic; flat;

Expression for flat tuples types and values. It has two forms, one defining a
type (static) and one defining a value of that type (dynamic).  The sort
of a flat tuple is `t@ype`.

Example:

        typedef t = @(int, int)
        val u = @(1, 2)
        val v:t = @(1, 2)


The field names are natural numbers, starting at zero and increasing one by
one. Field selectors must be expression using the decimal notation, no other
base is allowed. A field selector is a special lexical unit. A flat tuple
is a special case of flat record. See also `ATLBRACE_EXP`.

Example:

        typedef t = @(int, char)
        val u = @(1, 'a')
        val v:t = @(1, 'a')
        val i = u.0
        val c = u.1


BEGIN_EXP
------------------------------------------------------------------------------

        BEGIN_EXP = "begin" … "end"

Tags: expression; dynamic; void;

Expression of void type. It contains a sequence of void expressions,
semicolon separated. Unlike with declarations, the semicolons are required.
There may be extraneous semicolons at the end. The same can be written
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

Tags: expression; dynamic; macro;

Borrowed from LISP’s back‑quote notation, used in macro definition and
invocation to treat whatever "…" is, frozen after binding resolution. The "…"
part must be a valid ATS2 syntactic sub‑tree; as an example, it may not
contain an unclosed expression, hence in that regard and except for freezing
and binding resolution, it is like with `SRPDEFINE_DECL`. See also
`COMMALPAREN_EXP` and `MACDEF_DECL`.

The identifiers used in the expression, must be dynamic identifiers.

Example:

        val n = 1
        macrodef m = `(n + n)  // Frozen, however binding resolved.
        val n = 2
        val a:int(2) = ,(m)    // Still 1 + 1, not 2 + 2.

        val n = 1
        #define M n + n        // Not frozen.
        val n = 2
        val a:int(4) = M       // 2 + 2, not 1 + 1 any more.

        #define M2 j + j       // No error since no binding resolution.
        macrodef m2 = `(i + i) // Error, since unresolved binding.

        macrodef m = `(println! "Test.")  // Not evaluated right now.
        implement main0() = begin
           ,(m);                          // Evaluated here.
           ,(m);                          // Evaluated one more time here.
        end


CASE_EXP
------------------------------------------------------------------------------

        CASE_EXP = CASE … "of" … "|"* … IMPEND

Tags: expression; dynamic;

Where `CASE` is one of:

  * `"case"` for warnings when coverage is not exhaustive.
  * `"case+"` for errors when coverage is not exhaustive.
  * `"case-"` for no static check about pattern coverage.

Dynamic patterns guarded expressions, borrowed from ML/SML. The static
counter‑part is `SCASE_EXP`.

The first part, contains the expression to be matched with patterns. The
second part which may be multiple `|` separated, contains the patterns and
the associated expressions. The repeatable second part (and last third part)
has its own inner syntax with a richer semantic than the ML/SML counter part;
this will be documented later. For friendliness, an extraneous `|` may
appears before the first pattern.

Example:

        val b:bool = true

        val c:int =
          case b of
          | false => 0
          | true => 1

        datatype tree =
          | Leaf
          | Left of tree
          | Right of tree
          | Left_Right of (tree, tree)

        val t:tree = Leaf

        val count:int =
          case t of
          | Leaf() => 0
          | Left(_) => 1
          | Right(_) => 1
          | Left_Right(_, _) => 2


**Warning:** nullary constructors in patterns of a `case` expression, must be
written with parentheses for distinguishing with pattern variables. Without
parentheses, what may looks like to be a constructor pattern will in reality
be a pattern variable. You may have made this error if you have a message
from Postiats saying “this pattern match clause is redundant”.

Example:

        datatype t = C | D

        val c = C  // No parentheses is OK here.

        val b:bool =
          case c of
          | C => true // Not the intent: C is a pattern variable!
          | D => false

        val b:bool =
          case c of
          | C() => true // The intent: C() refers to the constructor.
          | D() => false


Three different keywords for three coverage checking modes at compile‑time.
In any case, a failure to find a matching clause at run‑time ends in a
run‑time error (program execution stops).

Example:

        datatype t = C1 | C2

        val c = C2

        val b = case- c of C1() => true
        // Not compile‑time message and run‑time error.

        val b = case c of C1() => true
        // Compile‑time warning and run‑time error.

        val b = case+ c of C1() => true
        // Compile‑time error.


CLASSDEC_DECL
------------------------------------------------------------------------------

        CLASSDEC_DECL = "classdec" … ":"? … ";"?

Tags: declaration; static;

Defines classes relations. A definition is of the sort `cls` and static values
of the sort `cls` has an `<=` operator. Static values of the sort `cls` may
be used as type index.

Example:

        classdec mime_type       // Defines a root.
        classdec text: mime_type // Defines a relation: text <= mime_type.
        classdec html: text      // html <= text.
        classdec xml: text       // xml <= text.

        abstype class(c:cls)
        abstype file(c:cls) = [c <= mime_type] class(c)


COMMALPAREN_EXP
------------------------------------------------------------------------------

        COMMALPAREN_EXP = ",(" … ")"

Tags: expression; dynamic; macro;

Borrowed from LISP, this is used with macro definition and application, to
require evaluation of a  `BQUOTELPAREN_EXP` back‑quoted expression. See also
`MACDEF_DECL`.

Example:

        macrodef m = `(println! "Test.")

        implement main0() = begin
           ,(m); // Evaluation occurs here.
        end

A comma‑quoted expression can only be applied on or in a back‑quoted
expression.

Example:

        val a = ,(`(1)) // OK.
        val b = ,(1)    // Error.

A comma‑quoted expression yields an ATS2 “code” fragment from an ATS2
syntactic node, the latter being created using a back‑quoted expression.


DATASORT_DECL
------------------------------------------------------------------------------

        DATASORT_DECL = "datasort" … "and"* … ";"?

Tags: declaration; static;

Provides the only way to define a new sort with constants of that sort. The
static equality operator `==` is available for these constants. As with any
other static values, these constants may be used as type index. With the `and`
keyword, multiple sorts referring to each others may be defined. See also
`DATATYPE_DECL` for the dynamic counterpart. The constants can be matched by
an `SCASE_EXP` which is a dynamic expression although its domain is in the
static; this is done usually for proof value. When all constructors are
nullary, it is like an enumeration (a common SML idiom).

Example:

        datasort three_state =
          | On
          | Off
          | High_Impedance

        abstype state(s:three_state)

        fn is_on {s:three_state} (v: state(s)): bool =
          scase s of
            | On() => true
            | Off() => false
            | High_Impedance() => false


DATATYPE_DECL
------------------------------------------------------------------------------

        DATATYPE_DECL = DATATYPE … "and"* … ";"?

Tags: declaration; static; algebraic; dynamic; constructor;

Where `DATATYPE` may be one of:

  * `"datatype"`
  * `"dataprop"`
  * `"dataview"`
  * `"dataviewtype"`
  * `"datavtype"`

Defines an algebraic type of prop, type, view or viewtype sort. The types
introduce static identifiers but the constructors introduce dynamic
identifiers, hence it is both static and dynamic. There is no associated
versatile variant as there are with `ABSTYPE_DECL` and `TYPEDEF_DECL`. See
also `DATASORT_DECL` for the static counterpart. The dynamic constructors
can be matched by a `CASE_EXP`. When all constructors are nullary, it is
like an enumeration (a common SML idiom).

Example:

        datatype natural =
          | Zero
          | Succ of natural

        val n: natural = Succ(Succ(Zero))

        fun to_int(n: natural): int =
          case+ n of
            | Zero() => 0
            | Succ(n') => 1 + to_int(n')


EXCEPTION_DECL
------------------------------------------------------------------------------

        EXCEPTION_DECL = "exception" … "and"* … ";"?

Tags: declaration; dynamic; exception;

Very like a `DATATYPE_DECL`, except it only defines constructors, not an
associated type, so it only defines dynamic identifiers. It also has no
alternative (`|`) parts: since it does not introduce a type, it would be
useless. An instance of an exception is of sort `viewtype`, that is, of a
(anonymous) linear type. It is not usually matched by a `CASE_EXP` like with
data types, rather a `TRY_EXP`. An instance is thrown/raised with the
`"$raise"` special function. Raising exceptions requires memory allocation on
the stack using “alloca”. Raising exceptions is known to possibly cause some
memory leaks.

Example:

        exception IOError of int

        fn input_fd(path: string): int =
          if path = "stdin" then 0
          else $raise IOError(1)

        val fd =
          try input_fd("foo")
          with ~IOError(_) => (println! "Oops."; 0)


EXTCODE_DECL
------------------------------------------------------------------------------

        EXTCODE_DECL = "extcode" … ";"?

Tags: declaration; static; dynamic;

Embed literal foreign language snuppets in the generated target language file.

This may as much impact the static and the dynamic, since even types may be
defined this way. For the notation, see “External code” in “lexemes-guide.md”.


EXTERN_DECL
------------------------------------------------------------------------------

        EXTERN_DECL = "extern" … ";"?

Tags: declaration; static; dynamic; binding;

Versatile construct covering the use cases of `EXTTYPE_DECL`, `EXTVAR_DECL`,
`STATIC_DECL`, which are in the while, explained here.

These four examples:

        extern fn f(): int            // Declare an fn signature.
        extern val v: int             // Declare a val signature.
        extern typedef "c_type" = int // Export a type to the target language.
        extern var "c_var" = 0        // Assign a target language variable.

Mean the same as these four ones:

        static fn f(): int
        static val v: int
        extype "c_type" = int
        extvar "c_var" = 0

The `extern` form may be more readable for `fn` and `val`. The `extype` and
`extvar` forms may be more readable than the `extern` form. The `extype` form
can also be used with types of other sorts:

        viewtypedef vt = int
        extern viewtypedef "c_type" = vt // Same as below.
        extype "c_type" = vt             // Same as above.

In addition, note the two special functions `"$extype"` and `"$extval"` which
are not keywords, for importing:

        typedef t = $extype "c_type" // Import a target language type.
        val v = $extval(t, "c_var")  // Import a target language value.

Note it is `$extval` and not `$extvar` (which does not exists).


EXTTYPE_DECL
------------------------------------------------------------------------------

        EXTTYPE_DECL = "exttype" … ";"?

Tags: declaration; static; binding;

See `EXTERN_DECL`.


EXTVAR_DECL
------------------------------------------------------------------------------

        EXTVAR_DECL = "extvar" … ";"?

Tags: declaration; dynamic; binding;

See `EXTERN_DECL`.


FIX_EXP
------------------------------------------------------------------------------

        FIX_EXP = "fix" … IMPEND

Tags: expression;


FIXITY_DECL
------------------------------------------------------------------------------

        FIXITY_DECL = FIXITY … ";"?

Tags: declaration; dynamic;

Where `FIXITY` may be one of:

  * `"infix"`
  * `"infixl"`
  * `"infixr"`
  * `"prefix"`
  * `"postfix"`


FOLDAT_EXP
------------------------------------------------------------------------------

        FOLDAT_EXP = "fold@" … IMPEND

Tags: expression;


FOR_EXP
------------------------------------------------------------------------------

        FOR_EXP = "for" … IMPEND

Tags: expression;


FORSTAR_EXP
------------------------------------------------------------------------------

        FORSTAR_EXP = "for*" … "=>" … IMPEND

Tags: expression;


FREEAT_EXP
------------------------------------------------------------------------------

        FREEAT_EXP = "free@" … IMPEND

Tags: expression;


FUN_DECL
------------------------------------------------------------------------------

        FUN_DECL = FUN … "and"* … ";"?

Tags: declaration; dynamic;

Where `FUN` is one of:

  * `"fn"`
  * `"fnx"`
  * `"fun"`
  * `"prfn"`
  * `"prfun"`
  * `"praxi"`
  * `"castfn"`


HASHLBRACKET_EXP
------------------------------------------------------------------------------

        HASHLBRACKET_EXP = "#[" … "]"

Tags: expression;


IDENT_arr_EXP
------------------------------------------------------------------------------

        IDENT_arr_EXP = ALNUM"[" … "]"

Tags: expression;


IDENT_tmp_EXP
------------------------------------------------------------------------------

        IDENT_tmp_EXP = ALNUM"<" … ">"

Tags: expression;


IFCASE_EXP
------------------------------------------------------------------------------

        IFCASE_EXP = "ifcase" … "|"* … IMPEND

Tags: expression;


IF_EXP
------------------------------------------------------------------------------

        IF_EXP = "if" … then … "else"? … IMPEND

Tags: expression;


IMPLEMENT_DECL
------------------------------------------------------------------------------

        IMPLEMENT_DECL = IMPLEMENT … ";"?

Tags: declaration; dynamic;

Where `IMPLEMENT` is one of:

  * `"implmnt"`
  * `"implement"`
  * `"primplement"`
  * `"primplmnt"`


LAM_EXP
------------------------------------------------------------------------------

        LAM_EXP = "lam" … IMPEND

Tags: expression;


LBRACE_EXP
------------------------------------------------------------------------------

        LBRACE_EXP = "{" … "}"

Tags: expression;


LBRACKET_EXP
------------------------------------------------------------------------------

        LBRACKET_EXP = "[" … "]"

Tags: expression;


LET_EXP
------------------------------------------------------------------------------

        LET_EXP = "let" … "in" … "end"

Tags: expression;


LOCAL_DECL
------------------------------------------------------------------------------

        LOCAL_DECL   = "local" … "in" … "end"

Tags: declaration; static; dynamic;


LPAREN_EXP
------------------------------------------------------------------------------

        LPAREN_EXP = "(" … ")"

Tags: expression;

For sequence of void expressios, see also `BEGIN_EXP`.


MACDEF_DECL
------------------------------------------------------------------------------

        MACDEF_DECL = MACDEF … "and"* … ";"?

Tags: declaration; dynamic; macro;

Where `MACDEF` may be one of:

  * `"macdef"` for user friendly short form, explained below.
  * `"macrodef"` for raw long form, explained below.

LISP‑like macro names are dynamic identifiers.

Borrowed from LISP, defines macro which like with `SRPDEFINE_DECL` are defined
with valid syntactic sub‑tree node, but which unlike with the latter, requires
binding to be resolvable and allows to control where evaluation occurs.
`BQUOTELPAREN_EXP` is used for frozen expressions and `COMMALPAREN_EXP` is
used for evaluated expressions.

`macrodef` is a more raw form than `macdef` or `macdef` is a special case
of `macrodef`. A `macdef` is implicitly back‑quoted at the time of its
definition and its evaluation is implicitly requested at the macro name is
referred to. With `macrodef`, both must be explicitly specified.

Example:

        macrodef m = `(println! "Test m.")  // Explicit freeze request.
        macdef n = (println! "Test n.")     // `(…) is implicit

        implement main0() = begin
           ,(m);                            // Explicit evaluation request.
           n;                               // ,(…) is implicit
        end

LISP‑like macros, like `SRPDEFINE_DECL` C‑like macros, are scoped.

Example:

        local
           macdef n = 1
           val a:int = n  // OK
        in
           (* empty *)
        end

        val b:int = n     // Error.

LISP‑like macros, like `SRPDEFINE_DECL` C‑like macros, may have arguments. The
arguments must be ATS2 syntactic nodes, which are created with back‑quote
expressions. It may turns into many back‑quotations, hence the friendliness of
`macdef` over `macrodef` becomes clear.

Example:

        macrodef succ(x) = `(,(x) + 1)
        val a:int(2) = ,(succ `(1))      // Argument explicitly back‑quoted.

        macdef succ(x) = ,(x) + 1
        val a:int(2) = succ 1            // Argument implicitly back‑quoted.


NONFIX_DECL
------------------------------------------------------------------------------

        NONFIX_DECL = "nonfix" … ";"?

Tags: declaration; dynamic;


OP_EXP
------------------------------------------------------------------------------

        OP_EXP = "op" … IMPEND

Tags: expression;


OVERLOAD_DECL
------------------------------------------------------------------------------

        OVERLOAD_DECL = "overload" … "with" … ";"?

Tags: declaration; dynamic;


QUOTELBRACE_EXP
------------------------------------------------------------------------------

        QUOTELBRACE_EXP = "'{" … "}"

Tags: expression;


QUOTELBRACKET_EXP
------------------------------------------------------------------------------

        QUOTELBRACKET_EXP = "'[" … "]"

Tags: expression;


QUOTELPAREN_EXP
------------------------------------------------------------------------------

        QUOTELPAREN_EXP = "'(" … ")"

Tags: expression;


REASSUME_DECL
------------------------------------------------------------------------------

        REASSUME_DECL = REASSUME … ";"?

Tags: declaration; static; abstract;

Where `REASSUME` may be one of:

  * `"reassume"`
  * `"absreimpl"`

Recall a previous assumption of equality of two static abstract constants. See
also `ASSUME_DECL`.

Example:

        absprop p
        absprop q
        assume p = q

        abstype t
        abstype u
        assume t = u

        reassume p
        reassume t


REC_DECL
------------------------------------------------------------------------------

        REC_DECL = "rec" … "and"* … ";"?

Tags: declaration;


SCASE_EXP
------------------------------------------------------------------------------

        SCASE_EXP = "scase" … "of" … "|"* … IMPEND

Tags: expression;


SIF_EXP
------------------------------------------------------------------------------

        SIF_EXP = "sif" … "then" … "else" … IMPEND

Tags: expression;


SORTDEF_DECL
------------------------------------------------------------------------------

        SORTDEF_DECL = "sortdef" … "and"* … ";"?

Tags: declaration; static;


SRPASSERT_DECL
------------------------------------------------------------------------------

        SRPASSERT_DECL = "#assert" … ";"?

Tags: declaration;


SRPCODEGEN2_DECL
------------------------------------------------------------------------------

        SRPCODEGEN2_DECL = "#codegen2" … ";"?

Tags: declaration;


SRPCOND_DECL
------------------------------------------------------------------------------

        SRPCOND_DECL = SRPCOND … "#then"? … SRPELCOND* … "#else"? … "#endif"

Tags: declaration;

Where `SRPCOND` may be one of:

  * `"#if"`
  * `"#ifdef"`
  * `"#ifndef"`

And where `SRPELCOND` may be one of:

  * `"#elif"`
  * `"#elifdef"`
  * `"#elifndef"`


SRPDEFINE_DECL
------------------------------------------------------------------------------

        SRPDEFINE_DECL = "#define" … ";"?

Tags: declaration; static; dynamic; macro;

C‑like macro names are dynamic identifiers.

Borrowed from C, defines a weak macro. Unlike `MACDEF_DECL` LISP‑like macros,
C‑like macros does not do binding resolution, identifiers appearing in it
are just identifiers. A consequence of this is that unlike LISP‑like macros,
C‑like macros may resolve referring to static identifiers.

Example:

        #define T int
        val a:T = 1

        macdef T = int   // Error.

However, C‑like macro are not expanded in static declarations, only in
dynamic declarations, refering to static or dynamic identifiers.

Example:

        #define V a
        val a:int = 0
        val b:int = V

        #define T int
        val a:T = 1

        #define S type
        stacst t:S       // Error.

        #define S t@ype  // Additionally, this is a syntax error.

Unlike LISP‑like macros, C‑like macros don’t allow controlling evaluation,
there is no evaluation at the time of the definition, evaluation occurs at the
time the macro is referred to by name, doing binding resolution in the context
where the reference occurs.

Example:

        val n = 1
        #define N n
        val n = 2
        val a:int(2) = N // Use the n available from here.

Like with LISP‑like macros and unlike with original C macros, the macro’s body
is not raw text substitution, it must be a valid syntactic sub‑tree …

Example:

        #define N (1  // Error.

… and the expression is like implicitly wrapped in parentheses when it is
evaluated.

Example:

        #define N 1 + 2
        val a:int(12) = 4 * N  // Like 4 * (1 + 3) not like 4 * 1 + 2.

Unlike original C macros and like LISP‑like macros, C‑like macros are
scoped.

Example:

        local
           #define N 1
           val a:int = N  // OK.
        in
           (* empty *)
        end

        val b:int = N  // Error.

C‑like macros may have arguments.

Example:

        #define SUCC(x) x + 1
        val a:int(2) = SUCC 1


SRPDYNLOAD_DECL
------------------------------------------------------------------------------

        SRPDYNLOAD_DECL = SRPDYNLOAD … ";"?

Tags: declaration; dynamic;

Where `SRPDYNLOAD` is one of:

  * `"dynload"`
  * `"#dynload"`


SRPERROR_DECL
------------------------------------------------------------------------------

        SRPERROR_DECL = "#error" … ";"?

Tags: declaration;


SRPINCLUDE_DECL
------------------------------------------------------------------------------

        SRPINCLUDE_DECL = "#include" … ";"?

Tags: declaration;


SRPPRAGMA_DECL
------------------------------------------------------------------------------

        SRPPRAGMA_DECL = "#pragma" … ";"?

Tags: declaration;


SRPPRERR_DECL
------------------------------------------------------------------------------

        SRPPRERR_DECL = "#prerr" … ";"?

Tags: declaration;


SRPPRINT_DECL
------------------------------------------------------------------------------

        SRPPRINT_DECL = "#print" … ";"?

Tags: declaration;


SRPREQUIRE_DECL
------------------------------------------------------------------------------

        SRPREQUIRE_DECL = "#require" … ";"?

Tags: declaration;


SRPSTALOAD_DECL
------------------------------------------------------------------------------

        SRPSTALOAD_DECL = SRPSTALOAD … ";"?

Tags: declaration; static; dynamic;

Where `SRPSTALOAD` may be one of:

  * `"staload"`
  * `"#staload"`


SRPUNDEF_DECL
------------------------------------------------------------------------------

        SRPUNDEF_DECL = "#undef" … ";"?

Tags: declaration;


STACST_DECL
------------------------------------------------------------------------------

        STACST_DECL = STACST … "and"* … ";"?

Tags: declaration; static; abstract;

Where `STACST` may be one of:

  * `"sta"`
  * `"stacst"`

Abstract static expression. Abstract: the value does not matter and there is
none, only the introduced identity (name) and its declared sort, do, and
possibly its properties defined as axioms. The constant is expected to be of a
predicative sort; although doing otherwise will not end in a syntax error from
Postiats, it is not supported.

This is mainly used to name a constant to which some axioms will be attached,
also to be able to have readable name in expressions exported to constraint
solvers.

Example:

        stacst c: int
        static praxi c_lemma(): [speed:int; speed < c] void


STADEF_DECL
------------------------------------------------------------------------------

        STADEF_DECL = "stadef" … "and"* … ";"?

Tags: declaration; static; aliasing;

Versatile static expression aliasing. `TYPEDEF_DECL` has more specialized
keywords better expressing the intent.


STATIC_DECL
------------------------------------------------------------------------------

        STATIC_DECL = "static" … ";"?

Tags: declaration; dynamic;


SYMELIM_DECL
------------------------------------------------------------------------------

        SYMELIM_DECL = "symelim" … ";"?

Tags: declaration; dynamic;


SYMINTR_DECL
------------------------------------------------------------------------------

        SYMINTR_DECL = "symintr" … ";"?

Tags: declaration; dynamic;


SYMLT_EXP
------------------------------------------------------------------------------

        SYMLT_EXP = SYMLT … ">"

Tags: expression;

Where `SYMLT` may be one of:

  * `":<"`
  * `"=<"`
  * `"-<"`


TKINDEF_DECL
------------------------------------------------------------------------------

        TKINDEF_DECL = "tkindef" … ";"?

Tags: declaration; static;


TRY_EXP
------------------------------------------------------------------------------

        TRY_EXP = "try" … "with" … IMPEND

Tags: expression;


TYPEDEF_DECL
------------------------------------------------------------------------------

        TYPEDEF_DECL = TYPEDEF … "and"* … ";"?

Tags: declaration; static; aliasing; type;

Where `TYPEDEF` may be one of:

  * `"propdef"`
  * `"typedef"`
  * `"viewdef"`
  * `"viewtypedef"`
  * `"vtypedef"`

Prop, type, view or viewtype expression aliasing. Specialized cases of
`STADEF_DECL` which is more versatile but less expresses the intent.


VAL_DECL
------------------------------------------------------------------------------

        VAL_DECL = VAL … "and"* … ";"?

Tags: declaration; dynamic;

Where `VAL` is one of:

  * `"val"`
  * `"val+"`
  * `"val-"`
  * `"prval"`


VAR_DECL
------------------------------------------------------------------------------

        VAR_DECL = VAR … "and"* … ";"?

Tags: declaration; dynamic;

Where `VAR` is one of:

  * `"var"`
  * `"prvar"`


VIEWAT_EXP
------------------------------------------------------------------------------

        VIEWAT_EXP = "view@" … IMPEND

Tags: expression; dynamic;

Given a `var` `v:t`, `view@ v` returns a proof of a view of a `t` at `v`.
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

Tags: expression;


WHILESTAR_EXP
------------------------------------------------------------------------------

        WHILESTAR_EXP = "while*" … "=>" … IMPEND

Tags: expression;

