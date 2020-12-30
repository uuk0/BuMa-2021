# Hilfsfunktionen zu Generatoren
import itertools

# Verarbeitung der Daten in mehreren Prozessen (-> theoretisch schneller)
import multiprocessing

# Hilfsbibliothek für Zeitmessung
import time


class Network:
    """
    Klasse, die den Graphen G erstellt und verarbeitet.
    Eigenschaften von G:
    Jeder Knoten [node] ist zunächst mit jedem anderen Verbunden, aber alle bis auf einen jeweils mit zwei
        anderen so nicht, dass die nicht-verbindungen eine geschlossene Kurve ergeben.

    Jeder Knoten hat eine ID, wobei der erste 0 hat (die Spitze der Pyramide), und die anderen dann bei 1 bis n gehen.
    [Hier wird bei 0 begonnen, da dies die Programmiersprache python für Listen so vorsieht]

    Dieses Programm benutzt die Bibliothek "itertools". Deren funktionen sind hier nicht näher beschrieben.
    Siehe https://docs.python.org/3/library/itertools.html für eine genaue Dokumentation.

    Einige Funktionen haben ein ominöses Parameter colors=2.
    Dies erlaubt in der theorie, auch färbungen mit mehr als zwei Farben.
    Python nimmt hier als default-Wert den Wert 2 an, wie in der Aufgabenstellung gefragt
    """

    class Slave:
        """
        Hilfsklasse für "multiprocessing"
        Zurzeit nicht benutzt
        """

        def __init__(self, master: "Network"):
            self.task_pipe = multiprocessing.Queue(maxsize=1000)
            self.result_pipe = multiprocessing.Queue()
            self.master = master
            self.alive = True
            self.running = False

        def run(self):
            while self.alive:
                if self.task_pipe.empty():
                    time.sleep(.2)
                    self.running = not self.task_pipe.empty()
                    continue
                self.running = True
                coloring = self.task_pipe.get()
                self.result_pipe.put(self.check_coloring(coloring))

        def check_coloring(self, coloring: list) -> bool:
            for a, b, c in itertools.permutations(range(len(self.master.connections)), 3):
                ab = (min(a, b), max(a, b))
                bc = (min(b, c), max(b, c))
                ac = (min(a, c), max(a, c))
                if ab not in self.master.connections or bc not in self.master.connections or ac not in self.master.connections:
                    continue

                ab = coloring[self.master.connections.index(ab)]
                bc = coloring[self.master.connections.index(bc)]
                ac = coloring[self.master.connections.index(ac)]
                if ab == bc == ac:
                    return True
            print(coloring)
            return False

    def __init__(self, nodes: int):
        """
        Konstruktor der Klasse.
        Erzeugt noch keinen Graphen
        :param nodes: wie viele Knoten der Graph haben soll - 1 [Also die Anzahl an eckpunkten der Grundfigur]
        """
        self.nodes = nodes + 1
        self.connections = []

    def bake(self):
        """
        Erzeugt den Graphen G
        """

        # Hilfscode, um doppelte Verbindungen zu vermeiden
        self.connections = set(self.connections)

        # Suche alle möglichen paare a, b der Knoten...
        for a, b in itertools.product(range(self.nodes), range(self.nodes)):
            # Sortiere sie nach größtem und kleinsten der beiden...
            con = (min(a, b), max(a, b))
            if a != b:  # Schaue, ob die beiden nicht identisch sind
                self.connections.add(con)

        print(len(self.connections))

        # Und nun entferne alle Verbindungen von Knoten, deren ID sich um 1 unterscheidet, und nicht die Spitze enthalten
        for i in range(1, self.nodes-1):
            self.connections.remove((i, i+1))
        # Und den Knoten mit der ID 1 und den letzten
        self.connections.remove((1, self.nodes-1))

        print(len(self.connections))

        # Hilfscode, um doppelte Verbindungen zu vermeiden
        self.connections = list(self.connections)

    def get_colorings(self, colors=2):
        # Hilfsfunktion, um alle Farbkombinationen zu erhalten
        return itertools.product(range(colors), repeat=len(self.connections))

    def check_colorings(self, colors=2) -> bool:
        """
        Überprüft im Graphen G alle möglichen Färbungen
        """
        m = 2 ** len(self.connections)  # so viele Färbungen gibt es
        for i, coloring in enumerate(self.get_colorings(colors)):  # iteriere über alle
            if i % 1000 == 10:
                # wenn die Anzahl mod 1000 == 10 ist, gebe die aktuelle Stelle aus
                # 10 deshalb, da für kleine Graphen sonst gar nichts ausgegeben würde
                print(i / m, i, m)
            if not self.check_coloring(coloring):
                # falls in diese konfiguration keine drei Knoten existiere, sodass die Verbindungen die gleiche Farbe
                # tragen, so gebe diese Konfiguration aus, und gib False zurück.
                print(coloring, self.connections)
                return False
        return True

    def check_colorings_parallel(self, colors=2, processes=10) -> bool:
        m = 2 ** len(self.connections)
        ran = 0
        pool = multiprocessing.Pool(processes)
        jobs = []
        for coloring in self.get_colorings(colors):
            jobs.append(pool.apply_async(self.check_coloring, (coloring,)))
        counts = 0
        while len(jobs) > 0:
            if ran // 1000 != counts:
                counts = ran // 1000
                print("\r", ran / m, ran, m, end="")

            for job in jobs[:]:
                if job.ready() and job.successful():
                    if not job.get():
                        pool.close()
                        return False
                    jobs.remove(job)
                    ran += 1
        pool.close()
        return True

    def check_coloring_parallel_1(self, colors=2, processes=10):
        m = 2 ** len(self.connections)
        ran = 0
        colorings = self.get_colorings(colors)
        slaves = []
        process_instances = []
        counts = 0
        for _ in range(processes):
            slave = Network.Slave(self)
            slaves.append(slave)
            process_instances.append(multiprocessing.Process(target=slave.run))
        for process in process_instances:
            process.start()
        while True:
            if ran // 1000 != counts:
                counts = ran // 1000
                print("\r", ran / m, ran, m, end="")
            try:
                for slave in slaves:
                    while not slave.task_pipe.full():
                        coloring = next(colorings)
                        slave.task_pipe.put(coloring)

                    while not slave.result_pipe.empty():
                        ran += 1

                        if not slave.result_pipe.get():
                            for s in slaves:
                                s.alive = False
                            return False
            except StopIteration:
                while len(slaves) > 0:
                    for slave in slaves[:]:
                        while not slave.result_pipe.empty():
                            ran += 1

                            if not slave.result_pipe.get():
                                for s in slaves:
                                    s.alive = False
                                return False

                        if not slave.running:
                            slaves.remove(slave)
                            slave.alive = False
                return True

    def check_coloring(self, coloring: tuple) -> bool:
        """
        Überprüft eine gewisse Färbung
        :param coloring: die Färbung
        """
        # iteriere über alle möglichen triple dreier Punkte
        for a, b, c in itertools.permutations(range(len(self.connections)), 3):
            # o.b.d.a. können wir alle Tripel, wo nicht a < b < c gilt, weglassen
            if not (a < b < c): continue

            # Alle 3 Kanten
            ab = (min(a, b), max(a, b))
            bc = (min(b, c), max(b, c))
            ac = (min(a, c), max(a, c))

            # Existieren diese Kanten?
            if ab not in self.connections or bc not in self.connections or ac not in self.connections:
                continue

            # Suche die Farben dafür ...
            ab = coloring[self.connections.index(ab)]
            bc = coloring[self.connections.index(bc)]
            ac = coloring[self.connections.index(ac)]
            if ab == bc == ac:  # ... und überprüfe, ob sie gleich sind
                return True
        return False


if __name__ == "__main__":
    network = Network(int(input("nodes: ")))
    network.bake()

    print(network.check_colorings(), network.connections)

"""
Environment:
    PyPy version 3.8, downloaded from https://www.pypy.org/
    PyCharm 2020.3.1 (Community Edition)
    Build #PC-203.6682.86, built on December 18, 2020
    Runtime version: 11.0.9.1+11-b1145.37 amd64
    VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
    Windows 10 10.0
    GC: ParNew, ConcurrentMarkSweep
    Memory: 725M
    Cores: 8

8 fails with e.g.:
(0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1) 
connections:
    [(3, 7), (4, 6), (5, 7), (0, 2), (0, 5), (1, 6), (0, 8), (2, 5), (1, 3), (2, 8), (6, 8), (4, 8), (3, 6), (0, 1), (0, 7), (2, 4), (0, 4), (2, 7), (1, 5), (4, 7), (3, 5), (3, 8), (5, 8), (0, 3), (1, 4), (0, 6), (1, 7), (2, 6)]
9 run without pre-exit
"""


