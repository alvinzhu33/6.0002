# 6.0002 Problem Set 2
# Graph optimization
# Name: Alvin Zhu
# Collaborators:
# Time: 4

#
# Finding shortest paths through the Boston t
#


import unittest
from graph import Digraph, Node, WeightedEdge


# PROBLEM 2: Building up the Boston t Map
#
# PROBLEM 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the times
# represented?
#
# ANSWER: The graph's nodes represents the subway stations. The graph's edges represents the path between two subway stations (in other words, that a subway travels directly between them). The times between connected stations are represented by the weights assigned to every node.



# PROBLEM 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following format, separated by blank spaces:
            From To TotalTime LineColor
        e.g.
            green_st forest_hills 3 orange
        This entry would become an edge from green_st to forest_hills on the orange line. There should also be
        another edge from forest_hills to green_st on the orange line with time travelled = 3

    Returns:
        a directed graph representing the map
    """
    dig = Digraph()
    file = open(map_filename, 'r');

    for line in file:
        line = line.split()

        #Check and add Nodes to the digraph
        for x in range(2):
            if not dig.has_node(Node(line[x])):
                dig.add_node(Node(line[x]));

        #Add edges to the digraph
        info = WeightedEdge(Node(line[0]), Node(line[1]), line[2], line[3])
        dig.add_edge(info)

        info = WeightedEdge(Node(line[1]), Node(line[0]), line[2], line[3])
        dig.add_edge(info);

    return dig;


# PROBLEM 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
#dig = load_map("test_load_map.txt");
#print(dig)

# PROBLEM 3: Finding the Shortest Path using Optimized Search Method
#
# PROBLEM 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# ANSWER: We are trying to find the shortest path (minimum total time spent travelling) between a source node and destination node. We are constrained by not passing through certain color lines on the T.

# PROBLEM 3b: Implement add_node_to_path


def add_node_to_path(node, path):
    """
    Parameters:
        path: list composed of [[list of nodes], int]
            Represents the current path of nodes being traversed. Contains
            a list of nodes (Node) and total time traveled

        node: Node object
            Node of t stop being added to the path

    Returns:
        [[list of nodes], int] - A safely COPIED version of path with the Node added to the end of
        a COPY of the first element of path.

        This method should not mutate path or path[0]

    """
    return [path[0]+[node], path[1]];

# PROBLEM 3c: Implement get_best_path
def get_best_path(digraph, start, end, path, restricted_colors, best_time,
                  best_path):
    """
    Finds the shortest path between t stops subject to constraints.

    Parameters:
        digraph: Digraph
            The graph on which to carry out the search
        start: Node
            t stop at which to start
        end: Node
            t stop at which to end
        path: list composed of [[list of Nodes], int]
            Represents the current path of nodes being traversed. Contains
            a list of Nodes and total time traveled.
        restricted_colors: list[strings]
            Colors of lines not allowed on path
        best_time: int
            The shortest time between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of Nodes
            The path with the shortest total time found so far between the original start
            and end node.

    Returns:
        A tuple of the form (best_path, best_time).
        The first item is the shortest-path from start to end, represented by
        a list of t stops (Nodes).
        The second item is an integer, the length (time traveled)
        of the best path.


        If there exists no path that satisfies restricted_colors constraints, then return None.
    """
    #Checking if start and end Nodes are in digraph
    if not(digraph.has_node(start) or digraph.has_node(end)):
        raise ValueError;

    #Check if start Node = end Node
    elif start.get_name() == end.get_name():
        best_path = path[0];
        best_time = path[1];

    else:
        #Iterate through connection of a child
        for edge in digraph.get_edges_for_node(start):

            #Check if we already went through that edge and if we are not restricted from that edge
            if edge.get_destination() not in path[0] and edge.get_color() not in restricted_colors:

                #Create newPath  with the edge's destination tacked on to original path list and increment travel time
                #Optimize for when next path is longer than shortest path found so far 
                newPath = [path[0] + [edge.get_destination()], path[1] + edge.get_total_time()]
                if newPath[1] > best_time:
                    break;
                dfs = get_best_path(digraph, edge.get_destination(), end, newPath, restricted_colors, best_time, best_path);

                #Deals with multiple paths that go to the destination (pick the lowest time!)
                if dfs != None and dfs[1] < best_time:
                    best_path = dfs[0]
                    best_time = dfs[1];
    
    #Checks if any path exists at all
    if best_path == None:
        return None;
    return (best_path, best_time);


### USED FOR TESTING. PLEASE DO NOT CHANGE THIS FUNCTION.
def directed_dfs(digraph, start, end, restricted_colors):
    """
    Finds the shortest time path from start to end using a directed depth-first
    search. Minimize the total time and do not use the color lines in colors_not_used.

    Parameters:
        digraph: instance of Digraph
            The graph on which to carry out the search
        start: Node
            t-stop at which to start
        end: Node
            t-stop at which to end
        restricted_colors: list[string]
            Colors of lines not allowed in path

    Returns:
        The shortest-path from start to end, represented by
        a list of t stops (Nodes).

        If there exists no path that satisfies restricted_colors constraints, then raises a ValueError.
    """
    path = [[start], 0]  # begin at start node with 0 distance
    result = get_best_path(digraph, start, end, path, restricted_colors, 99999, None)

    if result is None:
        raise ValueError("No path from {} to {}".format(start, end))

    return result[0]


#UNCOMMENT THE FOLLOWING LINES TO DEBUG IF YOU WOULD LIKE TO

'''digr = load_map('t_map.txt')
print(digr)

start = Node('central')
end = Node('park_st')
restricted_colors = []

print(directed_dfs(digr, start, end, restricted_colors))'''

'''#Personal Testing
digr = load_map("test_load_map.txt");
print(digr);
start = Node('Javitts');
end = Node('34');
#print(directed_dfs(digr, start, end, ['S']))
#print(directed_dfs(digr, start, end, ['R']))'''