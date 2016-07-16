#!/usr/bin/env python3.5

# Arun Debray, 24 Dec. 2015
# Given a group order, classifies finite abelian groups of that order.

# ./finite_abelian_groups.py [-tpi] number
#	-t formats the output in TeX (as opposed to in the terminal)
#	-p chooses the primary components decomposition (default)
#	-i chooses the invariant factors decomposition

import argparse
import collections
import functools
import itertools
import math

# Handles command-line arguments. See usage, above.
def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description='Classifies finite abelian groups of a given order.')
	parser.add_argument('-t', action='store_true', help='formats output in LaTeX')
	parser.add_argument('-p', action='store_true', help='chooses primary components decomposition (default)')
	parser.add_argument('-i', action='store_true', help='chooses invariant factors decomposition')
	parser.add_argument('order', metavar='n', type=int, help='group order')
	return parser.parse_args()

# Determines the prime factors of a number. No, this isn't the best algorithm, but
# it's good enough. Returns them as a Counter object (a dict of prime -> power), in which
# all values will be strictly positive.
def prime_factors(n: int) -> collections.Counter:
	for i in range(2, 1 + math.ceil(math.sqrt(n))):
		# By doing this in order, we guarantee that this only happens when i is prime (2 comes before
		# any other even number, etc.)
		if n % i == 0:
			if n == i:
				return collections.Counter({n: 1})
			else:
				to_return = prime_factors(n // i)
				to_return[i] += 1
				return to_return
	# if n is prime
	return collections.Counter({n: 1})

# A helper function for the partitions function, below. Returns the partitions of n using integers
# less than or equal to m. However, within this program it makes more sense to do this multiplicatively:
# n is represented as p^n, and we are partitioning as p^n = p^{n_1} x p^{n_2} x ... x p^{n_k}.
@functools.lru_cache(maxsize=None) # Wraps the function in a cache, making memoization simpler
def _part_lt(p: int, n: int, m: int) -> list:
	if n == 0:
		return [[]]
	if n == 1:
		return [[p]]
	if m > n:
		return _part_lt(p, n, n)
	# Now, we recurse: the first entry in the partition can be any j in {1, ..., m}, and the rest is a
	# partition in _part_lt(n-j, j).
	to_return = []
	for j in range(1, m+1):
		to_return += [part + [p**j] for part in _part_lt(p, n-j, j)]
	return to_return

# Returns the partitions of n as pth powers, i.e. the ways of writing p^n = p^{a_1} x ... x p^{a_m}
# such that  each a_i is a positive integer and a_i >= a_{i+1} for each i. This is the algorithmic meat
# of each decomposition, though some thought must go into piecing the partitions for different primes
# together. Of course, this function calls the helper function, above.
def partitions(p: int, n: int) -> list:
	return _part_lt(p, n, n)

# Flattens one level of a list, turning [[1, 2, 3], [4, 5]] into [1, 2, 3, 4, 5].
def flatten(xs: list) -> list:
	return [item for sublist in xs for item in sublist]

# Given the prime factors, returns a list of all abelian groups of the given order in primary-
# factors format.
def primary_factor_decomp(factors: collections.Counter) -> list:
	decomps_at_primes = [partitions(p, factors[p]) for p in factors]
	return [flatten(choice) for choice in itertools.product(*decomps_at_primes)]

# Uses the partitions in a different way to make a list of all abelian groups of a given order in
# the invariant-factors decomposition.
def invariant_factor_decomp(factors: collections.Counter) -> list:
	decomps_at_primes = [partitions(p, factors[p]) for p in factors]
	return [(functools.reduce(lambda x,y: x*y, inv_fact)
		for inv_fact in itertools.zip_longest(*choice, fillvalue=1))
		for choice in itertools.product(*decomps_at_primes)]

# Returns "there are n abelian groups" or "there is one abelian group" depending on the value of n.
def format_plurals(n: int) -> str:
	if n == 1:
		return 'There is one abelian group'
	else:
		return 'There are %d abelian groups' % n

# Formats and prints the output.
def output(groups: list, order: int, as_TeX: bool):
	if as_TeX:
		print('\\documentclass{amsart}')
		print('\\newcommand{\\Z}{\\mathbb Z}')
		print('\\title{Abelian Groups of Order %d}' % order)
		print('\\begin{document}')
		print('\\maketitle')
		print('%s of order %d.' % (format_plurals(len(groups)), order))
		print('\\begin{gather*}')
		print('\\\\\n'.join(['\\oplus'.join(['\\Z/%d' % component for component in group]) for group in groups]))
		print('\\end{gather*}')
		print('\\end{document}')
	else:
		print('%s of order %d.' % (format_plurals(len(groups)), order))
		for group in groups:
			print('⊕ '.join('ℤ/%d' % component for component in group))

def main():
	arginfo = parse_args()
	groups = None
	factors = prime_factors(arginfo.order)
	if arginfo.i:
		groups = invariant_factor_decomp(factors)
	else:
		groups = primary_factor_decomp(factors)
	output(groups, arginfo.order, arginfo.t)

if __name__ == '__main__':
	main()
