As a consequence of the [fundamental theorem of finitely generated abelian groups](https://en.wikipedia.org/wiki/Finitely_generated_abelian_group), if *G* is a finite abelian group, it can be written as a direct product (or, equivalently, a direct
sum) of finite cyclic groups, which are all isomorphic to the integers mod *n* for some *n*. Moreover, one can choose
the *n* appearing in this decomposition to be particularly nice: either a list of powers of primes or a list of *invariant
factors*, where the first one divides the second one, which divides the third one, and so on. The two are related by way
of the [Chinese remainder theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem).

This is simple enough that one can turn the problem around: what is the list of all finite abelian groups of a given order?
The answer is given by listing the prime factors of the order and putting them together either using prime powers or
invariant factors. This is relatively algorithmic, so I decided to automate it, partly to get more experience with these
algorithms and partly to play with some interesting programming problems. Though it's currently done in Python, I'd like
to try in Haskell and Rust, to play with those two languages a little more.

In addition to the sources for these programs, I have provided some sample outputs in the `examples` directory.
