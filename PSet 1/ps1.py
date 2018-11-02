################################################################################
## 6.0002 Fall 2018
## Problem Set 1
## Written By: habadio, mkebede
## Name: Alvin Zhu
## Collaborators:
## Time: 7 hours


# Problem 1
class State():
    """
    A class representing the election results for a given state.
    Assumes there are no ties between dem and gop votes. The party with a
    majority of votes receives all the Electoral College (EC) votes for
    the given state.
    """
    def __init__(self, name, dem, gop, ec):
        """
        Parameters:
        name - the 2 letter abbreviation of a state
        dem - number of Democrat votes cast
        gop - number of Republican votes cast
        ec - number of EC votes a state has

        Attributes:
        self.name - str, the 2 letter abbreviation of a state
        self.winner - str, the winner of the state, "dem" or "gop"
        self.margin - int, difference in votes cast between the two parties, a positive number
        self.ec - int, number of EC votes a state has
        """
        self.name = name;
        self.winner = "dem" if dem > gop else "gop";
        self.margin = abs(dem - gop);
        self.ec = ec;

    def get_name(self):
        """
        Returns:
        str, the 2 letter abbreviation of the state
        """
        return self.name;

    def get_ecvotes(self):
        """
        Returns:
        int, the number of EC votes the state has
        """
        return self.ec;

    def get_margin(self):
        """
        Returns:
        int, difference in votes cast between the two parties, a positive number
        """
        return self.margin;

    def get_winner(self):
        """
        Returns:
        str, the winner of the state, "dem" or "gop"
        """
        return self.winner;

    def __str__(self):
        """
        Returns:
        str, representation of this state in the following format,
        "In <state>, <ec> EC votes were won by <winner> by a <margin> vote margin."
        """
        return "In " + self.name + ", " + str(self.ec) + " EC votes were won by " + self.winner + " by a " + str(self.margin) + " vote margin."

    def __eq__(self, other):
        """
        Determines if two State instances are the same.
        They are the same if they have the same state name, winner, margin and ec votes
        Note: Allows you to check if State_1 == State_2

        Param:
        other - State object to compare against

        Returns:
        bool, True if the two states are the same, False otherwise
        """
        if self.name == other.name and self.winner == other.winner and self.margin == other.margin and self.ec == other.ec:
            return True;
        return False;


# Problem 2
def load_election_results(filename):
    """
    Reads the contents of a file, with data given in the following tab-delimited format,
    State   Democrat_votes    Republican_votes    EC_votes

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a list of State instances
    """
    #Deal with file
    file = open(filename, 'r')
    file.readline(); #Deals with first line of the file (the headers)

    #Populate a list of state instance by looking over each line of file (aside from the first line which I already dealt with)
    states = []
    for line in file:
        info = line.split()
        states += [State(info[0], int(info[1]), int(info[2]), int(info[3]))];

    return states;

# Problem 3
def find_winner(election):
    """
    Finds the winner of the election based on who has the most amount of EC votes.
    Note: In this simplified representation, all of EC votes from a state go
    to the party with the majority vote.

    Parameters:
    election - a list of State instances

    Returns:
    a tuple, (winner, loser) of the election i.e. ('dem', 'gop') if Democrats won, else ('gop', 'dem')
    """
    #Utilize a dictionar to keep track of the winning party based on EC votes. Loop through each state in election and extract the state's EC votes to add to their party key in the dictionary.
    votes = {'gop': 0, 'dem':0}
    for state in election:
        votes[state.get_winner()] += state.get_ecvotes();

    if votes['gop'] > votes['dem']:
        return ('gop', 'dem');
    return ('dem', 'gop')

def states_lost(election):
    """
    Finds the list of States that were lost by the losing candidate (states won by the winning candidate).

    Parameters:
    election - a list of State instances

    Returns:
    A list of State instances lost by the loser (won by the winner)
    """
    #Determine which party won the elecction
    if find_winner(election) == ('gop', 'dem'):
        winner = 'gop'
    else: winner = 'dem';

    #Populate list of State instances won by the winner by looping through each state in the election and appending that state to the list if the winner of the state is the winner of the election
    lost = []
    for state in election:
        if state.get_winner() == winner:
            lost += [state];

    return lost;

def ec_votes_reqd(election, total=538):
    """
    Finds the number of additional EC votes required by the loser to change election outcome.
    Note: A party wins when they earn half the total number of EC votes plus 1.

    Parameters:
    election - a list of State instances
    total - total possible number of EC votes

    Returns:
    int, number of additional EC votes required by the loser to change the election outcome
    """
    #Determine loser of election
    if find_winner(election) == ('gop', 'dem'):
        loser = 'dem';
    else: loser = 'gop';

    #Count the number of EC votes garnered by the loser
    votes = 0
    for state in election:
        if state.get_winner() == loser:
            votes += state.get_ecvotes();

    #To win the election, a party must get half the total number of EC votes + 1. Thus, to get the number of votes a loser needs to win, you need that number - the votes the loser garnered.
    return total//2 + 1 - votes;

# Problem 4
def greedy_election(lost_states, ec_votes_needed):
    """
    Finds a subset of lost_states that would change an election outcome if
    voters moved into those states. First chooses the states with the smallest
    win margin, i.e. state that was won by the smallest difference in number of voters.
    Continues to choose other states up until it meets or exceeds the ec_votes_needed.
    Should only return states that were originally lost by the loser (won by the winner) in the election.

    Parameters:
    lost_states - a list of State instances that were lost by the loser of the election
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """
    #Create a dictionary with key as the margin and value as a dictionary where the key is the number of EC votes and the value the state instance;
    stateVotes = {}
    for state in lost_states:
        if state.get_margin() in stateVotes:
                stateVotes[state.get_margin()][state.get_ecvotes()] = state
        else:
            stateVotes[state.get_margin()] = {state.get_ecvotes(): state};

    #Populate list of state instances representing swing states by repeatedly determining the state with the least margin, updating the EC votes needed given you obtained those states, and deleting that state from the dictionary
    swings = []
    while len(stateVotes) > 0:
        #We're done if we do not need any more EC votes!
        if ec_votes_needed < 1:
            return swings;

        minMargin = stateVotes[min(stateVotes)] #Get dictionary value for states with the least margin
        maxEC = minMargin[max(minMargin)] #Get state for the state with the least margin but greatest EC votes
        #Remove from the dictionary the state with the least margin but greatest EC votes.
        if len(minMargin) > 1:
            del minMargin[max(minMargin)]
        else:
            del stateVotes[min(stateVotes)];

        ec_votes_needed -= maxEC.get_ecvotes() #Update EC votes needed
        swings += [maxEC]; #Add that state to swings

    #Return the list if we successfully won the election, else return an empty list.
    if ec_votes_needed < 1:
        return swings
    return [];

# Problem 5
def dp_move_max_voters_get(lost_states, ec_votes, memo = None):
    """
    Finds the largest number of voters needed to relocate to get at most ec_votes
    for the election loser. Analogy to the knapsack problem:
    Given a list of states each with a weight(#ec_votes) and value(#margin),
    determine the states to include in a collection so the total weight(#ec_votes)
    is less than or equal to the given limit(ec_votes) and the total value(#voters displaced)
    is as large as possible.
    """
    #Checck if dp instance already in memo
    if (len(lost_states), ec_votes) in memo:
        result = memo[(len(lost_states), ec_votes)]
    #Check for invalid instances (no more lost states or we surpass the max EC votes)
    elif lost_states == [] or ec_votes <= 0:
        result = (0, ());
    #Ignore the case when the state at hand has EC votes greater than the max
    elif lost_states[0].get_ecvotes() > ec_votes:
        result = dp_move_max_voters_get(lost_states[1:], ec_votes, memo);
    else:
        #Test which case has the greater number of people/margin: if you take that state vs if you leave that state.
        takeVal, takeLeft = dp_move_max_voters_get(lost_states[1:], ec_votes - lost_states[0].get_ecvotes(), memo)
        takeVal += lost_states[0].get_margin()
        leaveVal, leaveLeft = dp_move_max_voters_get(lost_states[1:], ec_votes, memo)
        if takeVal > leaveVal:
            result = (takeVal, takeLeft + (lost_states[0],))
        else:
            result = (leaveVal, leaveLeft);
    memo[(len(lost_states), ec_votes)] = result #Update the memo with our hard work to save time later!

    return result;

def dp_move_max_voters(lost_states, ec_votes, memo = None):
    '''
    Parameters:
    lost_states - a list of State instances that were lost by the loser
    ec_votes - int, the maximum number of EC votes
    memo - dictionary, an OPTIONAL parameter for memoization (don't delete!).
    Note: If you decide to use the memo make sure to override the default value when it's first called.

    Returns:
    A list of State instances such that the maximum number of voters need to be relocated
    to these states in order to get at most ec_votes
    The empty list, if no possible states
    '''
    #dp_move_max_voters_get returns  a tuple of length 2 where the first index is the total margin and the second is the list of state instances we actually want.
    #For a more intuitive dp_move_max_voters_get, I decided to split the code up so that the main function just returns the second element of the tuple
    return dp_move_max_voters_get(lost_states, ec_votes, {})[1];

def move_min_voters(lost_states, ec_votes_needed):
    """
    Finds a subset of lost_states that would change an election outcome if
    voters moved into those states. Should minimize the number of voters being relocated.
    Only return states that were originally lost by the loser (won by the winner)
    of the election.
    Hint: This problem is simply the complement of dp_move_max_voters

    Parameters:
    lost_states - a list of State instances that the loser of the election lost
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """
    #move_min_voters is essentially the complement of dp_move_max_voters. We thus first calculate the total EC votes received by the loser in the states they won.
    total_ec_votes = 0
    for state in lost_states:
        total_ec_votes += state.get_ecvotes();

    #Call dp_move_max_voters with parameters lost_states and extra votes they can have (total EC - votes they need). This gives us the complement of what we want since dp_move_max_voters will tell us which states to phase out (ones with the highest margin and EC votes that are lower than extra votes we can have)
    maxx = dp_move_max_voters(lost_states, total_ec_votes-ec_votes_needed)
    minn = [state for state in lost_states if state not in maxx] #Find states in lost_states that aren't in the states we want to phase out
    return minn;

#Problem 6
def flip_election(election, swing_states):
    """
    Finds a way to shuffle voters in order to flip an election outcome.
    Moves voters from states that were won by the losing candidate (any state not in lost_states),
    to each of the states in swing_states. To win a swing state, must move (margin + 1) new voters into that state.
    Also finds the number of EC votes gained by this rearrangement, as well as the minimum number of
    voters that need to be moved.

    Parameters:
    election - a list of State instances representing the election
    swing_states - a list of State instances where people need to move to flip the election outcome
                   (result of move_min_voters or greedy_election)

    Return:
    A tuple that has 3 elements in the following order:
        - a dictionary with the following (key, value) mapping:
            - Key: a 2 element tuple, (from_state, to_state), the 2 letter abbreviation of the State
            - Value: int, number of people that are being moved
        - an int, the total number of EC votes gained by moving the voters
        - an int, the total number of voters moved
    None, if it is not possible to sway the election
    """
    #Determine the states we won. If we did not win any states, we cannot win the election!
    lost_states = states_lost(election)
    win_states = [state for state in election if state not in lost_states];
    if len(win_states) == 0:
        return None;

    #Loop through both the states won and the swing dates to allocate votes from the win states to the swing states
    flip = [{}, 0, 0] #I chose to deal with a list because I will be modifying the 2nd and 3rd indices.
    swing_index = 0
    marginNeed = swing_states[swing_index].get_margin()+1 #To win a state, you need more of your party than the other (it cannot tie). This is the amount of votes a swing state needs to flip.
    for state in win_states:
        marginGive = state.get_margin()-1 #Amount of votes a winning state can give
        while swing_index < len(swing_states):
            #Once a swing state is successfully dealt with, move on to the next state
            if marginNeed == 0:
                marginNeed = swing_states[swing_index].get_margin() + 1;

            #Case 1: votes winning state can give > votes a swing states needs. Move on to the next swing state; Keep dealing with the current winning state but with a lower number of votes they can give.
            if marginGive > marginNeed:
                marginGive -= marginNeed
                flip[0][(state.get_name(), swing_states[swing_index].get_name())] = marginNeed
                flip[1] += swing_states[swing_index].get_ecvotes()
                flip[2] += marginNeed
                marginNeed = 0
                swing_index += 1;
            #Case 2: votes winning state can give = votes a swing states needs. Move on to the next winning state and swing state (by breaking the current while loop).
            elif marginGive == marginNeed:
                flip[0][(state.get_name(), swing_states[swing_index].get_name())] = marginGive
                flip[1] += swing_states[swing_index].get_ecvotes()
                flip[2] += marginNeed
                marginNeed = 0
                swing_index += 1
                break;
            else: #Case 3: votes winning state can give < votes a swing state needs. Move on to the next winning state; keep dealing with the current swing state but with a lower number of votes needed to flip (by breaking the current while loop).
                marginNeed -= marginGive
                flip[0][(state.get_name(), swing_states[swing_index].get_name())] = marginGive
                flip[2] += marginGive
                break;

    #If we went through every winning state but still have not taken care of each swing state, there is no way to win the election! Otherwise (if each swing state is already accounted for), we found the answer!
    if swing_index < len(swing_states):
        return None;
    return tuple(flip);


if __name__ == "__main__":
    pass
    # Uncomment the following lines to test each of the problems

    # # tests Problem 1 and Problem 2
    election2012 = load_election_results("2012_results.txt")

    # # tests Problem 3
    winner, loser = find_winner(election2012)
    lost_states = states_lost(election2012)
    names_lost_states = [state.get_name() for state in lost_states]
    ec_votes_needed = ec_votes_reqd(election2012)
    print("Winner:", winner, "\nLoser:", loser)
    print("EC votes needed:",ec_votes_needed)
    print("States lost by the loser: ", names_lost_states, "\n")

    # tests Problem 4
    print("greedy_election")
    greedy_swing = greedy_election(lost_states, ec_votes_needed)
    names_greedy_swing = [state.get_name() for state in greedy_swing]
    voters_greedy = sum([state.get_margin()+1 for state in greedy_swing])
    ecvotes_greedy = sum([state.get_ecvotes() for state in greedy_swing])
    print("Greedy swing states results:", names_greedy_swing)
    print("Greedy voters displaced:", voters_greedy, "for a total of", ecvotes_greedy, "Electoral College votes.", "\n")

    '''PERSONAL TESTING
    election2008 = load_election_results("2008_results.txt")
    lost_states08 = states_lost(election2008)
    total_lost08 = sum(state.get_ecvotes() for state in lost_states08)
    ec_votes_needed08 = ec_votes_reqd(election2008)
    move_max08 = dp_move_max_voters(lost_states08, total_lost08-ec_votes_needed08)
    print("YOOO",[state.get_name() for state in move_max08])
    election2016 = load_election_results("2016_results.txt")
    lost_states16 = states_lost(election2016)
    total_lost16 = sum(state.get_ecvotes() for state in lost_states16)
    ec_votes_needed16 = ec_votes_reqd(election2016)
    move_max16 = dp_move_max_voters(lost_states16, total_lost16-ec_votes_needed16)
    print("YOOO",[state.get_name() for state in move_max16])'''

    # # tests Problem 5: dp_move_max_voters
    print("dp_move_max_voters")
    total_lost = sum(state.get_ecvotes() for state in lost_states)
    move_max = dp_move_max_voters(lost_states, total_lost-ec_votes_needed)
    max_states_names = [state.get_name() for state in move_max]
    max_voters_displaced = sum([state.get_margin()+1 for state in move_max])
    max_ec_votes = sum([state.get_ecvotes() for state in move_max])
    print("States with the largest margins:", max_states_names)
    print("Max voters displaced:", max_voters_displaced, "for a total of", max_ec_votes, "Electoral College votes.", "\n")

    # tests Problem 5: move_min_voters
    print("move_min_voters")
    swing_states = move_min_voters(lost_states, ec_votes_needed)
    swing_state_names = [state.get_name() for state in swing_states]
    min_voters = sum([state.get_margin()+1 for state in swing_states])
    swing_ec_votes = sum([state.get_ecvotes() for state in swing_states])
    print("Complementary knapsack swing states results:", swing_state_names)
    print("Min voters displaced:", min_voters, "for a total of", swing_ec_votes, "Electoral College votes. \n")
