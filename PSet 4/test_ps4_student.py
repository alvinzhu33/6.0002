import unittest
import numpy
from ps4_classes import *
from blackjack import *


class MockCardDecks(CardDecks):
    """
    Mock representation of CardDecks class used for testing.

    Allows tester to specify which cards to deal.
    """

    def __init__(self, num_decks, card_type, cards_to_deal):
        CardDecks.__init__(self, num_decks, card_type)
        self.cards_to_deal = cards_to_deal

    def deal_card(self):
        return self.cards_to_deal.pop()

    def num_cards_left(self):
        return len(self.cards_to_deal)


def is_within_epsilon(true_value, estimated_value, epsilon):
    return abs(true_value - estimated_value) <= epsilon


def check_within_epsilon(true_values, estimated_values, epsilon):
    """
    Returns True if and only if each value in true_values is within epsilon
    of the corresponding value in estimated_values.
    """
    for i in range(len(true_values)):
        if not is_within_epsilon(true_values[i], estimated_values[i], epsilon):
            return False
    return True


def get_printable_cards(cards):
    """
    Return list of string representations of each card in cards.
    """
    return [str(card) for card in cards]


best_val_error_message = "Your best_val returned %s for cards %s, but it should return %s."
mimic_error_message = "Your mimic_dealer_strategy returned %s when player has %s and dealer has %s, but it should return %s."
peek_error_message = "Your peek_strategy returned %s when player has %s and dealer has %s, but it should return %s."
simple_error_message = "Your simple_strategy returned %s when player has %s and dealer has %s, but it should return %s."


class TestPS4(unittest.TestCase):
    #######################
    # BlackJackHand Tests #
    #######################

    def test_best_val_no_aces_1(self):
        # no cards
        cards = []
        self.assertEqual(BlackJackHand.best_val(cards), 0, best_val_error_message % (
            BlackJackHand.best_val(cards), get_printable_cards(cards), 0))

    def test_best_val_no_aces_2(self):
        # less than 21
        cards = [BlackJackCard('2', 'C'), BlackJackCard(
            '3', 'C'), BlackJackCard('K', 'H')]
        self.assertEqual(BlackJackHand.best_val(cards), 15, best_val_error_message % (
            BlackJackHand.best_val(cards), get_printable_cards(cards), 15))

    def test_best_val_one_ace_1(self):
        # less than 21, A with value 11
        cards = [BlackJackCard('2', 'C'), BlackJackCard(
            'A', 'C'), BlackJackCard('7', 'H')]
        self.assertEqual(BlackJackHand.best_val(cards), 20, best_val_error_message % (
            BlackJackHand.best_val(cards), get_printable_cards(cards), 20))

    def test_best_val_one_ace_2(self):
        # less than 21, A with value 1
        cards = [BlackJackCard('2', 'C'), BlackJackCard(
            'A', 'C'), BlackJackCard('K', 'S')]
        self.assertEqual(BlackJackHand.best_val(cards), 13, best_val_error_message % (
            BlackJackHand.best_val(cards), get_printable_cards(cards), 13))

    def test_best_val_multiple_aces_1(self):
        # one A with value 1, one A with value 11
        cards = [BlackJackCard('2', 'C'), BlackJackCard(
            'A', 'C'), BlackJackCard('A', 'H')]
        self.assertEqual(BlackJackHand.best_val(cards), 14, best_val_error_message % (
            BlackJackHand.best_val(cards), get_printable_cards(cards), 14))

    def test_best_val_multiple_aces_2(self):
        # two A with value 1
        cards = [BlackJackCard('2', 'C'), BlackJackCard('A', 'C'), BlackJackCard(
            'A', 'S'), BlackJackCard('8', 'H'), BlackJackCard('K', 'H')]
        self.assertEqual(BlackJackHand.best_val(cards), 22, best_val_error_message % (
            BlackJackHand.best_val(cards), get_printable_cards(cards), 22))

    def test_mimic_dealer_strategy_1(self):
        # less than 17, hit
        player_cards = [BlackJackCard('5', 'C'), BlackJackCard('K', 'C')]
        dealer_cards = [BlackJackCard('6', 'C'), BlackJackCard('3', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.mimic_dealer_strategy(), BlackJackHand.hit, mimic_error_message % (
            hand.mimic_dealer_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.hit))

    def test_mimic_dealer_strategy_2(self):
        # 17, stand
        player_cards = [BlackJackCard('7', 'C'), BlackJackCard('K', 'C')]
        dealer_cards = [BlackJackCard('6', 'C'), BlackJackCard('3', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.mimic_dealer_strategy(), BlackJackHand.stand, mimic_error_message % (
            hand.mimic_dealer_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.stand))

    def test_peek_strategy_1(self):
        # player < dealer, hit
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('K', 'C')]
        dealer_cards = [BlackJackCard('K', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.peek_strategy(), BlackJackHand.hit, peek_error_message % (
            hand.peek_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.hit))

    def test_peek_strategy_2(self):
        # player == dealer, stand
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('A', 'C')]
        dealer_cards = [BlackJackCard('K', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.peek_strategy(), BlackJackHand.stand, peek_error_message % (
            hand.peek_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.stand))

    def test_peek_strategy_3(self):
        # player > dealer, stand
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('A', 'C')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.peek_strategy(), BlackJackHand.stand, peek_error_message % (
            hand.peek_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.stand))

    def test_simple_strategy_1(self):
        # player > 17
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('A', 'C')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.simple_strategy(), BlackJackHand.stand, simple_error_message % (
            hand.simple_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.stand))

    def test_simple_strategy_2(self):
        # player == 17
        player_cards = [BlackJackCard('7', 'C'), BlackJackCard('A', 'C')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.simple_strategy(), BlackJackHand.stand, simple_error_message % (
            hand.simple_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.stand))

    def test_play_player_1(self):
        # player busts
        player_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        dealer_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        cards_to_deal = [BlackJackCard('K', 'S'), BlackJackCard(
            'K', 'S'), *dealer_hand, *player_hand]

        def strategy(hand):
            while hand.deck.num_cards_left() > 0:
                return BlackJackHand.hit

        deck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(deck)
        self.assertRaises(Busted, hand.play_player, strategy)

    def test_play_player_2(self):
        # player does not bust
        player_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        dealer_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        cards_to_deal = [BlackJackCard('3', 'S'), BlackJackCard(
            '3', 'S'), *dealer_hand, *player_hand]

        def strategy(hand):
            while hand.deck.num_cards_left() > 0:
                return BlackJackHand.hit

        deck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(deck)
        try:
            hand.play_player(strategy)
        except:
            self.fail('Your play_player busted when it should not have.')

    def test_play_dealer_1(self):
        # dealer busts
        player_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        dealer_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        cards_to_deal = [BlackJackCard('K', 'S'), BlackJackCard(
            'K', 'S'), *dealer_hand, *player_hand]

        deck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(deck)
        self.assertRaises(Busted, hand.play_dealer)

    def test_play_dealer_2(self):
        # dealer does not bust
        player_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        dealer_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        cards_to_deal = [BlackJackCard('3', 'S'), BlackJackCard(
            'K', 'S'), *dealer_hand, *player_hand]

        deck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(deck)
        try:
            hand.play_dealer()
        except:
            self.fail('Your play_dealer busted when it should not have.')

    ###################
    # play_hand Tests #
    ###################

    def test_play_hand_mimic_1(self):
        random.seed(3)
        correct_return = 0
        deck = CardDecks(1, BlackJackCard)
        player_return = play_hand(deck, BlackJackHand.mimic_dealer_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with mimic_dealer strategy.')

    def test_play_hand_mimic_2(self):
        random.seed(5)
        correct_return = 2
        deck = CardDecks(8, BlackJackCard)
        player_return = play_hand(deck, BlackJackHand.mimic_dealer_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with mimic_dealer strategy.')

    def test_play_hand_peek_1(self):
        random.seed(3)
        correct_return = 0
        deck = CardDecks(1, BlackJackCard)
        player_return = play_hand(deck, BlackJackHand.peek_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with peek strategy.')

    def test_play_hand_peek_2(self):
        random.seed(5)
        correct_return = 2.0
        deck = CardDecks(8, BlackJackCard)
        player_return = play_hand(deck, BlackJackHand.peek_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with simple strategy.')

    def test_play_hand_simple_1(self):
        random.seed(3)
        correct_return = 0
        deck = CardDecks(1, BlackJackCard)
        player_return = play_hand(deck, BlackJackHand.simple_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with simple strategy.')

    def test_play_hand_simple_2(self):
        random.seed(5)
        correct_return = 2.0
        deck = CardDecks(8, BlackJackCard)
        player_return = play_hand(deck, BlackJackHand.simple_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with simple strategy.')

    ########################
    # run_simulation Tests #
    ########################

    def test_run_simulation_mimic(self):
        random.seed(0)
        returns, mean, std = run_simulation(
            BlackJackHand.mimic_dealer_strategy, 2, 8, 20, 4000, False)
        correct_mean = -6.044375
        correct_std = 22.19167002186575

        self.assertTrue(is_within_epsilon(np.mean(returns), correct_mean, 0.0001),
                        'Returns of mimic simulation are not within epsilon of correct return values.')
        self.assertTrue(is_within_epsilon(np.std(returns), correct_std, 0.0001),
                        'Returns of mimic simulation are not within epsilon of correct return values.')
        self.assertTrue(
            is_within_epsilon(correct_mean, mean, 0.0001),
            'Mean of mimic simulation %s is not within epsilon of correct value %s.' % (mean, correct_mean))
        self.assertTrue(
            is_within_epsilon(correct_std, std, 0.0001),
            'STD of mimic simulation %s is not within epsilon of correct value %s.' % (std, correct_std))

    def test_run_simulation_peek(self):
        random.seed(0)
        returns, mean, std = run_simulation(
            BlackJackHand.peek_strategy, 2, 8, 20, 4000, False)
        correct_mean = -0.1825
        correct_std = 21.89051892372586

        self.assertTrue(is_within_epsilon(np.mean(returns), correct_mean, 0.0001),
                        'Returns of peek simulation are not within epsilon of correct return values.')
        self.assertTrue(is_within_epsilon(np.std(returns), correct_std, 0.0001),
                        'Returns of peek simulation are not within epsilon of correct return values.')
        self.assertTrue(
            is_within_epsilon(correct_mean, mean, 0.0001),
            'Mean of peek simulation %s is not within epsilon of correct value %s.' % (mean, correct_mean))
        self.assertTrue(
            is_within_epsilon(correct_std, std, 0.0001),
            'STD of peek simulation %s is not within epsilon of correct value %s.' % (std, correct_std))

    def test_run_simulation_simple(self):
        random.seed(0)
        returns, mean, std = run_simulation(
            BlackJackHand.simple_strategy, 2, 8, 20, 4000, show_plot=False)
        correct_mean = -3.3925
        correct_std = 21.8872895478

        self.assertTrue(is_within_epsilon(np.mean(returns), correct_mean, 0.0001),
                        'Returns of simple simulation are not within epsilon of correct return values.')
        self.assertTrue(is_within_epsilon(np.std(returns), correct_std, 0.0001),
                        'Returns of simple simulation are not within epsilon of correct return values.')
        self.assertTrue(
            is_within_epsilon(correct_mean, mean, 0.0001),
            'Mean of simple simulation %s is not within epsilon of correct value %s.' % (mean, correct_mean))
        self.assertTrue(
            is_within_epsilon(correct_std, std, 0.0001),
            'STD of simple simulation %s is not within epsilon of correct value %s.' % (std, correct_std))


# Dictionary mapping function names from the above TestCase class to
# the point value each test is worth.
point_values = {
    'test_best_val_no_aces_1': 0.10,
    'test_best_val_no_aces_2': 0.10,
    'test_best_val_one_ace_1': 0.10,
    'test_best_val_one_ace_2': 0.10,
    'test_best_val_multiple_aces_1': 0.10,
    'test_best_val_multiple_aces_2': 0.20,
    'test_mimic_dealer_strategy_1': 0.30,
    'test_mimic_dealer_strategy_2': 0.30,
    'test_peek_strategy_1': 0.30,
    'test_peek_strategy_2': 0.30,
    'test_peek_strategy_3': 0.30,
    'test_simple_strategy_1':0.30,
    'test_simple_strategy_2':0.30,
    'test_play_player_1': 0.40,
    'test_play_player_2': 0.40,
    'test_play_dealer_1': 0.40,
    'test_play_dealer_2': 0.40,
    'test_play_hand_mimic_1': 0.40,
    'test_play_hand_mimic_2': 0.40,
    'test_play_hand_peek_1': 0.40,
    'test_play_hand_peek_2': 0.40,
    'test_play_hand_simple_1': 0.40,
    'test_play_hand_simple_2': 0.40,
    'test_run_simulation_mimic': 0.40,
    'test_run_simulation_peek': 0.40,
    'test_run_simulation_simple': 0.40,
}


# Subclass to track a point score and appropriate
# grade comment for a suit of unit tests
class Results_600(unittest.TextTestResult):

    # We override the init method so that the Result object
    # can store the score and appropriate test output.
    def __init__(self, *args, **kwargs):
        super(Results_600, self).__init__(*args, **kwargs)
        self.output = []
        self.points = 8

    def addFailure(self, test, err):
        test_name = test._testMethodName
        msg = str(err[1])
        self.handleDeduction(test_name, msg)
        super(Results_600, self).addFailure(test, err)

    def addError(self, test, err):
        test_name = test._testMethodName
        self.handleDeduction(test_name, None)
        super(Results_600, self).addError(test, err)

    def handleDeduction(self, test_name, message):
        point_value = point_values[test_name]
        if message is None:
            message = 'Your code produced an error on test %s.' % test_name
        self.output.append('[-%s]: %s' % (point_value, message))
        self.points -= point_value

    def getOutput(self):
        if len(self.output) == 0:
            return "All correct!"
        return '\n'.join(self.output)

    def getPoints(self):
        return self.points


if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS4))
    result = unittest.TextTestRunner(
        verbosity=2, resultclass=Results_600).run(suite)

    output = result.getOutput()
    points = result.getPoints()

    # weird bug with rounding
    if points < .1:
        points = 0

    print("\nProblem Set 4 Unit Test Results:")
    print(output)
    print("Points: %s/8\n" % points)
