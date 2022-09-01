
from zmq import EADDRINUSE
from nodeClass import nodeClass
from heap import heap
from math import inf, sqrt
import networkx as nx
from matplotlib import pyplot as plt


class vis:

    def __init__(self, file):
        file_info = self.process(file)
        self.path = []
        self.blocked_path = []
        self.answer = []
        self.start, self.end, self.dim = file_info[:3]
        self.blocked = file_info[3:]
        self.blocked_paths(file_info)
        self.points = []
        self.path_finder(file_info)
        self.algorithm()
        self.graph()

    
        
        


    def path_finder(self, file_info):

        points = []

        for point in self.blocked:
            if [point[0], point[1]] not in points:
                points.append([point[0], point[1]])
            if [point[0]+1, point[1]] not in points:
                points.append([point[0]+1, point[1]])
            if [point[0], point[1]+1] not in points:
                points.append([point[0], point[1]+1])
            if [point[0]+1, point[1]+1] not in points:
                points.append([point[0]+1, point[1]+1])
        
        if self.start not in points:
            points.append(self.start)
        if self.end not in points:
            points.append(self.end)
       

        self.points = points
        for i in points:
            for j in points:
                if i != j:
                    if self.lineofsight(i, j) and (i,j) not in self.path and (j,i) not in self.path and self.can_pass(i, j):
                        self.path.append((i, j))


    def blocked_paths(self, file_info):
        for cell in self.blocked:
            self.blocked_path.append([cell, [cell[0]+1, cell[1]+1]])
            self.blocked_path.append([[cell[0], cell[1]+1], [cell[0]+1, cell[1]]])
            #check if cell is the left most cell or if the left cell is blocked
            if (cell[0]==1 or ([cell[0]-1,cell[1]] in self.blocked)):
                if ([cell,[cell[0],cell[1]+1]] not in self.blocked_path):
                    self.blocked_path.append([cell,[cell[0],cell[1]+1]])
            #UP
            if (cell[1]==1 or ([cell[0],cell[1]-1] in self.blocked)):
                if ([cell,[cell[0]+1,cell[1]]] not in self.blocked_path):
                    self.blocked_path.append([cell,[cell[0]+1,cell[1]]])
            #RIGHT
            if (cell[0]==self.dim[0] or ([cell[0]+1,cell[1]] in self.blocked)):
                if ([[cell[0]+1,cell[1]],[cell[0]+1,cell[1]+1]] not in self.blocked_path):
                    self.blocked_path.append([[cell[0]+1,cell[1]],[cell[0]+1,cell[1]+1]])
            #DOWN
            if (cell[1]==self.dim[1] or ([cell[0],cell[1]+1] in self.blocked)):
                if ([[cell[0],cell[1]+1],[cell[0]+1,cell[1]+1]] not in self.blocked_path):
                    self.blocked_path.append([[cell[0],cell[1]+1],[cell[0]+1,cell[1]+1]])
        

    def process(self, file):
        list = []
        
        with open(file) as f:
            lines = f.readlines()
            
            for line in lines:
                args = line.strip("\n").split()
                if len(args) == 2:
                    list.append([int(args[0]), int(args[1])])
                else:
                    if int(args[2]) == 1:
                        list.append([int(args[0]), int(args[1])])
        return list

    def lineofsight(self, point1, point2):
        x0 = point1[0]
        y0 = point1[1]
        x1 = point2[0]
        y1 = point2[1]
        f = 0
        dy = y1-y0
        dx = x1-x0
        if dy < 0:
            dy = -dy
            sy = -1
        else:
            sy = 1
        if dx < 0:
            dx = -dx
            sx = -1
        else:
            sx = 1
        if dx >= dy:
            while x0 != x1:
                f = f+dy
                if f >= dx:
                    if [x0 + ((sx-1)/2), y0 + ((sy-1)/2)] in self.blocked:
                        return False
                    y0 = y0+sy
                    f = f-dx
                if f != 0 and [x0 + ((sx-1)/2), y0 + ((sy-1)/2)] in self.blocked:
                    return False
                if dy == 0 and [x0 + ((sx-1)/2), y0] in self.blocked and [x0 + ((sx-1)/2), y0-1] in self.blocked:
                    return False
                x0 = x0+sx
        else:
            while y0 != y1:
                f = f+dx
                if f >= dy:
                    if [x0 + ((sx-1)/2), y0 + ((sy-1)/2)] in self.blocked:
                        return False
                    x0 = x0+sx
                    f = f-dy
                if f != 0 and [x0 + ((sx-1)/2), y0 + ((sy-1)/2)] in self.blocked:
                    return False
                if dx == 0 and [x0, y0 + ((sy-1)/2)] in self.blocked and [x0-1, y0 + ((sy-1)/2)] in self.blocked:
                    return False
                y0 = y0+sy

        return True

    def can_pass(self, point1, point2):
        x0 = point1[0]
        y0 = point1[1]
        x1 = point2[0]
        y1 = point2[1]
        
        if x0 == x1: 
            for path in self.blocked_path:
                if path[0][0] == path[1][0] and path[0][0] == x0:
                    if ((path[0][1] in range(y0, y1+1)) or (path[0][1] in range(y1, y0+1))) and ((path[1][1] in range(y0, y1+1)) or (path[1][1] in range(y1, y0+1))):

                        return False
        elif y0 == y1:
            for path in self.blocked_path:
                if path[0][1] == path[1][1] and path[0][1] == y0:
                    if ((path[0][0] in range(x0, x1+1)) or (path[0][0] in range(x1, x0+1))) and ((path[1][0] in range(x0, x1+1)) or (path[1][0] in range(x1, x0+1))):
                        return False
        return True

    def algorithm(self):
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
        for point in self.path:
            if coordinate == point[0] and self.reachable(coordinate, point[1]):
                temp_node = nodeClass(None, point[1])
                temp_node.h = self.heuristic(temp_node.coordinates)
                node_list.append(temp_node)
            elif coordinate == point[1] and self.reachable(coordinate, point[0]):
                temp_node = nodeClass(None, point[0])
                temp_node.h = self.heuristic(temp_node.coordinates)
                node_list.append(temp_node)
        return node_list

    def reachable(self, coordinate, dest):
        for path in self.blocked_path:
            if coordinate in path and dest in path:
                return False
        return True
            
    def distance(self, point1, point2):
        return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


    def heuristic(self, node):
        return sqrt(2)*min(abs(node[0]-self.end[0]), abs(node[1]-self.end[1]))+max(abs(node[0]-self.end[0]), abs(node[1]-self.end[1]))-min(abs(node[0]-self.end[0]), abs(node[1]-self.end[1]))


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

    def graph(self):
        if self.answer:
            print(self.answer)
        else:
            print("No path found")

        grid_cols = self.dim[0]+1 #Columns
        grid_rows = self.dim[1]+1 #Rows

        #Generate a grid graph using the given paramters
        G = nx.grid_2d_graph(grid_cols,grid_rows) 

        #list of correct co-ordinates
        v_list = []
        for i in range(1,grid_cols+1):
            for j in range(1,grid_rows+1):
                v_list.append([i,j])

        vis_list = []

        #list of correct edges from the vertices list
        v_edge_list = self.path
        [v_edge_list.append(edge) for edge in self.blocked_path]

        # print(v_edge_list)

        #tuple of edges from the list of edges because networkx only works with tuples.
        e_tuple = []
        for eagle in v_edge_list:
            temp1 = tuple(tuple(t) for t in eagle)
            if temp1[0] not in vis_list:
                vis_list.append(temp1[0])
            if temp1[1] not in vis_list:
                vis_list.append(temp1[1])
            
            e_tuple.append(temp1)

        # tuple of vertices from list of vertices
        v_tuple = (tuple(x) for x in v_list)
        
        # map the default graph nodes to new graph nodes using dictionary
        p_dict = dict(zip(list(G), v_tuple))

        #rename the default co-ordinates
        G1=nx.relabel_nodes(G,p_dict)
        

        # print(p_dict)
        # print((vis_list))
        # print(list(G1.nodes))
        fig, ax = plt.subplots()

        # reposition the grid into correct position
        pos = {(x,y):(x,-y) for x,y in G1.nodes()}

        #tuple of nodes that are in the answer
        a_tuple = []
        if self.answer:
            for m in self.answer:
                temp2 = (tuple(m))
                a_tuple.append(temp2)

        #tuple of edges that are in the blocked list
        s_tuple = []
        for l in self.blocked_path:
            temp = tuple(tuple(x) for x in l)
            s_tuple.append(temp)

        #tuple of edges from the tuple of nodes from the answer
        new_tuple = []
        for tyt in range(len(a_tuple)-1):
            new_tuple.append((a_tuple[tyt],a_tuple[tyt+1]))
        
        for tup in new_tuple:
            if (tup[0],tup[1]) not in e_tuple:
                e_tuple.append(tup)

        for e in e_tuple:
            if (e[0],e[1]) in s_tuple or (e[1],e[0]) in s_tuple:
                G1.add_edge(e[0],e[1],color = 'r', style = 'solid')
            elif (e[0],e[1]) in new_tuple or (e[1],e[0]) in new_tuple:
                G1.add_edge(e[0],e[1],color = 'g', style = 'solid')
            else:
                G1.add_edge(e[0],e[1],color = 'black', style = 'dotted')

        nx.set_node_attributes(G1, values = 0, name='f_val')
        nx.set_node_attributes(G1, values = 0, name='g_val')
        nx.set_node_attributes(G1, values = 0, name='h_val')

        for nodes in self.visited:
            G1.add_node(tuple(nodes.coordinates), f_val=nodes.f, g_val=nodes.g, h_val= nodes.h)

        source = []
        source.append(tuple(self.start))
        end = []
        end.append(tuple(self.end))
        color_map =[]
        for v in list(G1.nodes):
            if v in source:
                color_map.append('chartreuse')
            elif v in end:
                color_map.append('fuchsia')
            elif v in a_tuple:
                color_map.append('yellow')
            elif v in vis_list:
                color_map.append('black')
            else:
                color_map.append('white')
        
        colors = [G1[u][v]['color'] for u,v in e_tuple]
        style = [G1[m][n]['style'] for m,n in e_tuple]

        #Draw the new graph
        nodes = nx.draw_networkx_nodes(G1, pos=pos, ax=ax, node_size=20)
        nodes.set_edgecolor('white')
        nx.draw(G1, pos=pos, 
                # with_labels= True,
                edge_color = colors,
                node_color = color_map,
                edgelist = e_tuple,
                node_size=20,
                width = [2 if (we[0],we[1]) in new_tuple or (we[1],we[0]) in new_tuple else 1 for we in e_tuple],
                style = style,
                font_weight=10,
                font_color="blue")

        annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def update_annot(ind):
            node = list(G1.nodes())[ind]
            # print (node)
            xy = pos[node]
            # print(xy)
            annot.xy = xy
            node_attr = {'node': node}
            node_attr.update(G1.nodes[node])
            text = '\n'.join(f'{k}: {v}' for k, v in node_attr.items())
            annot.set_text(text)

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == ax:
                cont, ind = nodes.contains(event)
                if cont:
                    test = (ind['ind'][0])
                    # print(list(G1.nodes())[test])
                    update_annot(test)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    if vis:
                        annot.set_visible(False)
                        fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover)

        plt.subplots_adjust(left = 0.01, bottom = 0.01, right = 1, top = 1)
        plt.margins(0.15)
        plt.show()
