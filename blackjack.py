from cards import *
from hands import *

DIVIDER_SIZE = 30
WIN = "Win"
LOSE = "Lose"
PUSH = "Push"
BLACKJACK = "Blackjack"

class BlackjackGame:
    def __init__(self, bj_player, initial_chips, verbose=False):
        self.bj_player = bj_player
        self.verbose = verbose
        self.chips = initial_chips
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0

    def play(self, bet):
        if self.chips - bet < 0:
            print("You don't have enough chips!")
            return

        # Initialize the deck
        self.deck = Deck(standard=True)

        # Initialize player and dealer hands
        self.player_hands = [PlayerHand(self, bet, self.verbose)]
        self.dealer = DealerHand(self, self.verbose)

        # Deal hands
        for _ in range(2):
            self.player_hands[0].deal_card()
            self.dealer.deal_card()

        print()
        print("-" * DIVIDER_SIZE)

        ## Player Turn ##
        print()
        self.bj_player.play(self, self.player_hands[0])

        ## Dealer Turn ##
        print()
        self.dealer.play_dealer()

        ## Game results ##
        dealer_total = self.dealer.get_total().get_value()
        winnings = 0
        results = []

        for i in range(len(self.player_hands)):
            hand = self.player_hands[i]
            player_total = hand.get_total().get_value()
            win_amount = 0
            result = "Error"

            print()

            if len(self.player_hands) > 1:
                print(f"Hand #{i + 1}: ", end="")

            # check for blackjack
            if (hand.is_blackjack() and player_total != dealer_total):
                result = BLACKJACK
                win_amount = int(hand.bet * 1.5)

            # didn't bust and player had higher total -> win
            elif (self.dealer.busted() and not hand.busted()) or (not hand.busted() and player_total > dealer_total):
                result = WIN
                win_amount = hand.bet

            # player total == dealer total and didn't bust -> push
            elif not hand.busted() and player_total == dealer_total:
                result = PUSH

            # busted or dealer had higher -> lose
            elif hand.busted() or dealer_total > player_total:
                result = LOSE
                win_amount = -hand.bet

            print(result + ", ", end = "")

            if win_amount >= 0:
                print("+" + str(win_amount))
            else:
                print(str(win_amount))
            
            results.append(result)
            winnings += win_amount

        print()
        print("-" * DIVIDER_SIZE)

        self.chips += winnings
        return results