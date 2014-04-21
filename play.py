#!/usr/bin/env python2.7
"""executable blackjack play script"""


from blackjack import Blackjack, prompt
from time import sleep


def play(delay = 1.25, n_decks = 1):
    """
    play:
    - gameplay script utilizing Blackjack class and user input
    - delay parameter for added suspense/user-experience
    """
    # initialize game, print documentation
    game = Blackjack(n_decks)
    print(game.__doc__)
    print("Gameplay attributes:\n   {} deck(s)\n   {} sec deal delay".format(n_decks, delay))

    # init deal loop
    choice = "d"
    round_count = 0
    while choice == "d" and game.bank > 0:

        choice = prompt("\n[d]eal, [q]uit: ", accept = "dq")
        if choice == "q":
            break

        round_count += 1
        print("\n - Round {} - ".format(round_count))
        
        # init round, place bet
        game.new_hand()
        player = game.player
        dealer = game.dealer
        game.place_bet()

        # deal, show hands
        game.init_deal()
        game.show(dealer_hide = True)

        # check for player/mutual blackjack
        if game.rulecheck():
            continue

        # initialize player hit loop
        choice2 = prompt("[h]it or [s]tay: ", accept = "hs")
        while choice2 == "h":
            print("Player hits...")
            sleep(delay)
            player.hit(game.deck)
            game.show(dealer_hide = True)
            if player.total() >= 21:
                break 
            choice2 = prompt("[h]it or [s]tay: ", accept = "hs")

        # check for player bust
        if game.rulecheck():
            continue
        
        # reveal dealer's hand 
        print("Dealer reveal...")
        game.show()
        sleep(delay)

        # dealer hit loop
        while dealer.total() < 17 and dealer.total() <= player.total():
            print("Dealer hits...")
            dealer.hit(game.deck)
            game.show()
            sleep(delay)

        # check for dealer bust
        if game.rulecheck():
            continue

        # check for win
        game.wincheck()
        print(" - End of Round - ")

    # out of deal loop, print endgame info
    print("\n - End of Game - ")
    if game.bank < 1:
        print("\nOut of PyChips. The House always wins!\n")
    else:
        print("\nFinal bank = {} PyChips".format(game.bank))
    print("total won = {}\ntotal lost = {}\n".format(game.net_wins, game.net_loss))


if __name__ == "__main__":
    play(n_decks = 1)
