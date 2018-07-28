ATS2 big lines syntax
==============================================================================

The big lines of ATS2 syntax is described here with a purposely simple but
real model. The model was checked running a rather formal parser on a
reasonably large and representative set of sources. It defines a boundary
based segmentation of ATS2 sources. Each rule is in the form of a product name
followed by an equal‑sign follow by boundaries delimiting “…” parts which may
contains “any” sequence of tokens. The “…” are there to say there may be
anything between two boundaries, it may even be empty. Matching these rules is
not enough to be valid ATS2, but these rules are enough to have a grasp on a
source file and have a quick and easy overview of ATS2 syntax. These rules are
also enough for a “first‑pass” or “first‑level” parsing of the ATS2 language.

The keywords are subject to the lexical rules described in “lexemes-guide.md”.

The semantic description coming with the constructs, is intended to be terse.
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

**Repeatable part boundaries:** `SCASE_EXP = scase … of … "|"* … IMPEND`
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
  6. Declarations, with implied end, implicitly containing the next one.


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
        FOLDAT_EXP =     "fold@" … IMPEND
        FOR_EXP =          "for" … IMPEND
        FORSTAR_EXP =     "for*" … "=>" … IMPEND
        FREEAT_EXP =     "free@" … IMPEND
        IFCASE_EXP =    "ifcase" … "|"* … IMPEND
        IF_EXP =            "if" … then … "else"? … IMPEND
        LAM_EXP =            LAM … IMPEND
        OP_EXP =            "op" … IMPEND
        SCASE_EXP =      "scase" … "of" … "|"* … IMPEND
        SIF_EXP =          "sif" … "then" … "else" … IMPEND
        TRY_EXP =          "try" … "with" … IMPEND
        VIEWAT_EXP =     "view@" … IMPEND
        WHILE_EXP =      "while" … IMPEND
        WHILESTAR_EXP = "while*" … "=>" … IMPEND


`ALNUM"["` and `ALNUM"<"` are atomic lexical units, no space is allowed
between `ALNUM` and the symbol. This is shown expanded for clarity.

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
        EXTCODE_DECL =         EXTCODE … ";"?
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


With implied end, implicitly containing the next declaration:

        EXTERN_DECL = "extern" … IMPEND
        STATIC_DECL = "static" … IMPEND


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

Tags: declaration; static; abstract; type; proof;

Where `ABSTYPE` may be one of:

  * `"abstype"` — abstract boxed type, i.e. of sort `type`
  * `"abst@ype"` — abstract flat type, i.e. of sort `t@ype`
  * `"absprop"` — abstract proposition, i.e. of sort `prop`
  * `"absview"` — abstract view, i.e. of sort `view`
  * `"absviewtype"` — abstract flat type view, i.e. of sort `viewtype`
  * `"absviewt@ype"` — abstract boxed type view, i.e. of sort `viewt@ype`
  * `"abstbox"` — synonymous with `"abstype"`
  * `"abst0ype"` — synonymous with `"abst@ype"`
  * `"abstflat"` — synonymous with `"abst@ype"`
  * `"absvtbox"` — synonymous with `"absviewtype"`
  * `"absvtype"` — synonymous with `"absviewtype"`
  * `"absvt@ype"` — synonymous with `"absviewt@ype"`
  * `"absviewt0ype"` — synonymous with `"absviewt@ype"`
  * `"absvt0ype"` — synonymous with `"absviewt@ype"`
  * `"absvtflat"` — synonymous with `"absviewt@ype"`

Abstract type of various sorts. Introduces impredicative abstract constants.
These are comparable to `STACST_DECL` which is for predicative abstract
constants. Usually used to declare relations or properties. When an abstract
type is defined, it may later be implemented using an `ASSUME_DECL`, which is
usually the case when the type is intended to be data. When an abstract type
is defined, axioms may later be stated about it or it may be used for proofs
returned by functions, which is usually the case when the type is intended to
be a proof. Abstract types may be declared to get sort index(es), which is
usually the case when the abstract type is intended to be a proof, while less
common when the abstract type intended to be data, the latter most commonly
standing on its own.

Example with `abstype`:

        abstype tree                      // Abstract boxed definition.
        extern fun size(tree): int        // Declare property or method.
        datatype ml_tree =                // Prepare an implementation.
          | leaf
          | node1 of ml_tree
          | node2 of (ml_tree, ml_tree)
        absimpl tree = ml_tree            // Declare ml_tree implements tree.
        implement size(ml_tree): int = …  // Implement declared property.

        abstype nat(int)                  // May also get index(es).

Example with `abst@ype`:

        abst@ype file                     // Abstract flat definition.
        extern fn read(file): char        // Declare property or method.
        absimpl file = int                // Declare a fd implements file.
        implement read(file): char = …    // Implement declared property.

        abst@ype nat(int)                 // May also get index(es).

Example with `absprop`:

        datasort class = Class            // Define sort for index.
        absprop INHERIT(class, class)     // Define relation.
        extern praxi inherit_lemma        // State axiom on relations.
           {a, b, c: class}
           (INHERIT(b, a), INHERIT(c, b)): INHERIT(c, a)

        absprop NAT                       // May also get no index.


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

Tags: declaration; static; abstract; type;

Where `ASSUME` may be one of:

  * `"absimpl"`
  * `"assume"` — synonymous with `"absimpl"`

Assume equality of two static definitions. The first one is abstract, the
second one is typically not. The second one must be of the same sort or of a
more general sort than the first one. It is used to state the equality between
an abstract definition and a concrete implementation of it.

The equality is scoped, outside the scope where it is declared, it is not
visible. It can be pulled from another scope using `REASSUME_DECL`.

The requirement of being of the same or more general sort, implies as an
example, a boxed abstract type can only be implemented by a boxed concrete
type.

Example:

        abst@ype file
        absimpl file = int // Implement file with a POSIX file handle.

The implementing definition may be of an equal sort or of a more general sort
than the abstract implemented one. For sorts relations, see “sorts-guide.md”.

Example:

        abst@ype aft
        datatype bt = C
        absimpl aft = bt // Boxed type can implement abstract flat type.

The above is valid, because the `type` sort is more general than the `t@ype`
sort, hence a type of the `type` sort can implement a type of the `t@ype`
sort.

As soon as a concrete implementation is associated to an abstract type, it not
abstract any‑more.

Example:

        abst@ype file
        absimpl file = int
        absimpl file = int // Error here, file is not abstract anymore.


ATLBRACE_EXP
------------------------------------------------------------------------------

        ATLBRACE_EXP = "@{" … "}"

Tags: expression; static; dynamic; flat;

Expression for flat record types and values. It has two forms, one defining a
type (static) and one defining a value of that possibly anonymous type
(dynamic). The sort of a flat record is `t@ype`.

Example:

        typedef t = @{a=int, b=int}
        val u = @{a=1, b=2}
        val v:t = @{a=1, b=2}
        val x = u.a


The field names may be identifiers or natural numbers, the latter expressed as
decimal. When all field names are numbers and starts at zero then increasing
one by one, a flat tuple may be used instead. A flat tuple is a special case
of flat record. See also `ATLPAREN_EXP`.

Example:

        typedef t = @{1=int, a=int}
        extern val v:t
        val x = v.a
        val y = v.1


ATLBRACKET_EXP
------------------------------------------------------------------------------

        ATLBRACKET_EXP = "@[" … "]"

Tags: expression; static; dynamic; flat;

Expression for flat one‑dimension array types and values. It has two forms,
one defining a type (static) and one defining a value of that possibly
anonymous type (dynamic). The sort of a flat array is `t@ype`.

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

The elements may be all initialized with the same value.

Example:

        typedef t = @[int][3]
        var v:t = @[int](5) // |1…2] is 5


ATLPAREN_EXP
------------------------------------------------------------------------------

        ATLPAREN_EXP = "@(" … ")"

Tags: expression; static; dynamic; flat;

Expression for flat tuple types and values. It has two forms, one defining a
type (static) and one defining a value of that possibly anonymous type
(dynamic). The sort of a flat tuple is `t@ype`.

Example:

        typedef t = @(int, int)
        val u = @(1, 2)
        val v:t = @(1, 2)


The field names are natural numbers, starting at zero and increasing one by
one. Field selectors must be expression using the decimal notation, no other
base is allowed. A field selector is a special lexical unit, no space is
allowed between the dot and the natural number. A flat tuple is a special case
of flat record. See also `ATLBRACE_EXP`.

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
using an `LPAREN_EXP`, but a `BEGIN_EXP` more expresses the intent when the
content is a sequence of operations all returning void.

Example:

        val () = begin print! "a"; println! "b" end
        val () = (print! "a"; println! "b") // Same as this.

        implement main0() = begin
           println! "Hello ...";
           println! "... world!";
        end

Although typically used for implementing function returning void, this
construct is a void expression which can be used anywhere a void expression is
expected, as show in the example above.

Declarations are not allowed here. If declarations are needed to implement a
void expression or function, a `LET_EXP` or a form of an `LBRACE_EXP` is to be
used instead.

Example:

        implement main0() =
           let val s = "Hello"
           in println! s
           end

Example:

        implement main0() = {
              val s = "Hello"
              val () = println! s
           }


BQUOTELPAREN_EXP
------------------------------------------------------------------------------

        BQUOTELPAREN_EXP = "`(" … ")"

Tags: expression; dynamic; macro;

Borrowed from LISP’s back‑quote notation, used in macro definition and
invocation to treat whatever "…" is, frozen after binding resolution. The "…"
part must be a valid ATS2 syntactic sub‑tree of an expression; as an example,
it may not contain an unclosed expression, hence in that regard and except for
freezing and binding resolution, it is like with `SRPDEFINE_DECL`. See also
`COMMALPAREN_EXP` and `MACDEF_DECL`.

The identifiers used in the expression, must be dynamic identifiers. The macro
evaluation must yield an expression, not a declaration.

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

Note although the example here use `macrodef`, in practice, `macdef` is most
commonly used.


CASE_EXP
------------------------------------------------------------------------------

        CASE_EXP = CASE … "of" … "|"* … IMPEND

Tags: expression; dynamic;

Where `CASE` is one of:

  * `"case"` for warnings when coverage is not exhaustive.
  * `"case+"` for errors when coverage is not exhaustive.
  * `"case-"` for no static check about pattern coverage.

Dynamic patterns guarded expressions, borrowed from ML/SML. For static
patterns, use `SCASE_EXP` instead.

The first part, contains the expression to be matched with patterns. The
second part which may be multiple `|` separated, contains the patterns and the
associated expressions. The repeatable second part has its own inner syntax
with a richer semantic than the ML/SML counterpart; this will be documented
later. For friendliness, an extraneous `|` may appears before the first
pattern.

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
be a pattern variable. You may have made this error if you get a message
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
In any case, a failure to find a matching clause at run‑time, ends in a
run‑time error (program execution stops).

Example:

        datatype t = C1 | C2

        val c = C2

        val b = case- c of C1() => true
        // No compile‑time message and run‑time error.

        val b = case c of C1() => true
        // Compile‑time warning and run‑time error.

        val b = case+ c of C1() => true
        // Compile‑time error.


CLASSDEC_DECL
------------------------------------------------------------------------------

        CLASSDEC_DECL = "classdec" … ":"? … ";"?

Tags: declaration; static; binding;

Defines classes relations. A definition is of the sort `cls` and static values
of the sort `cls` has an `<=` operator. The static constants so defined are to
be used as type indexes, typically aside an index of sort `addr`. Typically
used for binding with object‑oriented library, but not restricted to that.

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
require evaluation of a `BQUOTELPAREN_EXP` back‑quoted expression. See also
`MACDEF_DECL`.

Example:

        macrodef m = `(println! "Test.")

        implement main0() = begin
           ,(m); // Evaluation occurs here.
        end

A comma‑quoted expression can only be applied on or in, a back‑quoted
expression.

Example:

        val a = ,(`(1)) // OK.
        val b = ,(1)    // Error.

Additionally, it is required for using macro arguments.

Example:

        macdef sum(a, b) = ,(a) + ,(b)
        val a:int(5) = sum(2, 3)

A comma‑quoted expression yields an ATS2 expression source fragment from an
ATS2 syntactic node, the latter being created using a back‑quoted expression.


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

  * `"datatype"` — algebraic type of sort `type`
  * `"dataprop"` — algebraic type of sort `prop`
  * `"dataview"` — algebraic type of sort `view`
  * `"dataviewtype"` — algebraic type of sort `viewtype`
  * `"datavtype"` — synonymous with `"dataviewtype"`

Defines an algebraic type of various sorts. The types introduce static
identifiers but the constructors introduce dynamic identifiers, hence it is
both static and dynamic. There is no associated versatile variant as there are
with `ABSTYPE_DECL` and `TYPEDEF_DECL`. See also `DATASORT_DECL` for the
static counterpart. The dynamic constructors can be matched by a `CASE_EXP`.
When all constructors are nullary, it is like an enumeration (a common SML
idiom).

Example:

        datatype natural =
          | Zero
          | Succ of natural

        val n: natural = Succ(Succ(Zero))

        fun to_int(n: natural): int =
          case+ n of
            | Zero() => 0
            | Succ(n') => 1 + to_int(n')

There is no way to directly define an algebraic type of sort `t@ype`. However,
this should be possible indirectly, using discriminating index(es), proofs of
view and flat records.


EXCEPTION_DECL
------------------------------------------------------------------------------

        EXCEPTION_DECL = "exception" … "and"* … ";"?

Tags: declaration; dynamic; exception;

Very like a `DATATYPE_DECL`, except it only defines constructors, not an
associated type, so it only defines dynamic identifiers. It also has no
alternative (`|`) parts: since it does not introduce a type, it would be
useless. An instance of an exception is of sort `viewtype`, that is, of a
(anonymous) linear type. It is not usually matched by a `CASE_EXP` like with
data types, rather by a `TRY_EXP`. An instance is thrown/raised with the
`"$raise"` special function. Raising an exception uses memory allocation in
the background. Raising exceptions is known to possibly cause some memory
leaks, so don’t be surprised if you find some (anyway, using exceptions as few
as possible is always better).

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

        EXTCODE_DECL = EXTCODE … ";"?

Tags: declaration; static; dynamic;

`EXTCODE` is not a keyword, it’s a lexical unit started with `"%{"` and
ended with `"%}"` as explained in “External code” in “lexemes-guide.md”.

Embed literal foreign language snippets in the generated target language file.

This may as much impact the static and the dynamic, since even types may be
defined this way as with `EXTERN_DECL`. For the notation, see “External code”
in “lexemes-guide.md”. The single part must be empty, this declaration accepts
no content except the one in the `EXTCODE` literal.


EXTERN_DECL
------------------------------------------------------------------------------

        EXTERN_DECL = "extern" … IMPEND

Tags: declaration; static; dynamic; binding;

Versatile construct covering the use cases of `EXTTYPE_DECL`, `EXTVAR_DECL`,
`STATIC_DECL`, which are in the while, explained here.

These four examples …:

        extern fn f(): int            // Declare an fn signature.
        extern val v: int             // Declare a val signature.
        extern typedef "c_type" = int // Export a type to the target language.
        extern var "c_var" = 0        // Assign a target language variable.

… mean the same as these four ones:

        static fn f(): int
        static val v: int
        extype "c_type" = int
        extvar "c_var" = 0

The `extern` form may be more readable for `fn` and `val`. The `extype` and
`extvar` forms may be more readable than the `extern` form for types and
variables. The `extype` form can be used with types of any sort:

        viewtypedef vt = int
        extern viewtypedef "c_type" = vt // Same as below.
        extype "c_type" = vt             // Same as above.

In addition, there are two special functions `"$extype"` and `"$extval"` which
are not keywords, for importing:

        typedef t = $extype "c_type" // Import a target language type.
        val v = $extval(t, "c_var")  // Import a target language value.

Note it is `$extval`, not `$extvar` (which does not exist).


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


FIXITY_DECL
------------------------------------------------------------------------------

        FIXITY_DECL = FIXITY … ";"?

Tags: declaration; static; dynamic;

Where `FIXITY` may be one of:

  * `"infix"` — binary, non‑associative
  * `"infixl"` — binary, left associative
  * `"infixr"` — binary, right associative
  * `"prefix"` — unary, right associative
  * `"postfix"` — unary, left associative


An operator name may be symbolic or alphanumeric and multiple may be defined
at once:

Example:

        infix ++
        infix o
        infix -- ** p q

The function associated to an operator may be defined using an usual
definition or an overloading. The definition may be any definition: function,
macro, define, constructor, type … (see the relevant sections for each of
these). The arity of the definition must just be the same as implied by the
operator definition, that is binary for the infixes and unary for the pre and
postfixes. The underlying implementation can be invoked using the usual
function invocation syntax, with the `"op"` keyword to locally and temporary
cancel the syntactic status of the operator.

Example:

        infix o                       // Operator with an alphanumeric name.
        extern fn o(int, int): int
        val v = 1 o 2 // o(1, 2)
        val v = op o(1, 2)

        infix +++
        extern fn +++(int, int): int  // Function with a symbolic name.
        val v = 1 +++ 2
        val v = op +++(1, 2)

        infix p
        macdef p(a, b) = ,(a) + ,(b)  // Definition is a macro.
        val v = 1 p 2 // 1 + 2
        val v = op p(1, 2)

        infix q
        #define q(a, b) a * b         // Definition is a #define.
        val v = 1 q 2 // 1 * 2
        val v = op q(1, 2)

        infix r
        extern fn f(int, int): int
        overload r with f             // Definitiion added with overloading.
        val v = 1 r 2 // f(1, 2)
        val v = op r(1, 2)

        prefix ++
        datatype t = ++ of int
        val v = ++ 1         // ++ is a constructor used as a prefix operator.
        val v = op ++ 1
        val v = op ++(1)

        postfix --
        datatype u = -- of int
        val v = 1 --        // -- is a constructor used as a postfix operator.
        val v = op -- 1
        val v = op --(1)

        infix ->>
        typedef ->>(i:int, j:int) = [k:int; k == i + j] int(k)
        val v: 1 ->> 2 = 3            // ->> is a type as an infix operator.


Given two operators o1 and o2 and three expressions or literals e1, e2 and e3,
in “e1 o1 e2 o2 e3”, it must be decided which operator e2 will go to. Is it
“(e1 o1 e2) o2 e3” or is it “e1 o1 (e2 o2 e3)” ? If o1 has an higher priority
than o2, it will be the former, if o2 has an higher priority than o1, it will
be the latter. The priority may be given as a natural number in decimal
notation. It is optional and defaults to 0. If multiple operator are defined
at once, the priority applies to each operator being defined. The file
`$PATSHOME/prelude/fixity.ats` contains the priorities of the usual ATS2
operators. An operator priority, may also be specified to be that of another
operator: instead of the decimal, the name of the operator is given wrapped
in parentheses.

Example:

        infix 0 o1
        infix 1 o2

        extern fn o1(int, int): int
        extern fn o2(int, int): int

        val (e1, e2, e3) = (1, 2, 3)
        val v = e1 o1 e2 o2 e3 // Evaluated as e1 o1 (e2 o2 e3)

        infix (+) ++ -- // Same priority as the + operator
        infix ( * ) ** // Spaces needed here!


If priority cannot be resolved or an operator is syntactically erroneously
used, Postiats says “operator fixity cannot be resolved”. This occurs as an
example, when two infix operators has the same priority or as another example,
if a prefix operator is used as a postfix operator.

Example:

        infix b
        prefix p

        extern fn b(int, int): int
        extern fn p(int): int

        val (e1, e2, e3) = (1, 2, 3)
        val v = e1 b e2 b e3 // Error here.
        val v = e1 p // Error here (if the line above is commented out).

Since it is common to have the same operator applied and an operator priority
would always be undecidable compared to that of its own peer, there must be
a way to decide it. This is associativity. The priority is on the left with
left associative operators and on the right with right associative operators.
A prefix operator is finally just a unary right associative operator, and the
other way for a postfix operator.

Example:

        infixl b
        infixr c

        extern fn b(int, int): int
        extern fn c(int, int): int

        val (e1, e2, e3) = (1, 2, 3)
        val v = e1 b e2 b e3 // Evaluated as (e1 b e2) b e3
        val v = e1 c e2 c e3 // Evaluated as e1 c (e2 c e3)


The case of two operators with the same priority, one being right associative
and the other left associative, is not decidable.

Example:

        infixr o
        infixl p

        extern fn o(int, int): int
        extern fn p(int, int): int

        val v = 1 o 2 p 3 // Undecidable.
        val v = 1 p 2 o 3 // Undecidable too.

Hint: operators with different associativities, should have different
priorities (whatever their arities) or else they may be two claiming the same
argument, with no way to decide.


FOLDAT_EXP
------------------------------------------------------------------------------

        FOLDAT_EXP = "fold@" … IMPEND

Tags: expression; dynamic; linear; type;

Applies on a variable matching an unfolded dataviewtype constructor. Such a
variable was previously unfolded (opened‑up) with a `"@"` decorating a
constructor in pattern matching. When the variable is unfolded, it can be
updated. When it is folded‑back, it cannot anymore.

Example:

        typedef r = @{i=int}     // A record type.
        dataviewtype t = C of r  // An r wrapped in a linear type.
        var c = C(@{i=1})        // c is initially folded (closed).
        val+ @C(r) = c           // Unfold (open) c to allow update.
        prval pf = view@ r       // If ever this proof is needed.
        val () = r.i := 2        // Update component.
        prval () = fold@ c       // Fold‑back c.
        val () = r.i := 3        // Error, c is folded again.

Folding‑back an instance of a linear type may be required to preserve its
type upon return to an another scope.

Example:

        typedef r = @{i=int}
        dataviewtype t = C of r

        fn test(c: &t >> t): void = let
           val+ @C(r) = c
           val () = r.i := 2
           prval () = fold@ c // Fold‑back before return.
        in end

If the line `prval () = fold@ c` is commented‑out, a type error occurs: the
type of `c` is not preserved.


FOR_EXP
------------------------------------------------------------------------------

        FOR_EXP = "for" … IMPEND

Tags: expression; dynamic; void; unsafe;

Void expression with side effects. If takes three arguments: initialization of
previously declared variable, condition to go on and step. The expressions
next to the arguments is the loop body. Its type must be void.

**Warning: there is not termination metrics, it can loop forever, the
typechecker will not complain!**. See `FORSTAR_EXP` for the same kind of loop
with termination metrics.

Example:

        var i: int
        val () = for (i := 0; i <= 9; i := i + 1) println! i

It can loop forever.

Example:

        // Purposely erroneous, to show it should be used with lot of care.
        var i: int
        val () = for (i := 0; i <= 9; i := i) println! i


FORSTAR_EXP
------------------------------------------------------------------------------

        FORSTAR_EXP = "for*" … "=>" … IMPEND

Tags: expression; dynamic; void;

Same as `FOR_EXP` but with optional termination metrics. The syntax varies a
bit: after the keyword, comes static declarations, the metrics, and a dynamic
declaration matching the loop variable. **If the metrics are omitted, this
construct is not safer than `FOR_EXP`.**

The metrics must be strictly decreasing and greater than or equal to, zero. It
includes the case which makes the loop stops not just the ones where the loop
body is entered.

Example:

        var i: int
        val () = for* {j:int; j <= 10} .<10 - j>. (i: int(j))
           => (i := 0; i <= 9; i := i + 1)
              println! i



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

  * `"implement"`
  * `"primplement"`
  * `"implmnt"` — synonymous with `"implement"`
  * `"primplmnt"` — synonymous with `"primplement"`


LAM_EXP
------------------------------------------------------------------------------

        LAM_EXP = LAM … IMPEND

Tags: expression; closure;

Where `LAM` may be one of:

  * `"fix"`
  * `"fix@"`
  * `"lam"`
  * `"lam@"`
  * `"llam"`
  * `"llam@"`


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

For sequence of void expressions, see also `BEGIN_EXP`.


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

Tags: declaration; static; abstract; type;

Where `REASSUME` may be one of:

  * `"absreimpl"`
  * `"reassume"` — synonymous with `"absreimpl"`

Recall a previously stated implementation of an abstract type declared (the
implementation) with `ASSUME_DECL`. It literally pulls the declaration from
any scope to any other scope.

Example:

        abst@ype file

        local
           (* Scope #1 *)
           absimpl file = int
        in
        end

        local
           (* Scope #2 *)
           absreimpl file
           fn is_stdout(f:file): bool = (f = 1)
        in
        end

The effect of `absimpl` in scope #1 is pulled into scope #2 by `absreimpl`.


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
dynamic declarations, referring to static or dynamic identifiers.

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
  * `"#dynload"` — synonymous with `"dynload"`


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
  * `"#staload"` — synonymous with `"staload"`


SRPUNDEF_DECL
------------------------------------------------------------------------------

        SRPUNDEF_DECL = "#undef" … ";"?

Tags: declaration;


STACST_DECL
------------------------------------------------------------------------------

        STACST_DECL = STACST … "and"* … ";"?

Tags: declaration; static; abstract;

Where `STACST` may be one of:

  * `"stacst"`
  * `"sta"` — synonymous with `"stacst"`

Abstract static expression. Abstract: the value does not matter and there is
none, only the introduced identity (name) and its declared sort, do, and
possibly its properties defined as axioms. The constant is expected to be of a
predicative sort; although doing otherwise will not end in a syntax error from
Postiats, it is not supported. If impredicative abstract constants are needed,
`ABSTYPE_DECL` should be used instead.

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

        STATIC_DECL = "static" … IMPEND

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
  * `"vtypedef"` — synonymous with `"viewtypedef"`

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

