#!/usr/bin/env python2.7
"""docstring"""

from random import randrange

suits_str = ["Heart", "Diamond", "Spade", "Club"]
suits_unichr = [unichr(9829), unichr(9830), unichr(9828), unichr(9831)]
cards = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
freshdeck = zip(suits_str*13, suits_unichr*13, cards*4, values*4)

class deck(object):
    """deck object"""
    def __init__(self):
        self.value = freshdeck
    def pick(self):
        card = self.value.pop(randrange(len(self.value)))
        print u"[{} {}] {} worth {}".format(card[1], card[2], card[0], card[3])
    def shuffle(self):
        pass
    def __str__(self):
        print "{} cards left".format(len(self.value))

if __name__ == "__main__":
    pass
