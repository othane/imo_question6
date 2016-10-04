#!/usr/bin/python

from pylab import *
import json


N = 500

def psieve(M):
    """
    find primes between 1 and M
    """
    # init
    sieve = []
    def update_sieve(p):
        sieve.append(p*range(int(M*1.0/p)))
    primes = [2,]
    update_sieve(2)

    # hunt
    for m in range(3,M):
        # if we have found this already don't worry
        if m in sieve:
            continue
        
        # if m / all known primes this number has a known
        # prime factor so give up ... ideally we would add
        # these to our sive
        if any([m % p == 0 for p in primes]):
            continue

        # ok so m is not a known prime and it has no known
        # prime factors so its a new prime !!! yaya
        primes.append(m)
        update_sieve(m)
    return primes


# load our cached primes list or build it again if missing
try:
    with open("primes.json", "r") as f:
        primes = json.load(f)
except IOError:
    print "Building initial prime list ... "
    primes = psieve(N)
    print "Done"
    with open("primes.json", "w") as f:
        json.dump(primes,f)


def _pfactors(x):
    """
    return prime factors of x
    """
    return set([p for p in primes if x % p == 0])


pfactor_lut = None
def pfactors(x):
    """
    return prime pfactors of x and their powers
    """
    if pfactor_lut is None:
        ret = {}
        for p in primes:
            if x % p == 0:
                # p is a prime factor, what is its power ie p**n?
                for n in range(1, x+1):
                    if x % p**n != 0:
                        break
                ret[p] = n - 1
        print "prime factors of {} are {}".format(x, ret)
        return ret
    else:
        return pfactor_lut[str(x)]


# load our cached prime factor table or build it again if missing
try:
    with open("prime_factors.json", "r") as f:
        pfactor_lut = json.load(f)
except IOError:
    print "Building initial prime factor table ... "
    pfactor_lut = {str(x): pfactors(x) for x in range(1,N**2)}
    print "Done"
    with open("prime_factors.json", "w") as f:
        json.dump(pfactor_lut, f)


# todo, make this faster by pre-compute the prime factors of 1..N as a dict
# and even write to disk and load


def min_common_factors(a, b):
    afactors = pfactors(a)
    bfactors = pfactors(b)
    # one liner
    # [pf**(min(n, bfactors[pf])) for pf, n in afactors.items if pf in bfactors]
    ret = []

    for pf, n in afactors.items():
        try:
            m = bfactors[pf]
            ret.append(int(pf)**min(n,m))
        except KeyError:
            pass
    return ret


if __name__ == "__main__":
    for a in range(1,N):
        for b in range(1,N):
            found = ''
            # we need the powers of the primes for this to work !!
            c2 = prod(min_common_factors(a**2, b**2))
            num = a**2 + b**2
            den = a*b + 1

            if num / c2 == den:
                found = '*' 

            if num % den == 0:
                print "{}s(a={}, b={}) = {} , c2 = {}".format(
                    found, a, b, (a**2 + b**2) / (a*b + 1), c2)

    print "done {} iterations".format(N)
