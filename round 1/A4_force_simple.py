import itertools


class Network:
    def __init__(self, nodes: int):
        self.nodes = nodes + 1
        self.connections = []

    def bake(self):
        self.connections = set(self.connections)

        for a, b in itertools.product(range(self.nodes), range(self.nodes)):
            con = (min(a, b), max(a, b))
            if a != b:
                self.connections.add(con)

        print(len(self.connections))

        for i in range(1, self.nodes - 1):
            self.connections.remove((i, i + 1))
        self.connections.remove((1, self.nodes - 1))

        print(len(self.connections))

        self.connections = list(self.connections)

    def get_colorings(self, colors=2):
        return itertools.product(range(colors), repeat=len(self.connections))

    def check_colorings(self, colors=2) -> bool:
        m = colors ** len(self.connections)
        for i, coloring in enumerate(self.get_colorings(colors)):
            if i % 1000 == 10:
                # print("\r", i / m, i, m, end="")
                print(i / m, i, m)
            if not self.check_coloring(coloring):
                print(coloring, self.connections)
                return False
        return True

    def check_coloring(self, coloring: tuple) -> bool:
        for a, b, c in itertools.permutations(range(len(self.connections)), 3):
            if not (a < b < c): continue

            ab = (min(a, b), max(a, b))
            bc = (min(b, c), max(b, c))
            ac = (min(a, c), max(a, c))
            if ab not in self.connections or bc not in self.connections or \
                    ac not in self.connections:
                continue

            ab = coloring[self.connections.index(ab)]
            bc = coloring[self.connections.index(bc)]
            ac = coloring[self.connections.index(ac)]
            if ab == bc == ac:
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
