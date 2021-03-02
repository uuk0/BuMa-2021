# Verwende die Bibliothek "math", welche einige nützliche mathematische Funktionen bereitstellt
import math
import typing
import itertools

file = open("entries.txt", mode="a")


# Dies ist nun eine Funktion, welche eine Ganzzahl n nimmt, und dabei eine weitere Ganzzahl und eine Menge ausgibt
def phi(n: int) -> typing.Tuple[int, set]:
    # Erzeugung von φ''(n) als range() objekt (ist effizienter als set, kann hier aber das selbe) aller ganzer Zahlen zwischen...
    phi_dd = range(
        # ... aufgerundet auf eine ganze Zahl n/3 und ...
        math.ceil(
            n / 3
        ),
        # ... abgerundet auf eine ganze Zahl 2 * n / 3 + 1 exklusiv [also ohne +1 inklusiv]
        math.floor(
            2 * n / 3
        ) + 1
    )

    # Filterung der Menge φ''(n) zur Menge φ'(n)
    phi_d = set(filter(
        lambda element: (n * element) % (3 * element - n) == 0,
        phi_dd
    ))

    # φ(n) als größe dieser Menge
    return len(phi_d), phi_d


# Und nun, iteriere über alle n ab 1...
# (itertools.count(a, s) iteriert unendlich lang ab a in Schritten von s)

m = 0
for i in itertools.count(1, 1):
    # Falls i durch drei teilbar ist, überspringe diese Zahl
    if i % 3 == 0: continue

    c, phi_d = phi(i)


    m = max(m, c)

    if i % 1000 == 0:
        print(i, c, m)
        m = 0

    if c < 1000:
        continue

    if c != 2021:
        file.write(str(i)+" "+str(c)+"\n")
        continue

    print(i, "erfüllt die Eigenschaft, mit folgenden Paaren:")

    for x in sorted(phi_d):
        # rechne y aus
        y = int((i * x) / (3 * x - i))

        # und gebe dieses Paar aus
        print("x=" + str(x) + ", y=" + str(y))

    break
