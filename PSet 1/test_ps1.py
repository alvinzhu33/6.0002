import copy
import unittest
import ps1 as ps1

def check_valid_mapping(election, move_voters_result, real_results):
    # case when student returns None
    if move_voters_result is None:
        return real_results is None

    voter_map, ec_votes, voters_moved = move_voters_result
    orig_states_lost = ps1.states_lost(election)
    orig_winner, orig_loser = ps1.find_winner(election)
    election_copy = election[:]
    
    # check if the numbers line up
    if ec_votes != real_results[1] or voters_moved != real_results[2]:
        print("The number of ec_votes gained or voters_moved isn't quite right")
        return False

    # maps the state to the index in the list allows for easy access
    election_dict = {}
    for state_index in range(len(election)):
        election_dict[election[state_index].get_name()] = state_index 

    # make all of the move's suggested in voter_map 
    for state_from, state_to in voter_map:
        from_index, to_index = election_dict[state_from], election_dict[state_to]
        from_margin, to_margin = election_copy[from_index].get_margin(), election_copy[to_index].get_margin()
        margin_moved = voter_map[(state_from, state_to)]

        # just flipped a state that was already won
        if from_margin-margin_moved < 1:
            print("You lost/tied a State that was already won by the winner.")
            return False
        
        #change the results of the election
        election_copy[from_index].margin = from_margin-margin_moved
        if to_margin - margin_moved < 0:
            election_copy[to_index].margin = abs(to_margin-margin_moved)
            election_copy[to_index].winner = orig_loser
        else:
            election_copy[to_index].margin = to_margin-margin_moved

    # check if after all of the changes are made, the election result has been flipped 
    new_winner, new_loser = ps1.find_winner(election_copy)
    return new_winner == orig_loser


class TestPS1(unittest.TestCase):

    def test_1_state_class(self):
        state_1 = ps1.State("MA", 100000, 20000, 8)
        state_2 = ps1.State("NY", 123456, 7890, 25)
        state_1_dup = ps1.State("MA", 100000, 20000, 8)

        self.assertIsInstance(state_1, ps1.State, "The class did not return an instance of State, but instead an instance of %s." % type(state_1))
        self.assertEqual(state_1.get_name(), "MA", "The get_name() function was not implemented correctly.")
        self.assertEqual(state_1.get_ecvotes(), 8, "The get_ecvotes() function was not implemented correctly.")
        self.assertEqual(state_1.get_margin(), abs(100000-20000), "The get_margin() function was not implemented correctly.")
        self.assertEqual(state_1.get_winner(), "dem", "The get_winner() function was not implemented correctly.")
        self.assertEqual(state_1, state_1_dup, "The __eq__ function was not implemented correctly.")
        self.assertNotEqual(state_1, state_2, "The __eq__ function was not implemented correctly.")

    def test_2_load_election_results(self):
        election = ps1.load_election_results("sample_results.txt")
        real_election = [ps1.State("6.00",1,2,530), ps1.State("6.0001",4,5,3), ps1.State("6.0002",7,8,5)]

        self.assertIsInstance(election, list, "load_election_results did not return a list, but instead returned an instance of %s." % type(election))
        self.assertEqual(len(election), 3, "The list returned by load_election_results does not have the correct number of keys. Expected %s, got %s." % (3, len(election)))
        self.assertTrue(all(isinstance(st, ps1.State) for st in election), "An item in the list returned by load_election_results is not a State instance. The item you returned is: %s" % election)
        self.assertTrue(all(election[i] == real_election[i] for i in range(len(election))), "The list returned by load_election_results does not match the expected list. \nExpected: %s \nGot: %s " % (real_election, election))

    def test_3_find_winner(self):
        gop_won = ("gop", "dem")
        dem_won = ("dem", "gop")
        results_2016 = ps1.find_winner(ps1.load_election_results("2016_results.txt"))
        results_2012 = ps1.find_winner(ps1.load_election_results("2012_results.txt"))
        results_2008 = ps1.find_winner(ps1.load_election_results("2008_results.txt"))

        self.assertEqual(results_2016, gop_won, "The tuple returned by find_winner does not have the correct number of items. Expected %s, got %s." % (2, len(results_2016)))
        self.assertEqual(results_2016, gop_won, "For the 2016 election: expected %s, got %s." % (gop_won, results_2016))
        self.assertEqual(results_2012, dem_won, "For the 2012 election: expected %s, got %s." % (gop_won, results_2012))
        self.assertEqual(results_2008, dem_won, "For the 2008 election: expected %s, got %s." % (gop_won, results_2008))
        
    def test_3_states_lost(self):
        real_sample = set(['6.00', '6.0001', '6.0002'])
        real_2016 = set(['AL', 'AK', 'AZ', 'AR', 'FL', 'GA', 'ID', 'IN', 'IA', 'KS', 'KY', 'LA', 'MI', 'MS', 'MO', 'MT', 'NE', 'NC', 'ND', 'OH', 'OK', 'PA', 'SC', 'SD', 'TN', 'TX', 'UT', 'WV', 'WI', 'WY'])
        real_2012 = set(['CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'HI', 'IL', 'IA', 'ME', 'MD', 'MA', 'MI', 'MN', 'NV', 'NH', 'NJ', 'NM', 'NY', 'OH', 'OR', 'PA', 'RI', 'VT', 'VA', 'WA', 'WI'])
        real_2008 = set(['CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'HI', 'IL', 'IN', 'IA', 'ME', 'MD', 'MA', 'MI', 'MN', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'OH', 'OR', 'PA', 'RI', 'VT', 'VA', 'WA', 'WI'])

        results_sample = [state.get_name() for state in ps1.states_lost(ps1.load_election_results("sample_results.txt"))]
        results_2016 = [state.get_name() for state in ps1.states_lost(ps1.load_election_results("2016_results.txt"))]
        results_2012 = [state.get_name() for state in ps1.states_lost(ps1.load_election_results("2012_results.txt"))]
        results_2008 = [state.get_name() for state in ps1.states_lost(ps1.load_election_results("2008_results.txt"))]

        self.assertEqual(len(results_sample), len(set(results_sample)), "Duplicate states found in list")
        self.assertEqual(len(results_2016), len(set(results_2016)), "Duplicate states found in list")
        self.assertEqual(len(results_2012), len(set(results_2012)), "Duplicate states found in list")
        self.assertEqual(len(results_2008), len(set(results_2008)), "Duplicate states found in list")

        self.assertEqual(real_sample, set(results_sample),  "For the sample election: expected %s, got %s." % (real_sample, results_sample))
        self.assertEqual(real_2016, set(results_2016), "For the 2016 election: expected %s, got %s." % (real_2016, results_2016))
        self.assertEqual(real_2012, set(results_2012), "For the 2012 election: expected %s, got %s." % (real_2012, results_2012))
        self.assertEqual(real_2008, set(results_2008), "For the 2008 election: expected %s, got %s." % (real_2008, results_2008))

    def test_3_ec_votes_reqd(self):
        real_sample = 270
        real_2016 = 37
        real_2012 = 64
        real_2008 = 96
        results_sample = ps1.ec_votes_reqd(ps1.load_election_results("sample_results.txt"))
        results_2016 = ps1.ec_votes_reqd(ps1.load_election_results("2016_results.txt"))
        results_2012 = ps1.ec_votes_reqd(ps1.load_election_results("2012_results.txt"))
        results_2008 = ps1.ec_votes_reqd(ps1.load_election_results("2008_results.txt"))

        self.assertEqual(results_sample, real_sample, "For the sample election: expected %s, got %s." %(real_sample, results_sample) )
        self.assertEqual(results_2016, real_2016, "For the 2016 election: expected %s, got %s." % (real_2016, results_2016))
        self.assertEqual(results_2012, real_2012, "For the 2012 election: expected %s, got %s." % (real_2012, results_2012))
        self.assertEqual(results_2008, real_2008, "For the 2008 election: expected %s, got %s." % (real_2008, results_2008))
   
    def test_4_greedy_election(self):
        real_sample = set(['6.00'])
        real_2016 = set(['MI', 'WI', 'PA'])
        real_2012 = set(['NH', 'NV', 'FL', 'DE', 'NM', 'IA', 'VT', 'ME', 'RI'])
        real_2008 = set(['NC', 'IN', 'NH', 'DE', 'VT', 'NV', 'NM', 'ME', 'RI', 'IA', 'HI', 'CO', 'DC', 'VA', 'FL'])
        lost_sample = ps1.states_lost(ps1.load_election_results("sample_results.txt"))
        lost_2016 = ps1.states_lost(ps1.load_election_results("2016_results.txt"))
        lost_2012 = ps1.states_lost(ps1.load_election_results("2012_results.txt"))
        lost_2008 = ps1.states_lost(ps1.load_election_results("2008_results.txt"))
        votes_sample = ps1.ec_votes_reqd(ps1.load_election_results("sample_results.txt"))
        votes_2016 = ps1.ec_votes_reqd(ps1.load_election_results("2016_results.txt"))
        votes_2012 = ps1.ec_votes_reqd(ps1.load_election_results("2012_results.txt"))
        votes_2008 = ps1.ec_votes_reqd(ps1.load_election_results("2008_results.txt"))
        results_sample = set(state.get_name() for state in ps1.greedy_election(lost_sample,votes_sample))
        results_2016 = set(state.get_name() for state in ps1.greedy_election(lost_2016,votes_2016))
        results_2012 = set(state.get_name() for state in ps1.greedy_election(lost_2012,votes_2012))
        results_2008 = set(state.get_name() for state in ps1.greedy_election(lost_2008,votes_2008))

        self.assertEqual(results_sample, real_sample, "For Sample Results: expected %s, got %s." % (list(real_sample), list(results_sample)))
        self.assertEqual(results_2016, real_2016, "For 2016 Results: expected %s, got %s." % (list(real_2016), list(results_2016)))
        self.assertEqual(results_2012, real_2012, "For 2012 Results: expected %s, got %s." % (list(real_2012), list(results_2012)))
        self.assertEqual(results_2008, real_2008, "For 2008 Results: expected %s, got %s." % (list(real_2008), list(results_2008)))     

    def test_5_dp_move_max_voters(self):
        real_sample = set([])
        real_2016 = set(['NE', 'WV', 'OK', 'KY', 'TN', 'AL', 'AR', 'MO', 'ND', 'IN', 'LA', 'KS', 'WY', 'SD', 'MS', 'UT', 'SC', 'OH', 'TX', 'ID', 'NC', 'MT', 'IA', 'GA', 'FL', 'AZ', 'AK'])
        real_2012 = set(['NY', 'MA', 'MD', 'DC', 'WA', 'HI', 'VT', 'NJ', 'CA', 'IL', 'CT', 'RI', 'OR', 'MI', 'MN', 'WI', 'NM', 'ME', 'PA', 'IA', 'DE', 'NV', 'CO'])
        real_2008 = set(['DC', 'VT', 'IL', 'NY', 'MA', 'MD', 'MI', 'CA', 'CT', 'WI', 'WA', 'HI', 'OR', 'RI', 'NJ', 'PA', 'NM', 'MN', 'DE', 'NV', 'ME', 'CO'])
        lost_sample = ps1.states_lost(ps1.load_election_results("sample_results.txt"))
        lost_2016 = ps1.states_lost(ps1.load_election_results("2016_results.txt"))
        lost_2012 = ps1.states_lost(ps1.load_election_results("2012_results.txt"))
        lost_2008 = ps1.states_lost(ps1.load_election_results("2008_results.txt"))
        votes_reqd_2016 = ps1.ec_votes_reqd(ps1.load_election_results("2016_results.txt"))
        votes_reqd_2012 = ps1.ec_votes_reqd(ps1.load_election_results("2012_results.txt"))
        votes_reqd_2008 = ps1.ec_votes_reqd(ps1.load_election_results("2008_results.txt"))
        lost_votes_2016 = sum(state.get_ecvotes() for state in lost_2016)
        lost_votes_2012 = sum(state.get_ecvotes() for state in lost_2012)
        lost_votes_2008 = sum(state.get_ecvotes() for state in lost_2008)
        results_sample = set(state.get_name() for state in ps1.dp_move_max_voters(lost_sample, 2))            
        results_2016 = set(state.get_name() for state in ps1.dp_move_max_voters(lost_2016,lost_votes_2016-votes_reqd_2016))
        results_2012 = set(state.get_name() for state in ps1.dp_move_max_voters(lost_2012,lost_votes_2012-votes_reqd_2012))
        results_2008 = set(state.get_name() for state in ps1.dp_move_max_voters(lost_2008,lost_votes_2008-votes_reqd_2008))

        self.assertEqual(results_sample, real_sample, "For Sample Results: expected States %s, got %s." % (list(real_sample), list(results_sample)))        
        self.assertEqual(results_2016, real_2016, "For the 2016 election: expected States %s, got %s." % (list(real_2016), list(results_2016)))
        self.assertEqual(results_2012, real_2012, "For the 2012 election: expected States %s, got %s." % (list(real_2012), list(results_2012)))
        self.assertEqual(results_2008, real_2008, "For the 2008 election: expected States %s, got %s." % (list(real_2008), list(results_2008)))     

    def test_5_move_min_voters(self):
        real_sample = set(['6.00'])
        real_2016 = set(['MI', 'PA', 'WI'])
        real_2012 = set(['FL', 'NH', 'OH', 'VA'])
        real_2008 = set(['FL', 'IN', 'IA', 'NH', 'NC', 'OH', 'VA'])
        lost_sample = ps1.states_lost(ps1.load_election_results("sample_results.txt"))
        lost_2016 = ps1.states_lost(ps1.load_election_results("2016_results.txt"))
        lost_2012 = ps1.states_lost(ps1.load_election_results("2012_results.txt"))
        lost_2008 = ps1.states_lost(ps1.load_election_results("2008_results.txt"))
        votes_sample = ps1.ec_votes_reqd(ps1.load_election_results("sample_results.txt"))
        votes_2016 = ps1.ec_votes_reqd(ps1.load_election_results("2016_results.txt"))
        votes_2012 = ps1.ec_votes_reqd(ps1.load_election_results("2012_results.txt"))
        votes_2008 = ps1.ec_votes_reqd(ps1.load_election_results("2008_results.txt"))
        results_sample = set(state.get_name() for state in ps1.move_min_voters(lost_sample, votes_sample))
        results_2016 = set(state.get_name() for state in ps1.move_min_voters(lost_2016,votes_2016))
        results_2012 = set(state.get_name() for state in ps1.move_min_voters(lost_2012,votes_2012))
        results_2008 = set(state.get_name() for state in ps1.move_min_voters(lost_2008,votes_2008))

        self.assertEqual(results_sample, real_sample, "For Sample Results: expected States %s, got %s." % (list(real_sample), list(results_sample)))        
        self.assertEqual(results_2016, real_2016, "For the 2016 election: expected States %s, got %s." % (list(real_2016), list(results_2016)))
        self.assertEqual(results_2012, real_2012, "For the 2012 election: expected States %s, got %s." % (list(real_2012), list(results_2012)))
        self.assertEqual(results_2008, real_2008, "For the 2008 election: expected States %s, got %s." % (list(real_2008), list(results_2008)))     

    def test_6_flip_election(self):
        real_sample = None
        real_2016 = ({('CA', 'MI'): 10705, ('CA', 'PA'): 44293, ('CA', 'WI'): 22749}, 46, 77747)
        real_2012 = ({('TX', 'NH'): 39644, ('TX', 'NV'): 67807, ('TX', 'FL'): 74310, ('TX', 'DE'): 77101, ('TX', 'NM'): 79548, ('TX', 'IA'): 91928, ('TX', 'VT'): 106542, ('TX', 'ME'): 109031, ('TX', 'RI'): 122474}, 64, 768385)
        real_2008 = ({('TX', 'FL'): 236451, ('TX', 'IN'): 28392, ('TX', 'IA'): 146562, ('TX', 'NH'): 68293, ('TX', 'NC'): 14178, ('TX', 'OH'): 262225, ('TX', 'VA'): 194593, ('OK', 'VA'): 39935}, 97, 990629)
        election_sample = ps1.load_election_results("sample_results.txt")
        election_2016 = ps1.load_election_results("2016_results.txt") 
        election_2012 = ps1.load_election_results("2012_results.txt") 
        election_2008 = ps1.load_election_results("2008_results.txt")
        lost_states_sample, ec_needed_sample = ps1.states_lost(election_sample), ps1.ec_votes_reqd(election_sample)
        lost_states_2016, ec_needed_2016 = ps1.states_lost(election_2016), ps1.ec_votes_reqd(election_2016)
        lost_states_2012, ec_needed_2012 = ps1.states_lost(election_2012), ps1.ec_votes_reqd(election_2012)
        lost_states_2008, ec_needed_2008 = ps1.states_lost(election_2008), ps1.ec_votes_reqd(election_2008)
        results_sample_g = ps1.flip_election(election_sample, ps1.move_min_voters(lost_states_sample, ec_needed_sample))
        results_2016_g = ps1.flip_election(election_2016, ps1.greedy_election(lost_states_2016, ec_needed_2016))
        results_2012_g = ps1.flip_election(election_2012, ps1.greedy_election(lost_states_2012, ec_needed_2012))
        results_2008_dp = ps1.flip_election(election_2008, ps1.move_min_voters(lost_states_2008, ec_needed_2008))

        self.assertTrue(check_valid_mapping(election_sample, results_sample_g, real_sample), "Your flip_election results did not give the correct result. For the sample election you got %s, \n one valid solution is %s." % (results_sample_g, real_sample))
        self.assertTrue(check_valid_mapping(election_2016, results_2016_g, real_2016), "Your flip_election results did not give the correct result. For the 2016 election you got %s, \n one valid solution is %s." % (results_2016_g, real_2016))
        self.assertTrue(check_valid_mapping(election_2012, results_2012_g, real_2012), "Your flip_election results did not give the correct result. For the 2012 election you got %s, \n one valid solution is %s." % (results_2012_g, real_2012,))
        self.assertTrue(check_valid_mapping(election_2008, results_2008_dp, real_2008), "Your flip_election results did not give the correct result. For the 2008 election you got %s, \n one valid solution is %s." % (results_2008_dp, real_2008))


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS1))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
