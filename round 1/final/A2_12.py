
# Dies ist die Menge φ''(2021), welche alle Elemente von 674 bis 1347 enthält.
# range(a, b) ist eine spezielle Datenstruktur, welche alle Elemente von a bis b exklusiv enthält.
# Also müssen wir von 674 bis 1348 gehen, um den gesuchten Bereich auszugeben
# set() konvertiert das ganze noch in eine Menge
phi_dd = set(range(674, 1348))

# set(filter(f, a)) gibt alle Element E aus a als Menge aus, für die f(E) wahr ist
phi_d = set(filter(
    # Dieses konstrukt ist die filter-funktion.
    # % ist der modulo-operator, == überprüft auf gleichheit als Wahrheitswert
    # lambda element: gibt an, dass die Funktion f(E) E in der Variable element speichert.
    # der Rest ist selbsterklärend
    lambda element: (2021 * element) % (3 * element - 2021) == 0,

    # Und dies ist dann einfach die zu filternde Menge
    phi_dd
))

# Dies gibt einfach die Menge phi_d aus
print(phi_d)
