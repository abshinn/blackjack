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
    def __init__(self, number = 1):
        self.stack = freshdeck*number
    def draw(self):
        card = self.stack.pop(randrange(len(self.stack)))
        return card
    def shuffle(self):
        pass
    def __str__(self):
        return "Remaining cards: {}".format(len(self.stack))

class Player(object):
    """Player object"""
    def __init__(self):
        self.chips = 100
        self.hand = []
    def draw(self, deck):
        card = deck.draw()
        self.hand.append(card)

class Dealer(object):
    """Dealer object"""
    def __init__(self):
        self.hand = []
    def draw(self, deck):
        card = deck.draw()
        self.hand.append(card)

def letsplay():
    deck = Deck(1)
    player = Player()
    dealer = Dealer()
    # ROUND
    # bet (1 minimum, 100 max)
    # deal (player, dealer, player, dealer face down)
    # choices: [h]it, [s]tay
    #...
    # if dealer == 21 dealer win
    # if dealer < 17 dealer.hit
    #...


if __name__ == "__main__":
    letsplay()
