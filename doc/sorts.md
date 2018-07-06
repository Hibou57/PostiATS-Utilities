Postiats sorts
==============================================================================

Impredicative sorts
------------------------------------------------------------------------------

Impredicative built‑in base sorts, after `pats_staexp2_sort.dats`:

  * `prop`: theorem proving, internalizing constraint‑solving.
  * `type`: boxed types, of unknown size.
  * `t@ype`: flat types, with a known size.
  * `types`: variadic arguments.
  * `view`: linear `prop` (possibly linear).
  * `viewtype`: linear `type` (possibly linear).
  * `viewt@ype`: linear `t@ype` (possibly linear).


With these variations:

  * “${sort}+“ (ex. `t@ype+`) for covariance.
  * “${sort}-“ (ex. `t@ype-`) for contravariance.


With these relations:

  * `t@ype` < `type`.
  * `viewtype` < `type`.
  * `viewt@ype` < `t@ype`.
  * `view@type` < `viewtype`.
  * `prop` < `t@ype`.
  * `view` < `view@type`.
  * `view` < `prop`.


With these aliases:

  * `t@ype`: `t0ype`.
  * `viewtype`: `vtype`.
  * `viewt@ype`: `viewt0ype`, `vt@ype` and `vt0ype`.


Ex: the `int` type is of the `t@ype` sort and the `string` type is of the
`type` sort.


Predicative sorts
------------------------------------------------------------------------------

Predicative built‑in base sorts, after `pats_staexp2_sort.dats`:

  * `addr` (also note `agz`, its derived not null subset).
  * `bool`: `false_bool` and `true_bool`.
  * `cls`: hierarchical ordering of nominal types (ex. specifying OO APIs).
  * `eff`: function effects.
  * `float`: without equality or comparison operators.
  * `int`: without negative literals, however with a negate operator.
  * `real`: experimental, for verification involving real numbers.
  * `string`: without equality or comparison operators.
  * `tkind`: algebraic (no quantifiers), like an abstract type, template args.

Note “char” used to be but is not anymore.


Semantic
------------------------------------------------------------------------------

Sorts classify types like types classify values. Alternatively, a sort
is to a type what a meta‑class is to a class.

Ex.

        stacst t: t@ype
        typedef u = t


Impredicative sorts are the sorts of types. In particular, `prop` is the
sort of proof types.

A predicative sort cannot be the sort of a type. The predicative sorts don’t
generate the types of the same name, they are built‑in types of `type` or
`t@ype` sorts.

If the argument of a type constructor is of …

  * a predicative sort, it defines an indexed type.
  * an impredicative sort, it defines a polymorphic type.

Ex. #1:

        stadef kilo: int -> t@ype = lam n => int(n * 1000)
        val v:kilo(3) = 3000

Ex. #2:

        stadef paire: t@ype -> t@ype = lam t => @(t, t)
        val v:paire(int) = (1, 2)

