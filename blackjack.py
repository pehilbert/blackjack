from cards import *
from hands import *

class BlackjackGame:
    def __init__(self, initial_chips, verbose=False):
        self.verbose = verbose
        self.chips = initial_chips

    def play(self, bet):
        if self.chips - bet < 0:
            print("You don't have enough chips!")
            return

        # Initialize the deck
        self.deck = Deck(standard=True)

        # Initialize player and dealer hands
        self.player_hands = [PlayerHand(self.deck, bet, self.verbose)]
        self.dealer = DealerHand(self.deck, self.verbose)

        # Deal hands
        for _ in range(2):
            self.player_hands[0].deal_card()
            self.dealer.deal_card()

        self.player_hands[0].playing = True

        if self.verbose:
            print("\n==================")
            print("    Start game    ")
            print("==================\n")

        ## Player Turn ##
        i = 0

        while i < len(self.player_hands):
            hand = self.player_hands[i]
            hand.playing = True
            split = False

            if len(self.player_hands) > 1:
                print(f"\nPlaying hand #{i + 1}:")

            print(self.dealer)
            print(self.player_hands[i])
            print()

            while hand.playing:
                prompt = "What to do? (STAND, HIT, DOUBLE) "

                if hand.can_split():
                    prompt = "What to do? (STAND, HIT, DOUBLE, SPLIT) "

                next_action = input(prompt).strip()
                
                if next_action.upper() == "STAND":
                    hand.stand()
                elif next_action.upper() == "HIT":
                    hand.hit()
                elif next_action.upper() == "DOUBLE":
                    if self.chips >= hand.bet * 2:
                        hand.double_down()
                    else:
                        print("You do not have enough chips to double down")

                elif next_action.upper() == "SPLIT" and hand.can_split():
                    new_hands = hand.split()

                    self.player_hands.pop(i)
                    self.player_hands.insert(i, new_hands[1])
                    self.player_hands.insert(i, new_hands[0])

                    split = True
                else:
                    print("Invalid command, try again")

            if not split:
                i += 1

        ## Dealer Turn ##
        print()
        self.dealer.play_dealer()
        print()

        dealer_total = self.dealer.get_total().get_value()
        winnings = 0

        for i in range(len(self.player_hands)):
            hand = self.player_hands[i]
            player_total = hand.get_total().get_value()
            win_amount = 0

            if len(self.player_hands) > 1:
                print(f"Hand #{i + 1}: ", end="")

            # check for blackjack
            if (hand.is_blackjack()):
                print("Blackjack! ", end="")
                win_amount = int(hand.bet * 1.5)

            # didn't bust and player had higher total -> win
            elif (self.dealer.busted() and not hand.busted()) or (not hand.busted() and player_total > dealer_total):
                print("Win, ", end="")
                win_amount = hand.bet

            # player total == dealer total and didn't bust -> push
            elif not hand.busted() and player_total == dealer_total:
                print("Push, ", end="")

            # busted or dealer had higher -> lose
            elif hand.busted() or dealer_total > player_total:
                print("Lose, ", end="")
                win_amount = -hand.bet

            else:
                print("Something went wrong, ", end="")

            if win_amount >= 0:
                print("+" + str(win_amount))
            else:
                print(str(win_amount))

            winnings += win_amount

        self.chips += winnings