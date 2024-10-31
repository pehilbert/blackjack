from cards import Card

class Hand:
    def __init__(self, game, owner, verbose=False):
        self.__cards = []
        self.game = game
        self.playing = False
        self.owner = owner
        self.verbose = verbose

    def get_total(self):
        total = 0
        ace = False

        for card in self.__cards:
            total += card.value_number()

            if card.value_number() == 1:
                ace = True

        if ace and total + 10 <= 21:
            return HandTotal(total + 10, total + 10 != 21)

        return HandTotal(total, False)
    
    def is_blackjack(self):
        return self.get_total().get_value() == 21 and len(self.get_cards()) == 2

    def busted(self):
        return self.get_total().get_value() > 21

    def stand(self):
        if self.playing:
            self.playing = False

            if self.verbose:
                print(self.owner, "stands")

    def hit(self):
        if self.playing:
            card = self.game.deck.get_card()
            self.add_card(card)

            if self.verbose:
                print(self.owner, "hits, dealt", card)
                print(self)

                if self.busted():
                    print(self.owner, "busts")
            else:
                print(self)

            if self.busted() or self.get_total().get_value() == 21:
                self.playing = False

    def deal_card(self):
        if not self.playing:
            self.add_card(self.game.deck.get_card())

    def add_card(self, card):
        self.__cards.append(card)

    def get_cards(self):
        return self.__cards

    def __str__(self):
        return self.owner + ": " + " ".join([str(c) for c in self.__cards]) + " (" + str(self.get_total()) + ")"

class PlayerHand(Hand):
    def __init__(self, game, initial_bet, verbose=False):
        super().__init__(game, "Player", verbose)
        self.bet = initial_bet

    def play_player(self, split_num=0):
        self.playing = not self.is_blackjack()

        if split_num > 0:
            print(f"Split hand #{split_num}:")

        print(f"Chips: {self.game.chips}")
        print(f"  Bet: {self.bet}")
        print()
        print(self.game.dealer)
        print(self)

        while self.playing:
            choices = ["STAND", "HIT", "DOUBLE"]

            if self.can_split():
                choices.append("SPLIT")
                
            prompt = "What to do? (" + ", ".join(choices) + ") "

            print()
            next_action = input(prompt).strip()
            
            if next_action.upper() == "STAND":
                self.stand()
            elif next_action.upper() == "HIT":
                self.hit()
            elif next_action.upper() == "DOUBLE":
                if self.game.chips >= self.bet * 2:
                    self.double_down()
                else:
                    print("You do not have enough chips to double down")

            elif next_action.upper() == "SPLIT":
                if self.can_split():
                    new_hands = self.split()

                    for hand_num, hand in enumerate(new_hands):
                        self.game.player_hands.append(hand)

                        print()
                        hand.play_player(split_num=hand_num + 1)

                    self.game.player_hands.remove(self)
                else:
                    print("You cannot split this hand")
            else:
                print("Invalid command, try again")

    def double_down(self):
        if self.playing:
            if self.verbose:
                print(self.owner, "doubles, bet is now", self.bet * 2)

            self.bet *= 2
            self.hit()
            self.playing = False

    def split(self):
        result = []

        if self.can_split():
            first_hand = PlayerHand(self.game, self.bet, self.verbose)
            first_hand.add_card(self.get_cards()[0].clone())
            first_hand.deal_card()

            second_hand = PlayerHand(self.game, self.bet, self.verbose)
            second_hand.add_card(self.get_cards()[1].clone())
            second_hand.deal_card()

            result = [first_hand, second_hand]
            self.playing = False

            if self.verbose:
                print(self.owner, "splits")

        return result
    
    def can_split(self):
        return self.playing and len(self.get_cards()) == 2 and self.get_cards()[0] == self.get_cards()[1]

class DealerHand(Hand):
    def __init__(self, game, verbose=False):
        super().__init__(game, "Dealer", verbose)

    def play_dealer(self):
        self.playing = True

        if self.verbose:
            print(self.owner, "flips")

        print(self)

        while self.playing and self.__should_hit():
            self.hit()

        self.playing = False

    def __should_hit(self):
        return self.get_total().get_value() < 17 or self.get_total().get_soft()
    
    def __str__(self):
        if not self.playing:
            to_join = ["xx"]
            to_join.extend([str(c) for c in self.get_cards()[1:]])
            return self.owner + ": " + " ".join(to_join)
        
        return super().__str__()

class HandTotal:
    def __init__(self, value, soft):
        self.__value = value
        self.__soft = soft

    def get_value(self):
        return self.__value
    
    def get_soft(self):
        return self.__soft
    
    def __str__(self):
        if self.__soft:
            return str(self.__value - 10) + "/" + str(self.__value)
        
        return str(self.__value)