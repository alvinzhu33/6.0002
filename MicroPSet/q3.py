def greedy_cow_transport(cows,limit=10):
	"""
	cows: a dictionary of name (string), weight (int) pairs
	limit: weight limit of the spaceship (an int)

	Uses a greedy heuristic to determine an allocation of cows that attempts to
	minimize the number of spaceship trips needed to transport all the cows.

	The greedy heuristic should follow the following method:
	1. As long as the current trip can fit another cow, add the lightest 
	   cow that will fit to the trip
	2. Once the trip is full, begin a new trip to transport some of the remaining cows
	Does not mutate the dictionary cows.

	Returns a list of lists, with each inner list containing the names of cows
	transported on a particular trip. The list should be in the order of the trips.
	"""
	avail = {}
	for cow in cows:
		weight = cows[cow]
		if weight in avail:
			avail[weight] += [cow]
		else:
			avail[weight] = [cow]
	
	transports = []
	while avail:
		weights = 0
		transporting = []
		smallest = min(avail)
		while weights + smallest <= limit:
			if len(avail[smallest]) > 1:
				transporting += avail[smallest].pop()
			else:
				transporting += avail[smallest]
				del avail[smallest]
			weights += smallest
			
			if avail:
				smallest = min(avail)
			else:
				break
		if transporting:
			transports += [transporting]
		
		if smallest > limit:
			break
	
	return transports


cows = {"A": 6, "B": 3, "C": 2, "D": 4}
print(greedy_cow_transport(cows, 10))
cows = {"A": 6, "B": 4, "C": 4, "D": 4}
print(greedy_cow_transport(cows, 10))
cows = {"A": 6, "B": 3, "C": 2, "D": 5}
print(greedy_cow_transport(cows, 10))
cows = {"A": 6, "B": 3, "C": 2, "D": 5}
print(greedy_cow_transport(cows, 3))
cows = {"A": 50, "B": 10, "C": 20, "D":900}
print(greedy_cow_transport(cows, 100))
print(greedy_cow_transport(cows, 1))