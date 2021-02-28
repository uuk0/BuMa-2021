# Verwende die Bibliothek "math", welche einige nützliche mathematische Funktionen bereitstellt
import math

# input(t) gibt t in die konsole aus und gibt die darauffolgende Benutzereingabe als String ("Zeichenkette") zurück.
# int(x) konvertiert ein beliebiges Datenobjekt in eine ganzzahl, in diesem Falle ein String
n = int(input("n: "))

# Erzeugung von φ''(n) als Menge aller ganzer Zahlen zwischen...
phi_dd = set(range(
    # ... aufgerundet auf eine ganze Zahl n/3 und ...
    math.ceil(
        n / 3
    ),
    # ... abgerundet auf eine ganze Zahl 2 * n / 3 + 1 exklusiv [also ohne +1 inklusiv]
    math.floor(
        2 * n / 3
    ) + 1
))

# Filterung der Menge φ''(n) zur Menge φ'(n)
phi_d = set(filter(
    lambda element: (n * element) % (3 * element - n) == 0,
    phi_dd
))

# φ(n) als größe dieser Menge
phi = len(phi_d)

# Überprüfe auf gesuchte Größe, ...
if phi == 2021:
    # ... gebe aus, dass es geklappt hat...
    print(str(n)+" lässt sich auf 2021 Weisen als Stammbruch darstellen, nämlich:")

    # ... und iteriere jetzt nach x aufsteigend über alle x und tue für jedes Element:
    for x in sorted(phi_d):
        # rechne y aus
        y = (n * x) / (3 * x - n)

        # und gebe dieses Paar aus
        print(x, y)

else:
    # und gebe hier noch aus, auf wie viele Weisen den sich n den darstellen lässt
    print(str(n)+" lässt sich leider auf "+str(phi)+" mögliche Weisen als Summe zweier Stammbrüche darstellen")

