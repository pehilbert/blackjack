from cards import *
from hands import *

class BlackjackGame:
    def __init__(self, initial_bet, verbose=False):
        self.verbose = verbose

        # Initialize the deck
        self.deck = Deck(standard=True)

        # Initialize player and dealer hands
        self.player_hands = [PlayerHand(self.deck, initial_bet, verbose)]
        self.dealer = DealerHand(self.deck, verbose)

        # Deal hands
        for _ in range(2):
            self.player_hands[0].deal_card()
            self.dealer.deal_card()

        self.player_hands[0].playing = True

        if self.verbose:
            print("\n==================")
            print("    Start game    ")
            print("==================\n")

    def play(self):
        ## Player Turn ##
        i = 0

        while i < len(self.player_hands):
            hand = self.player_hands[i]
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
                    hand.double_down()
                elif next_action.upper() == "SPLIT" and hand.can_split():
                    new_hands = hand.split()
                    new_hands[0].playing = True
                    new_hands[1].playing = True

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

        for i in range(len(self.player_hands)):
            hand = self.player_hands[i]
            player_total = hand.get_total().get_value()

            if len(self.player_hands) > 1:
                print(f"Hand #{i + 1}: ", end="")

            # didn't bust and player had higher total -> win
            if (self.dealer.busted() and not hand.busted()) or (not hand.busted() and player_total > dealer_total):
                print("Win")

            # player total == dealer total and didn't bust -> push
            elif not hand.busted() and player_total == dealer_total:
                print("Push")

            # busted or dealer had higher -> lose
            elif hand.busted() or dealer_total > player_total:
                print("Lose")

            else:
                print("Something went wrong")
