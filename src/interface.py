import networkx as nx
from matplotlib import pyplot as plt

def graph(data_):
    if data_.answer:
        print(data_.answer)
    else:
        print("No path found")

    grid_cols = data_.dim[0]+1 #Columns
    grid_rows = data_.dim[1]+1 #Rows

    #Generate a grid graph using the given paramters
    G = nx.grid_2d_graph(grid_cols,grid_rows) 

    #list of correct co-ordinates
    v_list = []
    for i in range(1,grid_cols+1):
        for j in range(1,grid_rows+1):
            v_list.append([i,j])

    #list of correct edges from the vertices list
    v_edge_list = []
    for ed in v_list:
        ed_top_left = [ed[0] - 1,ed[1] - 1]
        if (ed_top_left in v_list) and ([ed,ed_top_left] and [ed_top_left, ed] not in v_edge_list):
            v_edge_list.append([ed,ed_top_left])
        
        ed_top = [ed[0],ed[1]-1]
        if (ed_top in v_list) and ([ed,ed_top] and [ed_top, ed] not in v_edge_list):
            v_edge_list.append([ed,ed_top])

        ed_top_right = [ed[0]+1,ed[1]-1]
        if (ed_top_right in v_list) and ([ed,ed_top_right] and [ed_top_right, ed] not in v_edge_list):
            v_edge_list.append([ed,ed_top_right])

        ed_right = [ed[0]+1,ed[1]]
        if (ed_right in v_list) and ([ed,ed_right] and [ed_right, ed] not in v_edge_list):
            v_edge_list.append([ed,ed_right])

        ed_bottom_right = [ed[0]+1,ed[1]+1]
        if (ed_bottom_right in v_list) and ([ed,ed_bottom_right] and [ed_bottom_right, ed] not in v_edge_list):
            v_edge_list.append([ed,ed_bottom_right])

        ed_bottom = [ed[0],ed[1]+1]
        if (ed_bottom in v_list) and ([ed,ed_bottom] and [ed_bottom, ed] not in v_edge_list):
            v_edge_list.append([ed,ed_bottom])

        ed_bottom_left = [ed[0]-1,ed[1]+1]
        if (ed_bottom_left in v_list) and ([ed,ed_bottom_left] and [ed_bottom_left, ed] not in v_edge_list):
            v_edge_list.append([ed,ed_bottom_left])

        ed_left = [ed[0]-1,ed[1]]
        if (ed_left in v_list) and ([ed,ed_left] and [ed_left, ed] not in v_edge_list):
            v_edge_list.append([ed,ed_left])

    #tuple of edges from the list of edges because networkx only works with tuples.
    e_tuple = []
    for eagle in v_edge_list:
        temp1 = tuple(tuple(t) for t in eagle)
        e_tuple.append(temp1)

    # tuple of vertices from list of vertices
    v_tuple = (tuple(x) for x in v_list)

    # map the default graph nodes to new graph nodes using dictionary
    p_dict = dict(zip(list(G), v_tuple))

    #rename the default co-ordinates
    G1=nx.relabel_nodes(G,p_dict)

    fig, ax = plt.subplots()

    # reposition the grid into correct position
    pos = {(x,y):(x,-y) for x,y in G1.nodes()}

    #tuple of nodes that are in the answer
    a_tuple = []
    if data_.answer:
        for m in data_.answer:
            temp2 = (tuple(m))
            a_tuple.append(temp2)

    #tuple of edges that are in the blocked list
    s_tuple = []
    for l in data_.blocked_path:
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

    for nodes in data_.visited:
        G1.add_node(tuple(nodes.coordinates), f_val=nodes.f, g_val=nodes.g, h_val= nodes.h)

    source = []
    source.append(tuple(data_.start))
    end = []
    end.append(tuple(data_.end))
    color_map =[]
    for v in list(G1.nodes):
        if v in source:
            color_map.append('chartreuse')
        elif v in end:
            color_map.append('fuchsia')
        elif v in a_tuple:
            color_map.append('yellow')
        else:
            color_map.append('black')
    
    colors = [G1[u][v]['color'] for u,v in e_tuple]
    style = [G1[m][n]['style'] for m,n in e_tuple]
    
    #Draw the new graph
    nodes = nx.draw_networkx_nodes(G1, pos=pos, ax=ax, node_size=20)
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