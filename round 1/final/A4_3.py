import itertools
import multiprocessing
import typing


# Das konzept von Klassen...
# Eine Struktur, welche Funktionen und Attribute enthält
# Dabei bezeichnet "self" immer das aktuelle Objekt (eine Instanz der Klasse)
class Network:

    # Diese Funktion wird bei der Erzeugung einer Instanz ausgeführt, und definiert "nodes" und "connections"
    def __init__(self, nodes: int):

        self.nodes: int = nodes + 1  # +1 für die Spitze [die Spitze ist die "0", die anderen gehen ab 1]
        self.connections: typing.List[typing.Tuple[int, int]] = []

    def bake(self):
        # Diese Funktion erstellt die connections-liste, indem sie zunächst ein set() erstellt
        # (eine Datenstruktur, welche keine doppelten Elemente erlaubt)
        self.connections = set(self.connections)

        # Gefolgt von itertools.product(), eine funktion die alle Kombinationen zweier
        for a, b in itertools.product(range(self.nodes), range(self.nodes)):

            # Sortiere sie nach größtem und kleinstem
            con = (min(a, b), max(a, b))

            # Und füge sie den Kanten hinzu, wenn sie zwei verschiedene Endpunkte hat
            if a != b:
                self.connections.add(con)

        print("So viele Kanten vor der Entfernung:", len(self.connections))

        # Diese Kanten löschen wir, da sie die Nachbarverbindungen in der Grundebene sind
        for i in range(1, self.nodes-1):
            self.connections.remove((i, i+1))
        self.connections.remove((1, self.nodes-1))

        print("So viele Kanten nach der Entfernung:", len(self.connections))

        # Und konvertiere die kanten zurück in eine liste
        self.connections = list(self.connections)

    def get_colorings(self, colors=2):
        # Diese Funktion gibt die Färbungen zurück. colors ist die Anzahl an Farben, welche im Normalfall 2 ist.
        # itertools.product haben wir schon gesehen,
        # repeat=x ersetzt nun das Hinschreiben von x mal range(colors) durch einmal.
        return itertools.product(range(colors), repeat=len(self.connections))

    def check_colorings(self, colors=2) -> bool:
        # Diese Funktion überprüft nun alle Färbungen auf die gesuchte Eigenschaft

        # so viele Färbungen
        m = 2 ** len(self.connections)

        # Iteriere über alle
        for i, coloring in enumerate(self.get_colorings(colors)):

            # Falls wir bei einer Zahl, die 10 mehr als ein Vielfaches von 100000 ist, gebe dein Fortschritt an
            if i % 100000 == 10:
                # print("\r", i / m, i, m, end="")
                print(i / m, i, m)

            # Überprüfe die Färbung
            if not self.check_coloring(coloring):
                # Und falls diese keine drei Knoten mit gleichfarbigen Kanten hat, gebe die Färbung und die Kanten aus
                print(coloring, self.connections)
                return False

        # Ansonsten tue nichts
        return True

    def check_coloring(self, coloring: tuple) -> bool:
        # Diese Funktion überprüft nun eine Färbung
        # coloring ist eine Liste von 1 und 0, welche die Färbungen angibt

        # Iteriere über je drei Punkte
        # itertools.permutations sorgt für keine dopplungen von Knoten
        for a, b, c in itertools.permutations(range(len(self.connections)), 3):
            # O.b.d.A. dürfen wir das annehmen und diese Fälle überspringen
            if not (a < b < c): continue

            # Suche die Kanten, sie sind immer (kleinere Knoten ID, größere Knoten ID)
            ab = (min(a, b), max(a, b))
            bc = (min(b, c), max(b, c))
            ac = (min(a, c), max(a, c))

            # Und falls nun eine dieser drei Kanten gelöscht wurde, können wir auch einfach diese Runde überspringen
            if ab not in self.connections or bc not in self.connections or ac not in self.connections:
                continue

            # Suche nun die Färbungen
            ab = coloring[self.connections.index(ab)]
            bc = coloring[self.connections.index(bc)]
            ac = coloring[self.connections.index(ac)]

            # Und falls diese Identisch sind, gebe das aus
            if ab == bc == ac:
                return True

        # Sonst gibt es in diesem Programm keine
        return False


# Dieser Block wird bei der Ausführung des Programmes ausgeführt
if __name__ == "__main__":
    # erstelle den Graphen
    network = Network(int(input("nodes: ")))
    # Erstelle die Kanten
    network.bake()

    # und gebe das Ergebnis der Überprüfung aus
    print(network.check_colorings(), network.connections)

