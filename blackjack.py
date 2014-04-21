##!/usr/bin/env python2.7
"""blackjack module: see blackjack.Blackjack.__doc__"""


from random import randrange
from sys import version_info


def prompt(question, accept):
    """prompt: prompt until acceptable answer receieved"""
    answer = ""
    while True:
        # if python2, use raw_input()
        if version_info < (3,0):
            answer = raw_input(question)
        else:
            answer = input(question)
        if len(answer) == 1 and answer in accept:
            break
    return answer


class Blackjack(object):
    """
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    Welcome to PyCasino!
    
    Game: Blackjack (PyJack)

    Table Rules:
     - Dealer hits until hand value is 17 or greater
     - Dealer does not hit a soft 17, e.g., Ace + Six
     - Minimum bet = 1
     - A player-Blackjack wins 3/2 of bet (rounded down)
     - Deck is shuffled every round
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    """
    def __init__(self, n_decks = 1):
        """initialize Blackjack attributes"""
        self.n_decks = n_decks
        self.bet = 1
        self.bank = 100
        self.net_wins = 0
        self.net_loss = 0
        self.player = self.Hand()
        self.dealer = self.Hand()
        self.deck = self.Deck(self.n_decks)


    class Deck(object):
        """
        Deck(n_decks = 1):
        - subclass of Blackjack
        - creates and stores a deck of Card objects
        """
        def __init__(self, n_decks = 1):
            """initialize Deck attributes"""
            self.n_decks = n_decks
            self.stack = self.freshdeck()

        class Card(object):
            """
            Card:
            - subclass of Deck
            - contains card information
            Functionality:
            - when Card objects are added (+ operator), their values are added
            - when Card objects are summed in a list, their values are added
            """
            def __init__(self, suit, unichar, face, value):
                """initialize Card attributes"""
                self.suit_str = suit
                self.suit_unichr = unichar
                self.face = face
                self.value = value

            def __add__(self, other):
                """Card addition using + operator"""
                return self.value + other.value

            def __radd__(self, other):
                """Card addition using sum"""
                return self.value + other

            def __unicode__(self):
                """unicode support for Card"""
                return u"[{self.suit_unichr} {self.face}]".format(self=self)

            def __str__(self):
                """print(Card)"""
                if version_info < (3,0):
                    return unicode(self).encode("utf-8")
                else:
                    return self.__unicode__()

        def freshdeck(self):
            """assemble and return list of 52*N Card objects"""
            suits_str = ["Heart", "Diamond", "Spade", "Club"]
            suits_unichr = [u"\u2665", u"\u2666", u"\u2664", u"\u2667"]
            cards = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", \
                     "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
            values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
            # zip card attributes into list of 52 tuples
            # note: result is not a random stack of cards
            tupledeck = zip(suits_str*13, suits_unichr*13, cards*4, values*4)
            # populate list with 52*N Card objects
            stack = [self.Card(suit, unichar, face, value) for suit, unichar, face, value in tupledeck]*self.n_decks 
            return stack

        def draw(self):
            """random draw without replacement"""
            # note: when considering to add multiplayer functionality, be sure to not allow
            #       deck to empty, otherwise a ValueError is thrown by pop
            return self.stack.pop(randrange(len(self.stack)))


    class Hand(object):
        """
        Hand:
        - subclass of Blackjack
        - handles Ace value rules
        Print Functionality:
        - print(Hand()) sends string comprised of unicode card representations to stdout
        """
        def __init__(self):
            """initialize Hand attribute"""
            self.hand = []

        def total(self):
            """sum total of Card object values"""
            return sum(self.hand)

        def hit(self, deck):
            """hit(deck):
            - draw without replacement from Blackjack.Deck object
            - drawn Aces act as 11 if prior hand total < or = 10
            """
            self.hand.append(deck.draw())
            # set value of Ace to 11 if hand total <= 10
            if self.hand[-1].face == "Ace":
                if sum(self.hand[0:-1]) <= 10:
                    self.hand[-1].value = 11
                #print "You've got an Ace up your sleeve"
            # change an 11 value back to 1 if hand total > 21
            values = [card.value for card in self.hand]
            if 11 in values and sum(self.hand) > 21:
                for card in self.hand:
                    if card.value == 11:
                        card.value = 1

        def __unicode__(self):
            """unicode support for Card objects within Hand"""
            handstr = u""
            for card in self.hand:
                handstr = handstr + card.__unicode__()
            return handstr

        def __str__(self):
            """print(Hand)"""
            if version_info < (3,0):
                return unicode(self).encode("utf-8")
            else:
                return self.__unicode__()


    def init_deal(self):
        """initial deal"""
        for ii in range(2):
            self.player.hit(self.deck)
            self.dealer.hit(self.deck)

    def new_hand(self):
        """re-initialize attributes for new round, new hand"""
        self.player = self.Hand()
        self.dealer = self.Hand()
        self.deck = self.Deck(self.n_decks)

    def show(self, dealer_hide = False):
        """display dealer, player hands and hand totals"""
        # dealer hand
        if dealer_hide:
            print(u"   Dealer hand: {}[...] ({})".format(self.dealer.hand[0], self.dealer.hand[0].value))
        else:
            print(u"   Dealer hand: {} {}".format(self.dealer, self.dealer.total()))
        # player hand
        print(u"   Player hand: {} {}".format(self.player, self.player.total()))

    def rulecheck(self):
        """return True if either player busts, player-blackjack, or mutual-blackjack; otherwise False"""
        playertot = self.player.total()
        dealertot = self.dealer.total()
        if playertot > 21:
            print("Player busts")
            self.lose()
            return True
        elif dealertot > 21:
            print("Dealer busts")
            self.win()
            return True
        elif (dealertot + playertot) == 42 and (len(self.player.hand) + len(self.dealer.hand)) == 4:
            print("Dealer reveal...")
            self.show()
            print("Mutual Blackjack.\nPush")
            return True
        elif playertot == 21 and len(self.player.hand) == 2:
            print("Dealer reveal...")
            self.show()
            print("Blackjack!\nPlayer wins")
            self.win(BJ = True)
            return True
        return False

    def wincheck(self):
        """determine win/lose"""
        playertot = self.player.total()
        dealertot = self.dealer.total()
        if playertot > dealertot:
            print("Player wins")
            self.win()
        elif playertot < dealertot:
            print("Dealer wins")
            self.lose()
        elif playertot == dealertot:
            print("Push")

    def win(self, BJ = False):
        """player wins, update bank"""
        if BJ:
            new = self.bank + self.bet*3//2
            print("Bank + {} = {}".format(self.bet*3//2, new))
            self.bank = new
            self.net_wins += self.bet*3//2
        else:
            new = self.bank + self.bet
            print("Bank + {} = {}".format(self.bet, new))
            self.bank = new
            self.net_wins += self.bet

    def lose(self):
        """player loses, update bank"""
        new = self.bank - self.bet
        print("Bank - {} = {}".format(self.bet, new))
        self.bank = new
        self.net_loss -= self.bet

    def place_bet(self):
        """place integer bet in range: [1, self.bank]"""
        print("Bank = {self.bank}".format(self=self))
        while True:
            # if python2, use raw_input()
            if version_info < (3,0):
                new_bet = raw_input("Enter bet ({self.bet}): ".format(self=self))
            else:
                new_bet = input("Enter bet ({self.bet}): ".format(self=self))
            if new_bet:
                try:
                    new_bet = int(new_bet)
                except ValueError:
                    print("   invalid input type")
                    continue
                if new_bet > self.bank:
                    print("   bet cannot be larger than bank")
                elif new_bet < 1:
                    print("   bet cannot be less than 1")
                else:
                    self.bet = new_bet
                    break
            else:
                # keep old bet
                if self.bet > self.bank:
                    print("   bet cannot be larger than bank")
                else:
                    break
        print("Bet = {}".format(self.bet))
