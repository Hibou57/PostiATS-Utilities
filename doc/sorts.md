Sorts
==============================================================================

Impredicative
------------------------------------------------------------------------------

Impredicative built‑in base sorts, after `pats_staexp2_sort.dats`:

  * `prop`: theorem proving, internalizing constraint‑solving.
  * `prop+`
  * `prop-`
  * `type`: boxed types.
  * `type+`
  * `type-`
  * `t0ype`: flat types.
  * `t0ype+`
  * `t0ype-`
  * `types`: variadic arguments.
  * `view`: linear `prop` (possibly linear).
  * `view+`
  * `view-`
  * `vtype`: linear `type` (possibly linear).
  * `vtype+`
  * `vtype-`
  * `vt0ype`: linear `t@ype` (possibly linear).
  * `vt0ype+`
  * `vt0ype-`

Where `+` is for covariance and `-` is for contravariance.


Predicative
------------------------------------------------------------------------------

Predicative built‑in base sorts, after `pats_staexp2_sort.dats`:

  * `addr` (also note `agz`, its not null subset, derived).
  * `bool`: `false_bool` and `true_bool`.
  * `cls`: hierarchical ordering of nominal types (specifying OO APIs).
  * `eff`: function effects.
  * `float`
  * `int`: without negative literals, however with a negate operator.
  * `real`
  * `string`
  * `tkind`: algebraic (no quantifiers), like an abstract type, template args.

Note “char” used to be but is not anymore.
