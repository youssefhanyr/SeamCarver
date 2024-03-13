from PIL import Image
from stuff.Graph import DiGraph
from math import sqrt
from stuff.AcyclicSP import AcyclicSPMOD
from numpy import array


class SeamCarver:

    def __init__(self, picture):
        self.picture = Image.open(picture)
        self.width, self.height = self.picture.width, self.picture.height
        self.graphH, self.graphV = None, None
        self._construct()

    def _construct(self):
        pixels = self.__construct_list()
        self.graphH, self.graphV = DiGraph(pixels), DiGraph(pixels)
        for vertex in range(self.graphV.v):
            w = vertex % self.width
            if vertex + self.width >= self.width*self.height:
                continue
            elif w == 0:
                self.graphV.add_edge(vertex, vertex + self.width)
                self.graphV.add_edge(vertex, vertex + self.width + 1)
            elif w == self.width - 1:
                self.graphV.add_edge(vertex, vertex + self.width - 1)
                self.graphV.add_edge(vertex, vertex + self.width)
            else:
                self.graphV.add_edge(vertex, vertex + self.width - 1)
                self.graphV.add_edge(vertex, vertex + self.width)
                self.graphV.add_edge(vertex, vertex + self.width + 1)

        for vertex in range(self.graphH.v):
            if vertex % self.width == self.width - 1:
                continue
            elif vertex - self.width < 0:
                self.graphH.add_edge(vertex, vertex + 1)
                self.graphH.add_edge(vertex, vertex + self.width + 1)
            elif vertex + self.width >= self.width*self.height:
                self.graphH.add_edge(vertex, vertex - self.width + 1)
                self.graphH.add_edge(vertex, vertex + 1)
            else:
                self.graphH.add_edge(vertex, vertex - self.width + 1)
                self.graphH.add_edge(vertex, vertex + 1)
                self.graphH.add_edge(vertex, vertex + self.width + 1)

    def __construct_list(self):
        self._rgb = []
        stuff = list(self.picture.getdata())
        for y in range(0, self.width * self.height, self.width):
            z = stuff[y:y + self.width]
            self._rgb.append(z)
        return len(stuff)

    def energy(self, x, y):
        if x >= self.width or y >= self.height:
            raise IndexError(f"Coord nots right")
        if x == self.width - 1 or x == 0 or y == 0 or y == self.height - 1:
            return 1000.0
        rx, bx, gx = (self._rgb[y][x + 1][i] - self._rgb[y][x - 1][i] for i in range(3))
        ry, by, gy = (self._rgb[y + 1][x][i] - self._rgb[y - 1][x][i] for i in range(3))
        sq_dx = (rx**2) + (bx**2) + (gx**2)
        sq_dy = (ry**2) + (by**2) + (gy**2)
        return sqrt(sq_dx + sq_dy)

    def findverticalseam(self):
        min_energy, min_path = 999999999999999999.9, None
        for s in range(self.width):
            for d in range((self.width*(self.height - 1)), self.width*self.height):
                total_energy = 0.0
                finder = AcyclicSPMOD(self.graphV, s, self)
                path = finder.shortest_path_to(d)
                for v in path:
                    x, y = v % self.width, v // self.width
                    total_energy += self.energy(x, y)
                if total_energy <= min_energy and len(path) > 1:
                    min_energy = total_energy
                    min_path = path
        print(min_energy)
        return min_path

    def findhorizontalseam(self):
        min_energy, min_path = 999999999999999999.9, None
        for s in range(0, self.width*(self.height - 1), self.width):
            for d in range(self.width - 1, self.width*self.height, self.width):
                total_energy = 0.0
                finder = AcyclicSPMOD(self.graphH, s, self)
                path = finder.shortest_path_to(d)
                for v in path:
                    x, y = v % self.width, v // self.width
                    total_energy += self.energy(x, y)
                if total_energy <= min_energy and len(path) > 1:
                    min_energy = total_energy
                    min_path = path
        print(min_energy)
        return min_path

    def removeverticalseam(self, path):
        if path is None:
            raise ValueError("Must have a legitimate path!")
        for pixel in path:
            x, y = pixel % self.width, pixel // self.width
            self._rgb[y].pop(x)
        rgb = array(self._rgb)
        temp = Image.fromarray(rgb, "RGB")
        return temp

    def removehorizontalseam(self, path):
        if path is None:
            raise ValueError("Must have a legitimate path!")
        storage = []
        for pixel in path:
            x, y = pixel % self.width, pixel // self.width
            self._rgb[y].pop(x)
            storage.append((x, y))
        min_y = max(storage, key=lambda z: z[1])[1]
        count = 0
        for pixel in range(self.width):
            if storage[-1 - pixel][1] == min_y:
                count += 1
                continue
            y_current = min_y
            hold = None
            while True:
                y_current -= 1
                if storage[-1 - pixel][1] != y_current:
                    hold = self._rgb[y_current][pixel]
                    self._rgb[y_current][pixel] = self._rgb[min_y][pixel - count]
                else:
                    if hold is None:
                        self._rgb[y_current].insert(pixel, self._rgb[min_y][pixel - count])
                    else:
                        self._rgb[y_current].insert(pixel, hold)
                    break
        self._rgb.pop(min_y)
        rgb = array(self._rgb)
        temp = Image.fromarray(rgb, "RGB")
        return temp



''' First, you need to obtain the min path, to do that you have to
    go (assuming we are looking for v seam) point by point in width checking
    every path from each point in the bottom row with every one in the upper, w*h
    attempts will occur and only one will be minimum, as for the horizontal one
    i have chosen to keep a horizontal version of the graph what i described
    will be the same procedure
    
    deletion will start bottom-up, first find the last point that will be deleted
    and make sure to remove it from every upper point that has previously mentioned
    point in its adj_to same will happen with the other ones in the upper rows until
    the highest is reached then no deletion will be needed other than the deletion of the point
    itself.

 '''