Postiats sorts
==============================================================================

Impredicative sorts
------------------------------------------------------------------------------

Impredicative built‑in base sorts, after `pats_staexp2_sort.dats`:

  * `prop`: theorem proving, internalizing constraint‑solving.
  * `type`: boxed types.
  * `t@ype`: flat types.
  * `types`: variadic arguments.
  * `view`: linear `prop` (possibly linear).
  * `viewtype`: linear `type` (possibly linear).
  * `viewt@ype`: linear `t@ype` (possibly linear).


With these variations:

  * “${sort}+“ (ex. `t@ype+`) for covariance.
  * “${sort}-“ (ex. `t@ype-`) for contravariance.


With these relations:

  * `prop` < `t@ype` < `type`.
  * `view` < `view@type` < `viewtype`.
  * `view` < `prop`.
  * `viewt@ype` < `t@ype`.
  * `viewtype` < `type`.


With these aliases:

  * `t@ype`: `t0ype`.
  * `viewtype`: `vtype`.
  * `viewt@ype`: `viewt0ype`, `vt@ype` and `vt0ype`.


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

If the argument of a type constructor is of …

  * an impredicative sort, it defines an indexed type.
  * a predicative sort, it defines a polymorphic type.
