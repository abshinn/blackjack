#!/usr/bin/env python2.7
"""docstring"""

from random import randrange
from time import sleep

class Blackjack(object):
    """Game object"""

    def __init__(self, n_decks = 1):
        """Blackjack __init__"""
        self.n_decks = n_decks
        self.bet = 1
        self.bank = 100
        self.player = self.Hand()
        self.dealer = self.Hand()
        self.deck = self.Deck(self.n_decks)

    class Deck(object):
        """Deck object"""
        def __init__(self, n_decks = 1):
            self.n_decks = n_decks
            self.stack = self.freshdeck()
            print "Deck init... Number of decks: {}".format(n_decks)
        class Card(object):
            """Card: combines card attributes into one object, allows for adding together"""
            def __init__(self, suit, unichar, face, value):
                self.suit_str = suit
                self.suit_unichr = unichar
                self.face = face
                self.value = value
            def __add__(self, other):
                return self.value + other.value
            def __radd__(self, other):
                return self.value + other
            def __unicode__(self):
                return u"[{self.suit_unichr} {self.face}]".format(self=self)
            def __str__(self):
                return unicode(self).encode("utf-8")
        def draw(self):
            # pick without replacement
            try:
                card = self.stack.pop(randrange(len(self.stack)))
            except ValueError:
                print "End of deck! Shuffling..."
                sleep(1)
                self.stack = self.freshdeck()
                card = self.stack.pop(randrange(len(self.stack)))
            return card
        def freshdeck(self):
            suits_str = ["Heart", "Diamond", "Spade", "Club"]
            suits_unichr = [unichr(9829), unichr(9830), unichr(9828), unichr(9831)]
            cards = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", \
                     "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
            values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
            tupledeck = zip(suits_str*13, suits_unichr*13, cards*4, values*4)
            # populate list with 52 Card objects
            stack = [self.Card(suit, unichar, face, value) for suit, unichar, face, value in tupledeck]*self.n_decks 
            return stack
        def __str__(self):
            return "Remaining cards: {}".format(len(self.stack))

    class Hand(object):
        """Hand object"""
        def __init__(self):
            self.hand = []
        def total(self):
            return sum(self.hand)
        def hit(self, deck):
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
            handstr = u""
            for card in self.hand:
                handstr = handstr + card.__unicode__()
            return handstr
        def __str__(self):
            return unicode(self).encode("utf-8")


    def init_deal(self):
        for ii in range(2):
            self.player.hit(self.deck)
            self.dealer.hit(self.deck)

    def new_hand(self):
        self.player = self.Hand()
        self.dealer = self.Hand()
        self.deck = self.Deck(self.n_decks)

    def show(self, dealer_hide = False):
        if dealer_hide:
            print u"   Dealer hand: {}[...] {}".format(self.dealer.hand[0], self.dealer.hand[0].value)
        else:
            print u"   Dealer hand: {} {}".format(self.dealer, self.dealer.total())
        print u"   Player hand: {} {}".format(self.player, self.player.total())

    def bustcheck(self):
        """return True if either player win or bust"""
        playertot = self.player.total()
        dealertot = self.dealer.total()
        if playertot > 21:
            print "Player busts"
            self.lose()
            return True
        elif dealertot > 21:
            print "Dealer busts"
            self.win()
            return True
        elif dealertot + playertot == 42:
            print "Mutual Blackjack.\nPush"
            return True
        elif playertot == 21 and len(self.player.hand) == 2:
            print "Blackjack!\nPlayer wins"
            self.win()
            return True
        #elif dealertot == 21 and len(self.dealer.hand) == 2:
        #    print "Blackjack!\nDealer wins"
        #    self.show()
        #    self.lose()
        #    return True
        return False

    def wincheck(self):
        """check win"""
        playertot = self.player.total()
        dealertot = self.dealer.total()
        if playertot > dealertot:
            print "Player wins"
            self.win()
        elif playertot < dealertot:
            print "Dealer wins"
            self.lose()
        elif playertot == dealertot:
            print "Push"

    def win(self):
        """player wins"""
        new = self.bank + self.bet
        print "Bank + {} = {}".format(self.bet, new)
        self.bank = new

    def lose(self):
        """player loses"""
        new = self.bank - self.bet
        print "Bank - {} = {}".format(self.bet, new)
        self.bank = new

    def place_bet(self):
        print "Bank = {self.bank}".format(self=self)
        while True:
            new_bet = raw_input("Enter bet ({self.bet}): ".format(self=self))
            if new_bet:
                try:
                    new_bet = int(new_bet)
                except ValueError:
                    print "   invalid input type"
                    continue
                if new_bet > self.bank:
                    print "   bet cannot be larger than bank"
                elif new_bet < 1:
                    print "   bet cannot be less than 1"
                else:
                    self.bet = new_bet
                    break
            else:
                # keep old bet
                break
        print "Bet = {}".format(self.bet)

def prompt(question, accept):
    answer = ""
    while True:
        answer = raw_input(question)
        if len(answer) == 1 and answer in accept:
            break
    return answer

def play(delayhit = 1.25):
    """Game script"""
    game = Blackjack()
    choice = "d"
    iteration = 1
    while choice == "d" and game.bank > 0:
        choice = prompt("\n[d]eal, [q]uit: ", accept = "dq")
        if choice == "q":
            break
        print "\n - Round {} - ".format(iteration)
        game.new_hand()
        player = game.player
        dealer = game.dealer
        game.place_bet()
        game.init_deal()
        game.show(dealer_hide = True)
        # check if either player has Blackjack
        if game.bustcheck():
            sleep(delayhit)
            continue
        # choice
        choice2 = prompt("[h]it or [s]tay: ", accept = "hs")
        while choice2 == "h":
            print "Player hits..."
            sleep(delayhit - 1)
            player.hit(game.deck)
            game.show(dealer_hide = True)
            if player.total() > 21:
                break 
            choice2 = prompt("[h]it or [s]tay: ", accept = "hs")
        if game.bustcheck():
            continue
        game.show()
        sleep(delayhit)
        while dealer.total() < 17 and dealer.total() <= player.total():
            print "Dealer hits..."
            sleep(delayhit)
            dealer.hit(game.deck)
            game.show()
            if dealer.total() > 21:
                break
        if game.bustcheck():
            continue
        game.wincheck()
        print " - End of Round - "
        iteration += 1

    print "\n - End of Game - "
    if game.bank < 1:
        print "\nOut of chips. The House always wins!\n"
    else:
        print "\nYou leave with {} fake chips. Hooray!\n".format(game.bank)

if __name__ == "__main__":
    play()
