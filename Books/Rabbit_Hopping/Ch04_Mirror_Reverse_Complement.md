# Rabbit Hopping — Chapter 4
# Mirror, Reverse, and Complement Are Different

Three operations can produce patterns that look related, but they carry different information.

**Mirror** changes coordinate sign:

[
(n,r)mapsto(-n,-r).
]

**Reverse** changes traversal order:

[
(b_0,ldots,b_{N-1})mapsto(b_{N-1},ldots,b_0).
]

**Complement** changes token identity:

[
bmapsto1-b.
]

None implies the others.

This matters because Rabbit Hopping is meant to be reversible. A route can be mirrored without being read backward. It can be read backward without swapping lower and upper branch tokens. It can complement its branch token without crossing the zero mirror.

The receipt must keep those operations in separate fields.
