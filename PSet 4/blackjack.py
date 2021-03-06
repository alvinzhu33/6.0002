# Problem Set 4
# Name: Alvin Zhu
# Collaborators:
# Time Spent: 5:30
# Late Days Used: 0

import matplotlib.pyplot as plt
import numpy as np
from ps4_classes import BlackJackCard, CardDecks, Busted


#############
# PROBLEM 1 #
#############
class BlackJackHand:
    """
    A class representing a game of Blackjack.   
    """
    
    hit = 'hit'
    stand = 'stand'

    def __init__(self, deck):
        """
        Parameters:
        deck - An instance of CardDeck that represents the starting shuffled
        card deck (this deck itself contains one or more standard card decks)

        Attributes:
        self.deck - CardDeck, represents the shuffled card deck for this game of BlackJack
        self.player - list, initialized with the first 2 cards dealt to the player
                      and updated as the player is dealt more cards from the deck
        self.dealer - list, initialized with the first 2 cards dealt to the dealer
                      and updated as the dealer is dealt more cards from the deck
                      
        Important: You MUST deal out the first four cards in the following order:
            player, dealer, player, dealer
        """
        self.deck = deck
        self.player = [deck.deal_card()]
        self.dealer = [deck.deal_card()]
        self.player += [deck.deal_card()]
        self.dealer += [deck.deal_card()];

    # You can call the method below like this:
    #   BlackJackHand.best_val(cards)
    @staticmethod
    def best_val(cards):
        """
        Finds the best sum of point values given a list of cards, where the
        "best sum" is defined as the highest point total not exceeding 21.

        Remember that an Ace can have value 1 or 11.
        Hint: If you have one Ace, give it a value of 11 by default. If the sum
        point total exceeds 21, then give it a value of 1. What should you do
        if cards has more than one Ace?

        Parameters:
        cards - a list of BlackJackCard instances.

        Returns:
        int, best sum of point values of the cards  
        """
        #Sums up all the cards
        sums = 0
        aces = 0
        for card in cards:
            sums += card.get_val()
            if card.get_rank() == 'A':
                aces += 1
        
        #Accounting for when sums should bust but there are aces
        while sums > 21 and aces > 0:
            sums -= 10
            aces -= 1
        return sums;


    def get_player_cards(self):
        """
        Returns:
        list, a copy of the player's cards 
        """
        return self.player

    def get_dealer_cards(self):
        """
        Returns:
        list, a copy of the dealer's cards 
        """
        return self.dealer

    def get_dealer_upcard(self):
        """
        Returns the dealer's face up card. We define the dealer's face up card
        as the first card in their hand.

        Returns:
        BlackJackCard instance, the dealer's face-up card 
        """
        return self.get_dealer_cards()[0]

    def set_initial_cards(self, player_cards, dealer_cards):
        """
        Sets the initial cards of the game.
        player_cards - list, containing the inital player cards
        dealer_cards - list, containing the inital dealer cards

        used for testing, DO NOT MODIFY
        """
        self.player = player_cards[:]
        self.dealer = dealer_cards[:]

    # Strategy 1
    def mimic_dealer_strategy(self):
        """
        A playing strategy in which the player uses the same metric as the
        dealer to determine their next move.

        The player will:
            - hit if the best value of their cards is less than 17
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision  
        """
        if self.best_val(self.player) < 17:
            return self.hit
        return self.stand

    # Strategy 2
    def peek_strategy(self):
        """
        A playing strategy in which the player knows the best value of the
        dealer's cards.

        The player will:
            - hit if the best value of their hand is less than that of the dealer's
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision
        """
        if self.best_val(self.player) < self.best_val(self.dealer):
            return self.hit
        return self.stand;

    # Strategy 3
    def simple_strategy(self):
        """
        A playing strategy in which the player will
            - stand if one of the following is true:
                - the best value of player's hand is greater than or equal to 17
                - the best value of player's hand is between 12 and 16 (inclusive)
                  AND the dealer's up card is between 2 and 6 (inclusive)  
            - hit otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision 
        """
        playerVal = self.best_val(self.player)
        dealerUp = self.get_dealer_upcard().get_val()
        if playerVal >= 17 or (playerVal >=12 and playerVal <= 16 and dealerUp >= 2 and dealerUp <= 6):
            return self.stand
        return self.hit;

    def play_player(self, strategy):
        """
        Plays a full round of the player's turn and updates the player's hand
        to include new cards that have been dealt to the player. The player
        will be dealt a new card until they stand or bust.

        Parameter:
        strategy - function, one of the the 3 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy)

        This function does not return anything. Instead, it:
            - Adds a new card to self.player each time the player hits.
            - Raises Busted exception (imported from ps4_classes.py) if the
              best value of the player's hand is greater than 21.
        """
        #Keep adding cards until your strategy tells you to stand
        while strategy(self) == self.hit:
            self.player.append(self.deck.deal_card())

        #Raise Busted error if passed 21
        if self.best_val(self.player) > 21:
            raise Busted

    def play_dealer(self):
        """
        Plays a full round of the dealer's turn and updates the dealer's hand
        to include new cards that have been dealt to the dealer. The dealer
        will get a new card as long as the best value of their hand is less
        than 17, or they bust.

        This function does not return anything. Instead, it:
            - Adds a new card to self.dealer each time the dealer hits.
            - Raises Busted exception (imported from ps4_classes.py) if the
              best value of the dealer's hand is greater than 21.
        """
        #Keep hitting if value less than 17
        while self.best_val(self.dealer) < 17:
            self.dealer.append(self.deck.deal_card())

        #Raise Busted error if passed 21
        if self.best_val(self.dealer) > 21:
            raise Busted
        

    def __str__(self):
        """
        Returns:
        str, representation of the player and dealer and dealer hands.

        Useful for debugging. DO NOT MODIFY. 
        """
        result = 'Player: '
        for c in self.player:
            result += str(c) + ','
        result = result[:-1] + '    '
        result += '\n   Dealer '
        for c in self.dealer:
            result += str(c) + ','
        return result[:-1]

#############
# PROBLEM 2 #
#############


def play_hand(deck, strategy, bet=1.0):
    """
    Plays a hand of Blackjack and determines the amount of money the player
    gets back based on their inital bet.

    The player will get:

        - 2.5 times their original bet if the player's first two cards equal 21,
          and the dealer's first two cards do not equal 21.
        - 2 times their original bet if the player wins after getting more
          cards or the dealer busts.
        - the original amount they bet if the game ends in a tie. If the
          player and dealer both get blackjack from their first two cards, this
          is also a tie.
        - 0 if the dealer wins or the player busts.

    Parameters:

        deck - an instance of CardDeck
        strategy - function, one of the the 3 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy)
        bet - float, the amount that the player bets (default=1.0)

    Returns:

        float, the amount the player gets back
    """
    hand = BlackJackHand(deck)
    playerCards = hand.get_player_cards()
    dealerCards = hand.get_dealer_cards()
    
    #Blackjack check
    playerVal = hand.best_val(playerCards)
    dealerVal = hand.best_val(dealerCards)
    if playerVal == 21 or dealerVal == 21:
        if playerVal == 21:
            if dealerVal == 21:
                return bet
            return bet*2.5
        return 0;
    
    #Player busts or stays
    try:
        hand.play_player(strategy)
    except Busted:
        return 0;

    #Dealer busts or stays
    try:
        hand.play_dealer()
    except Busted:
        return bet*2;
    
    #No one busts so check whose best value is larger
    playerVal = hand.best_val(playerCards)
    dealerVal = hand.best_val(dealerCards)
    if playerVal > dealerVal:
        return bet * 2
    elif playerVal == dealerVal:
        return bet
    else: 
        return 0;


#############
# PROBLEM 3 #
#############


def run_simulation(strategy, bet=2.0, num_decks=8, num_hands=20, num_trials=100, show_plot=False):
    """
    Runs a simulation and generates a box plot reflecting the distribution of
    player's rates of return across all trials.

    The box plot displays the distribution of data based on the five number
    summary: minimum, first quartile, median, third quartile, and maximum.
    We also want to show the average on the box plot. You can do this by
    specifying another parameter: plt.boxplot(results, showmeans=True)

    For each trial:

        - instantiate a new CardDeck with the num_decks and type BlackJackCard
        - for each hand in the trial, call play_hand and keep track of how
          much money the player receives across all the hands in the trial
        - calculate the player's rate of return, which is
            100*(total money received-total money bet)/(total money bet)

    Parameters:

        strategy - function, one of the the 3 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy)
        bet - float, the amount that the player bets each hand. (default=2)
        num_decks - int, the number of standard card decks in the CardDeck. (default=8)
        num_hands - int, the number of hands the player plays in each trial. (default=20)
        num_trials - int, the total number of trials in the simulation. (default=100)
        show_plot - bool, True if the plot should be displayed, False otherwise. (default=False)

    Returns:

        tuple, containing the following 3 elements:
            - list of the player's rate of return for each trial
            - float, the average rate of return across all the trials
            - float, the standard deviation of rates of return across all trials
    """
    returns = []
    totalbet = bet*num_hands
    for trial in range(num_trials):
        #Calculate the gains from every hand of a single trial and record rate of return
        earnHands = 0
        deck = CardDecks(num_decks, BlackJackCard)
        for hand in range(num_hands):
            earnHands += play_hand(deck, strategy, bet)
        returns.append(100.0 * (earnHands-totalbet)/totalbet)
    
    #Calculate mean and standard deviation
    mean = np.mean(returns)
    std = np.std(returns)

    if show_plot:
        plt.boxplot(returns, showmeans=True)
        plt.title("Player ROI on Playing 20 Hands (" + strategy.__name__ + ")\n(mean = " + str(mean) + "%, SD = " + str(std) + "%)")
        plt.ylabel("% Returns")
        plt.xticks([1],[strategy.__name__])
        plt.show()
    
    return (returns, mean, std);


def run_all_simulations(strategies):
    """
    Runs the simulation for each strategy in strategies and generates a single
    graph with one box plot for each strategy. Each box plot should reflect the
    distribution of rates of return for each strategy.

    Make sure to label each plot with the name of the strategy.

    Parameters:

        strategies - list of strategies to simulate
    """
    #Instantiate lists to use for later plotting
    runs = []
    stratTicks = []
    i = 1
    strats = []
    #Run the simulation for each strategy with the default values
    for strategy in strategies:
        runs.append(run_simulation(strategy))
        stratTicks.append(i)
        i += 1
        strats.append(strategy.__name__)
    
    plt.boxplot([runs[0][0], runs[1][0], runs[2][0]], showmeans=True)
    plt.title("Player ROI Using Different Stategies")
    plt.ylabel("% Returns")
    plt.xticks(stratTicks, strats)
    plt.show()

if __name__ == '__main__':
    # uncomment to test each strategy separately
    run_simulation(BlackJackHand.mimic_dealer_strategy, show_plot=True)
    run_simulation(BlackJackHand.peek_strategy, show_plot=True)
    run_simulation(BlackJackHand.simple_strategy, show_plot=True)

    # uncomment to run all simulations
    run_all_simulations([BlackJackHand.mimic_dealer_strategy,
                         BlackJackHand.peek_strategy, BlackJackHand.simple_strategy])
    pass
