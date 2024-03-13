from stuff.sorts import topological_sort


class AcyclicSP:

    def __init__(self, graph, s):
        self.graph = graph
        self.distTo, self.edgeTo = [99999999999.9 for _ in range(self.graph.v)], [None for _ in range(self.graph.v)]
        self.distTo[s] = 0.0
        self._construct()

    def _construct(self):
        order = topological_sort(self.graph, True)
        for v in order:
            for e in self.graph.adj_to(v):
                self._relax(e)

    def _relax(self, e):
        v, w = e.start(), e.end()
        hold = self.distTo[v] + e.weight
        if self.distTo[w] >= hold:
            self.distTo[w] = hold
            self.edgeTo[w] = e

    def shortest_path_to(self, destination):
        pather = []
        while self.edgeTo[destination]:
            hold = self.edgeTo[destination]
            pather.append(hold)
            destination = hold.start()
        return pather
        
        
class AcyclicSPMOD:

    def __init__(self, graph, s, sc):
        self.s = s
        self.sc = sc
        self.graph = graph
        self.distTo, self.edgeTo = [99999999999.9 for _ in range(self.graph.v)], [None for _ in range(self.graph.v)]
        self.distTo[s] = 0.0
        self._construct()

    def _construct(self):
        order = topological_sort(self.graph)
        for v in order:
            for e in self.graph.adj_to(v):
                self._relax(e, v)

    def _relax(self, e, v):
        x, y = e % self.sc.width, e // self.sc.width
        hold = self.distTo[v] + self.sc.energy(x, y)
        if self.distTo[e] >= hold:
            self.distTo[e] = hold
            self.edgeTo[e] = v

    def shortest_path_to(self, destination):
        pather = [destination]
        while self.edgeTo[destination] is not None:
            hold = self.edgeTo[destination]
            pather.append(hold)
            destination = hold
        return pather

