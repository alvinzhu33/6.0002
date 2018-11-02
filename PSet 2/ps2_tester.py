#!/usr/bin/env python

from ps2 import *
from graph import *
import unittest

unittest.TestLoader.sortTestMethodsUsing = None


class InternalPs2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = Digraph()
        cls.na = Node('haymarket')
        cls.nb = Node('state')
        cls.nc = Node('government_center')
        
        #for best path tests
        cls.airport = Node('airport')
        cls.maverick = Node('maverick')
        cls.aquarium = Node('aquarium')
        cls.mgh = Node('mgh')
        cls.kendall = Node('kendall')
        cls.andrew = Node('andrew')
        cls.broadway = Node('broadway')
        cls.south_station = Node('south_station')
        cls.downtown_crossing = Node('downtown_crossing')
        cls.park_st = Node('park_st')
        cls.boylston = Node('boylston')
        cls.arlington = Node('arlington')
        cls.haymarket = Node('haymarket')
        cls.government_center = Node('government_center')
        
        cls.fields_corner = Node('fields_corner')
        cls.state = Node('state')
        cls.copley = Node('copley')
        cls.backbay = Node('backbay')
        cls.wood_island = Node('wood_island')
        cls.orient_heights = Node('orient_heights')
        cls.suffolk_downs = Node('suffolk_downs')
        cls.beachmont = Node('beachmont')
        cls.central = Node('central')
        
        
        cls.g.add_node(cls.na)
        cls.g.add_node(cls.nb)
        cls.g.add_node(cls.nc)
        cls.e1 = WeightedEdge(cls.na, cls.nb, 4, 'orange')
        cls.e2 = WeightedEdge(cls.na, cls.nc, 4, 'green')
        cls.e3 = WeightedEdge(cls.nb, cls.nc, 2, 'blue')
        cls.g.add_edge(cls.e1)
        cls.g.add_edge(cls.e2)
        cls.g.add_edge(cls.e3)
        cls.graph = load_map("t_map.txt")

    # ------------------------------------------------ testing graph.py

    def test_graph1_weighted_edge_src(self):
        self.assertEqual(str(self.e1.get_source()), str(self.na))
        self.assertEqual(str(self.e2.get_source()), str(self.na))
        self.assertEqual(str(self.e3.get_source()), str(self.nb))

    def test_graph2_weighted_edge_dest(self):
        self.assertEqual(str(self.e1.get_destination()), str(self.nb))
        self.assertEqual(str(self.e2.get_destination()), str(self.nc))
        self.assertEqual(str(self.e3.get_destination()), str(self.nc))

    def test_graph3_weighted_edge_str(self):
        self.assertEqual(str(self.e1), "haymarket -> state 4 orange")
        self.assertEqual(str(self.e2), "haymarket -> government_center 4 green")
        self.assertEqual(str(self.e3), "state -> government_center 2 blue")

    def test_graph4_weighted_edge_total_time(self):
        self.assertEqual(self.e1.get_total_time(), 4)
        self.assertEqual(self.e2.get_total_time(), 4)
        self.assertEqual(self.e3.get_total_time(), 2)

    def test_graph5_add_edge_to_nonexistent_node_raises(self):
        node_not_in_graph = Node('q')
        no_src = WeightedEdge(self.nb, node_not_in_graph, 5, 'purple')
        no_dest = WeightedEdge(node_not_in_graph, self.na, 5, 'purple')

        with self.assertRaises(ValueError):
            self.g.add_edge(no_src)
        with self.assertRaises(ValueError):
            self.g.add_edge(no_dest)

    def test_graph6_add_existing_node_raises(self):
        with self.assertRaises(ValueError):
            self.g.add_node(self.na)

    def test_graph7_str(self):
        lines = ["haymarket -> state 4 orange","haymarket -> government_center 4 green","state -> government_center 2 blue"]
        actual = str(self.g).split("\n")
        self.assertIn(lines[0], actual, "Your printed graph does not match the correct string")
        self.assertIn(lines[1], actual, "Your printed graph does not match the correct string")
        self.assertIn(lines[2], actual, "Your printed graph does not match the correct string")


    # ------------------------------------------------ testing ps2.py

    def test_ps2_load_map_t_map(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 63)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 136)
        
    def test_ps2_add_node_to_path(self):
        added_node = self.airport
        path = [[self.na, self.nb, self.nc], 1, 1]
        new_path = add_node_to_path(added_node, path)
        self.assertNotIn(added_node, path[0], "The original path has been mutated. A copy of the path has not been returned")
        self.assertIn(self.na, new_path[0], "The new node's name has not been added correctly into the path.")
        self.assertIn(self.nb, new_path[0], "The new node's name has not been added correctly into the path.")
        self.assertIn(added_node, new_path[0], "The new node's name has not been added correctly into the path.")
        self.assertEqual(len(path), 3, "Node name has been added to path, not the first element in path.")
        self.assertEqual(len(new_path[0]), 4, "Node name has not been added correctly into the path.")
        self.assertEqual(path[1], 1, "path[1] has been modified when it should not be.")
        self.assertEqual(path[2], 1, "path[2] has been modified when it should not be.")

    def _print_path_description(self, start, end, restricted_colors):
        constraint = ""
        if restricted_colors != []:
            constraint += " and without using the {} line(s)".format(restricted_colors)
        print("------------------------")
        print("Shortest path from T stop {} to {} {}".format(
            start, end, constraint))

    def _test_path(self, graph,expectedPath,message="",restricted_colors = []):
        
        start, end = expectedPath[0][0], expectedPath[0][-1]
        self._print_path_description(start, end, restricted_colors)
        dfsPath = directed_dfs(graph, start, end, restricted_colors)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertIn(dfsPath, expectedPath, message)

    def _test_impossible_path(self, graph,
                              start,
                              end,
                              restricted_colors=[], message=""):
        
        self._print_path_description(start, end, restricted_colors)
        try:
            path = directed_dfs(graph, start, end,restricted_colors)
            print(path)
            self.fail()
        except:
            with self.assertRaises(ValueError):
                directed_dfs(graph, start, end, restricted_colors)
                print(message)

    def test_ps2_mit_map1_path_one_step(self):
        self._test_path(self.graph, expectedPath=[[self.airport, self.maverick]], message="The path goes one step. Make sure you are looking at all of the neighboring nodes.")

    def test_ps2_mit_map2_path_limited_time(self):
        self._test_path(self.graph,
            expectedPath=[[self.aquarium, self.mgh, self.kendall]], message="This tests having a limited number of time to travel. Make sure your dfs is finding the shortest path.")
    
    def test_ps2_mit_map3_path_restricted_path(self):
        self._test_path(self.graph, expectedPath=[[self.andrew, self.broadway, self.south_station, self.downtown_crossing, self.park_st, self.boylston, self.arlington]], restricted_colors=['purple'],message="The path tests having a restricted list of colors (lines that can't be used). Make sure your DFS is finding the shortest correct path.")

    def test_ps2_mit_map_path_start_end_same(self):
        self._test_path(self.graph,expectedPath=[[self.fields_corner]], message="If the start and end are the same, the path should only be the start node")
        
    def test_ps2_mit_map_path_same_length_different_time(self):
        self._test_path(self.graph,expectedPath=[[self.state,self.downtown_crossing,self.park_st]], message="Should return path that has the shortest length of all edges combined")
        
    def test_ps2_mit_map_path_multiple_colors_not_allowed(self):
        self._test_path(self.graph,expectedPath=[[self.downtown_crossing, self.state, self.haymarket, self.government_center, self.park_st]], restricted_colors = ['red','blue'], message= "Make sure your search works with multiple restricted colors")
        
    def test_ps2_mit_map_path_long_path_no_edges(self):
        self._test_path(self.graph,expectedPath=[[self.state,self.government_center,self.park_st]], restricted_colors = ['orange'], message="Be sure you don't use any lines in restricted colors")
        
    def test_ps2_mit_map_path_bus(self):
        self._test_path(self.graph,expectedPath=[[self.copley,self.backbay]], restricted_colors = [], message="Be sure you don't use any lines in restricted colors")
    
    def test_ps2_mit_map_path_long(self):
        self._test_path(self.graph,expectedPath=[[self.copley, self.arlington, self.boylston, self.park_st, self.downtown_crossing, self.state, self.aquarium, self.maverick, self.airport, self.wood_island, self.orient_heights, self.suffolk_downs, self.beachmont]], restricted_colors = [], message="Be sure you are returning the shortest path")

    def test_impossible_path_no_blue(self):
        self._test_impossible_path(self.graph,start = self.central,end = self.kendall, restricted_colors = ['red'], message="Should be impossible")
        
    def test_impossible_path_no_red(self):
        self._test_impossible_path(self.graph,start = self.maverick,end = self.copley, restricted_colors = ['blue'], message="Should be impossible")
        


if __name__ == "__main__":
    #unittest.main(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(InternalPs2Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
