from cards import Card

class Hand:
    def __init__(self, deck, owner, verbose=False):
        self.__cards = []
        self.deck = deck
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

    def busted(self):
        return self.get_total().get_value() > 21

    def stand(self):
        if self.playing:
            self.playing = False

            if self.verbose:
                print(self.owner, "stands")

    def hit(self):
        if self.playing:
            card = self.deck.get_card()
            self.add_card(card)

            if self.verbose:
                print(self.owner, "hits, dealt", card)
                print(self)

                if self.busted():
                    print(self.owner, "busts")

                if self.get_total().get_value() == 21:
                    print(self.owner, "has 21!")

            if self.busted() or self.get_total().get_value() == 21:
                self.playing = False

    def deal_card(self):
        if not self.playing:
            self.add_card(self.deck.get_card())

    def add_card(self, card):
        self.__cards.append(card)

    def get_cards(self):
        return self.__cards

    def __str__(self):
        return self.owner + ": " + " ".join([str(c) for c in self.__cards]) + " (" + str(self.get_total()) + ")"

class PlayerHand(Hand):
    def __init__(self, deck, initial_bet, verbose=False):
        super().__init__(deck, "Player", verbose)
        self.bet = initial_bet

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
            first_hand = PlayerHand(self.deck, self.bet, self.verbose)
            first_hand.add_card(self.get_cards()[0].clone())
            first_hand.deal_card()

            second_hand = PlayerHand(self.deck, self.bet, self.verbose)
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
    def __init__(self, deck, verbose=False):
        super().__init__(deck, "Dealer", verbose)

    def play_dealer(self):
        self.playing = True

        if self.verbose:
            print(self.owner, "flips")
            print(self)

        while self.playing and self.__should_hit():
            self.hit()

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