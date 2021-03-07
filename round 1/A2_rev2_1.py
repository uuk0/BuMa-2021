import primefac
import itertools

n = int(input("n: "))
factors = list(primefac.primefac(n))


def divisors(f: list):
    l = len(f)
    yielded = set()
    for i in range(2**l):
        v = 1
        for x, c in enumerate(f):
            if i >> x & 1:
                v *= c
        if v in yielded: continue
        yield int(v)
        yielded.add(v)


print(list(divisors(factors)))

