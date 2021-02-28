import itertools
import multiprocessing
import time


class Network:
    """
    Class representing a network of n nodes linked in the following way:
    - every node is connected to each other
    - all but one nodes create a circle-like "shape" with n-1 connections. These connections are removed
        from the map

    The class is capable of calculating the permutation map of coloring this connection of the network
        in any amount of colors.
    The network can check if in a given permutation of the network has any three nodes connected by the same
        color.
    The network is further capable of connecting this in the following way:
        Is there always such a group of three points?
    """

    class Slave:
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
        self.nodes = nodes + 1
        self.connections = []

    def bake(self):
        self.connections = set(self.connections)

        for a, b in itertools.product(range(self.nodes), range(self.nodes)):
            con = (min(a, b), max(a, b))
            if a != b:
                self.connections.add(con)

        print(len(self.connections))

        for i in range(1, self.nodes-1):
            self.connections.remove((i, i+1))
        self.connections.remove((1, self.nodes-1))

        print(len(self.connections))

        self.connections = list(self.connections)

    def get_colorings(self, colors=2):
        return itertools.product(range(colors), repeat=len(self.connections))

    def check_colorings(self, colors=2) -> bool:
        m = 2 ** len(self.connections)
        for i, coloring in enumerate(self.get_colorings(colors)):
            if i % 100000 == 10:
                # print("\r", i / m, i, m, end="")
                print(i / m, i, m)
            if not self.check_coloring(coloring):
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
            if ran // 100000 != counts:
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
            if ran // 100000 != counts:
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
        for a, b, c in itertools.permutations(range(len(self.connections)), 3):
            if not (a < b < c): continue

            ab = (min(a, b), max(a, b))
            bc = (min(b, c), max(b, c))
            ac = (min(a, c), max(a, c))
            if ab not in self.connections or bc not in self.connections or ac not in self.connections:
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


