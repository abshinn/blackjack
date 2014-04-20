#!/usr/bin/env python2.7
"""docstring"""

from random import randrange

suits_str = ["Heart", "Diamond", "Spade", "Club"]
suits_unichr = [unichr(9829), unichr(9830), unichr(9828), unichr(9831)]
cards = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
tupledeck = zip(suits_str*13, suits_unichr*13, cards*4, values*4)

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

# populate list with 52 Card objects
freshdeck = [Card(suit, unichar, face, value) for suit, unichar, face, value in tupledeck]

class Deck(object):
    """Deck object"""
    def __init__(self, n_decks = 1):
        self.stack = freshdeck*n_decks
        print "Number of decks: {}".format(n_decks)
    def draw(self):
        card = self.stack.pop(randrange(len(self.stack)))
        return card
    def shuffle(self):
        pass
    def __str__(self):
        return "Remaining cards: {}".format(len(self.stack))

class Hand(object):
    """Hand object"""
    def __init__(self):
        self.handlist = []
    def total(self):
        return sum(self.handlist)
    def hit(self, deck):
        self.handlist.append(deck.draw())
        if self.handlist[-1].face == "Ace":
            print "You've got an Ace up your sleeve"
    def __unicode__(self):
        handstr = u""
        for card in self.handlist:
            handstr = handstr + card.__unicode__()
        return handstr
    def __str__(self):
        return unicode(self).encode("utf-8")

class newGame(object):
    """Game object"""
    def __init__(self):
        self.bet = 1
        self.bank = 10
        self.player = Hand()
        self.dealer = Hand()
        self.deck = Deck(n_decks = 1)

    def init_deal(self):
        for ii in range(2):
            self.player.hit(self.deck)
            self.dealer.hit(self.deck)

    def show(self):
        print u"Dealer hand: {} {}".format(self.dealer, self.dealer.total())
        print u"Player hand: {} {}".format(self.player, self.player.total())

    def checkrules(self):
        """return False if no rule is met, return rule if met"""
        playertot = self.player.total()
        dealertot = self.dealer.total()
        if playertot > 21:
            print "player busts"
            return self.lose
        if dealertot > 21:
            print "dealer busts"
            return self.win

    def win(self):
        """player wins"""
        self.bank = self.bank + self.bet

    def lose(self):
        """player loses"""
        self.bank = self.bank - self.bet

    def place_bet(self):
        print "Bank: {self.bank}".format(self=self)
        answer = True
        while answer:
            try:
                new_bet = input("Enter bet ({self.bet}): ".format(self=self))
            except SyntaxError:
                new_bet = False
            if new_bet:
                if type(new_bet) != int:
                    print "invalid input type"
                elif new_bet > self.bank:
                    print "bet larger than bank"
                else:
                    self.bet = new_bet
                    answer = False
            else:
                answer = False
        print "Bet = {}".format(self.bet)

def play():
    """Game script"""
    choice = raw_input("[n]ew game, [q]uit: ")
    if choice == "n":
        game = newGame()
        # round loop
        while True:
            game.place_bet()
            game.init_deal()
            game.show()
            # check if dealer has blackjack
            check = game.checkrules()
            if check:
                print check
                break
            # choice
            #while choice == "h":
            choice2 = raw_input("[h]it or [s]tay: ")
            if choice2 == "h":
                game.player.hit(game.deck)
                game.show()
            elif choice2 == "s":
                print "stay"
            check = game.checkrules()
            if check: print check
            break
    elif choice == "q":
        print("quit")

if __name__ == "__main__":
    play()
