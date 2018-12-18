class Node(object):
	"""Represents a node in the graph"""

	def __init__(self, name):
		self.name = str(name)

	def get_name(self):
		''' return: the name of the node '''
		return self.name

	def __str__(self):
		''' return: The name of the node.
				This is the function that is called when print(node) is called.
		'''
		return self.name

	def __repr__(self):
		''' return: The name of the node.
				Formal string representation of the node
		'''
		return self.name

	def __eq__(self, other):
		''' returns: True is self == other, false otherwise
				 This is function called when you used the "==" operator on nodes
		'''
		return self.name == other.name

	def __ne__(self, other):
		''' returns: True is self != other, false otherwise
				This is function called when you used the "!=" operator on nodes
		'''
		return not self.__eq__(other)

	def __hash__(self):
		''' This function is necessary so that Nodes can be used as
		keys in a dictionary, Nodes are immutable
		'''
		return self.name.__hash__()


class WeightedEdge(object):
	"""Represents an edge with an integer weight"""

	def __init__(self, src, dest, rate):
		""" Initialize  src, dest, total_time, and color for the WeightedEdge class
			src: Node representing the source node
			dest: Node representing the destination node
			total_time: int representing the time travelled between the src and dest
			color: string representing the t line color of the edge
		"""
		self.src = src
		self.dest = dest
		self.rate = rate

	def get_source(self):
		""" Getter method for WeightedEdge
			returns: Node representing the source node """
		return self.src

	def get_destination(self):
		""" Getter method for WeightedEdge
			returns: Node representing the destination node """
		return self.dest

	def get_rate(self):
		""" Getter method for WeightedEdge
			returns: float representing the rate between the source and dest nodes"""
		return self.rate

	def __str__(self):
		""" to string method
			returns: string with the format 'src -> dest total_time color' """
		return self.src.get_name() + ' -> ' + self.dest.get_name() + " " + str(self.rate)


class Digraph(object):
	"""Represents a directed graph of Node and WeightedEdge objects"""

	def __init__(self):
		self.nodes = set([])
		self.edges = {}  # must be a dictionary of Node -> list of edges starting at that node

	def __str__(self):
		edge_strs = []
		for edges in self.edges.values():
			for edge in edges:
				edge_strs.append(str(edge))
		edge_strs = sorted(edge_strs)  # sort alphabetically
		return '\n'.join(edge_strs)  # concat edge_strs with "\n"s between them

	def get_edges_for_node(self, node):
		''' param: node object
			return: a copy of the list of all of the edges for given node.
					empty list if the node is not in the graph
		'''
		return [item for item in self.edges[node]]

	def has_node(self, node):
		''' param: node object
			return: True, if node is in the graph. False, otherwise.
		'''
		return node in self.nodes

	def add_node(self, node):
		""" param: node object
			Adds a Node object to the Digraph.
			Raises a ValueError if it is already in the graph."""
		if node in self.nodes:
			raise ValueError
		self.nodes.add(node)  # Add to a set
		self.edges[node] = []  # Instantiate a key in edges {}.

	def add_edge(self, edge):
		""" param: WeightedEdge object
			Adds a WeightedEdge instance to the Digraph.
			Raises a ValueError if either of the nodes associated with the edge is not in the graph."""
		#Check if both nodes of an edge are in the digraph and whether the edge has already been added.
		if edge.get_source() in self.nodes and edge.get_destination() in self.nodes:
			if edge not in self.edges[edge.get_source()]:
				self.edges[edge.get_source()] += [edge]
		else:
			raise ValueError

def load_map(exchange_rates):
	dig = Digraph()
	for rate in exchange_rates:
		for x in range(2):
			if not dig.has_node(Node(rate[x])):
				dig.add_node(Node(rate[x]))

		#Add edges to the digraph
		info = WeightedEdge(Node(rate[0]), Node(rate[1]), rate[2])
		dig.add_edge(info)

		info = WeightedEdge(Node(rate[1]), Node(rate[0]), 1/rate[2])
		dig.add_edge(info)
	return dig


def get_best_path(digraph, start, end, path, best_time, best_path):
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
		raise ValueError

	#Check if start Node = end Node
	elif start.get_name() == end.get_name():
		best_path = path[0]
		best_time = path[1]

	else:
		#Iterate through connection of a child
		for edge in digraph.get_edges_for_node(start):

			#Check if we already went through that edge and if we are not restricted from that edge
			if edge.get_destination() not in path[0]:

				#Create newPath  with the edge's destination tacked on to original path list and increment travel time
				#Optimize for when next path is longer than shortest path found so far
				newPath = [path[0] + [edge.get_destination()],
						   path[1]*edge.get_rate()]
				if newPath[1] < best_time:
					break
				dfs = get_best_path(digraph, edge.get_destination(), end, newPath, best_time, best_path)

				#Deals with multiple paths that go to the destination (pick the lowest time!)
				if dfs != None and dfs[1] > best_time:
					best_path = dfs[0]
					best_time = dfs[1]

	#Checks if any path exists at all
	if best_path == None:
		return None
	return (best_path, best_time)


def exchange_money(exchange_rates, amount, currency_from, currency_to):
	"""
	exchange_rates: list of lists for all exchange rates, where one exchange rate
			is represented as: [currency_from, currency_to, exchange_rate]
	exchange_rate: positive and non-zero float s.t.
			amount_of_currency_from*exchange_rate = amount_of_currency_to
			amount_of_currency_to*(1/exchange_rate) = amount_of_currency_from
	currency_from, currency_to: str
	amount: float representing the amount of money you wish to exchange
	currency_from: string representing the currency that 'amount' is in
	currency_to: string representing the currency you wish to change 'amount' to
		
	Returns a float, rounded to 2 decimal places, representing the maximum amount
	of currency_to that can be achieved by using the exchange rates in exchange_rates to  
	exchange the amount of currency_from.

	If there is no path from curency_from to currency_to, returns None
	Hint: you should utilize classes from previous problem sets.
	"""
	dig = load_map(exchange_rates)
	start = Node(currency_from)
	end = Node(currency_to)
	
	if dig.has_node(start) and dig.has_node(end):
		ans = get_best_path(dig, Node(currency_from), Node(currency_to), [[], amount], 0, [])[1]
		
		if ans:
			return round(ans, 2)
		return None
	return None


exchange_rates = [["USD", "EUR", 0.90], ["MXN", "JPY", 5.57], ["JPY", "EUR", 0.0078], ["USD", "AUS", 9], ["JPY", "AUS", .007], ["USD", "MXN", 230.824], ["IND", "KOR", 5]]
print(exchange_money(exchange_rates, 1, "ASS", "ASS"))
print(exchange_money(exchange_rates, 1, "ASS", "AUS"))
print(exchange_money(exchange_rates, 1, "AUS", "ASS"))
print(exchange_money(exchange_rates, 1, "KOR", "AUS"))
print(exchange_money(exchange_rates, 1, "AUS", "IND"))
print(exchange_money(exchange_rates, 1, "USD", "MXN"))
print(exchange_money(exchange_rates, 1.5, "USD", "MXN"))
print(exchange_money(exchange_rates, 2, "USD", "MXN"))
ex = [["A", "B", 2], ["B","C",2], ["C", "D", 2], ["A", "E", 5], ["E", "C", 2]]
print(exchange_money(ex, 1, "A", "C"))
exchange_rates = [["USD", "EUR", 0.88], ["MXN", "JPY", 5.57], ["JPY", "EUR",0.0078]]
print(exchange_money(exchange_rates, 3, "USD", "MXN"))