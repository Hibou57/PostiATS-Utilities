Sorts
==============================================================================

Impredicative
------------------------------------------------------------------------------

Impredicative built‑in base sorts, after `pats_staexp2_sort.dats`:

  * `prop`
  * `prop+`
  * `prop-`
  * `type`: boxed types
  * `type+`
  * `type-`
  * `t0ype`: flat types
  * `t0ype+`
  * `t0ype-`
  * `types`: variadic arguments
  * `view`
  * `view+`
  * `view-`
  * `vtype`
  * `vtype+`
  * `vtype-`
  * `vt0ype`
  * `vt0ype+`
  * `vt0ype-`

Where `+` is for covariance and `-` is for contravariance.


Predicative
------------------------------------------------------------------------------

Predicative built‑in base sorts, after `pats_staexp2_sort.dats`:

  * `addr` (also note agz, the subset of not null addr)
  * `bool`
  * `cls`
  * `eff`: function effects
  * `float`
  * `int`
  * `real`
  * `string`
  * `tkind`: algebraic (no quantifiers), like an abstract type

Note “char” used to be but is not anymore.
