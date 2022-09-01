from math import inf, sqrt
from nodeClass import nodeClass
from heap import heap
import timeit

class a_star:

    def __init__(self, grid_file=None):
        self.start_time = timeit.default_timer()

        self.grid_file = grid_file
        self.blocked, self.start, self.end, self.dim = self.gridInit(grid_file)
        self.blocked_path = self.blocked_paths()
        self.algorithm()
        self.runtime
        

    def gridInit(self, file):
        with open(file) as f:
            lines = f.readlines()
        
        goals = []
        layout = []

        for line in lines:
            arr = [int(string) for string in line.split()]
            if len(arr) == 2:
                goals.append(arr)
            elif len(arr) == 3 and arr[2] == 1:
                layout.append(arr[0:2])
        return layout, goals[0], goals[1], goals[2]

    def algorithm(self):
        self.answer = []
        start_node = nodeClass(None, self.start)
        start_node.g = 0
        start_node.h = self.heuristic(start_node.coordinates)
        start_node.f = start_node.g + start_node.h
        heapp = heap()
        heapp.insert(start_node)
        self.visited = []
        while heapp.size != 0:
            inspect_node = heapp.pop()
            self.visited.append(inspect_node)
            if inspect_node.coordinates == self.end:
                self.answer, self.answer_obj = self.backtrack(inspect_node)
                self.stop_time = timeit.default_timer()
                self.runtime = self.stop_time-self.start_time
                return
            for node in self.successor(inspect_node.coordinates):
                if node not in self.visited:
                    if not heapp.search(node):
                        node.g = inf
                    inspect_distance = inspect_node.g + self.distance(inspect_node.coordinates, node.coordinates)
                    if inspect_distance < node.g:
                        node.g = inspect_distance
                        node.root = inspect_node
                        node.f = node.g + node.h 
                        if heapp.search(node):
                            heapp.rebuild(node)
                        else: 
                            heapp.insert(node)
        

    def successor(self, coordinate):
        node_list = []
        x_max, x_min, y_max, y_min = self.dim[0]+1, 0, self.dim[1]+1, 0

        for x in range(coordinate[0]-1,coordinate[0]+2):
            for y in range(coordinate[1]-1,coordinate[1]+2):
                if (x != coordinate[0] or y != coordinate[1]) and (x <= x_max and x > x_min and y <= y_max and y > y_min) and self.reachable(coordinate, [x, y]):
                    temp_node = nodeClass(None, [x,y])
                    temp_node.h = self.heuristic(temp_node.coordinates)
                    node_list.append(temp_node)

        return node_list

    def reachable(self, coordinate, dest):
        for path in self.blocked_path:
            if coordinate in path and dest in path:
                return False
        return True
            

    def backtrack(self, node):
        path1 = [node.coordinates]
        path2 = [node]
        while node.root:
            temp = node.root
            path1.append(temp.coordinates)
            path2.append(temp)
            node = node.root
        path1.reverse()
        path2.reverse()
        return path1, path2


    def distance(self, point1, point2):
        return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


    def heuristic(self, node):
        return sqrt(2)*min(abs(node[0]-self.end[0]), abs(node[1]-self.end[1]))+max(abs(node[0]-self.end[0]), abs(node[1]-self.end[1]))-min(abs(node[0]-self.end[0]), abs(node[1]-self.end[1]))
        
        
    def blocked_paths(self):
        bl_path = []
        for cell in self.blocked:
            bl_path.append([cell, [cell[0]+1, cell[1]+1]])
            bl_path.append([[cell[0], cell[1]+1], [cell[0]+1, cell[1]]])
            #check if cell is the left most cell or if the left cell is blocked
            if (cell[0]==1 or ([cell[0]-1,cell[1]] in self.blocked)):
                if ([cell,[cell[0],cell[1]+1]] not in bl_path):
                    bl_path.append([cell,[cell[0],cell[1]+1]])
            #UP
            if (cell[1]==1 or ([cell[0],cell[1]-1] in self.blocked)):
                if ([cell,[cell[0]+1,cell[1]]] not in bl_path):
                    bl_path.append([cell,[cell[0]+1,cell[1]]])
            #RIGHT
            if (cell[0]==self.dim[0] or ([cell[0]+1,cell[1]] in self.blocked)):
                if ([[cell[0]+1,cell[1]],[cell[0]+1,cell[1]+1]] not in bl_path):
                    bl_path.append([[cell[0]+1,cell[1]],[cell[0]+1,cell[1]+1]])
            #DOWN
            if (cell[1]==self.dim[1] or ([cell[0],cell[1]+1] in self.blocked)):
                if ([[cell[0],cell[1]+1],[cell[0]+1,cell[1]+1]] not in bl_path):
                    bl_path.append([[cell[0],cell[1]+1],[cell[0]+1,cell[1]+1]])
        return bl_path
    

