import random

SPADES   = "♠︎"
CLUBS    = "♣︎"
HEARTS   = "♥︎"
DIAMONDS = "♦︎"

class Deck:
    def __init__(self, standard=False):
        self.__cards = []
        self.__index = 0

        if standard:
            for suit in [SPADES, DIAMONDS, CLUBS, HEARTS]:
                for value in range(1, 14):
                    self.__cards.append(Card(suit, value))

        self.shuffle()

    def get_card(self):
        if len(self.__cards) == 0:
            raise ValueError("There must be at least one card in the deck to get a card")
        
        if self.__index < len(self.__cards):
            result = self.__cards[self.__index]
            self.__index += 1
            return result
        
        self.shuffle()
        self.__index = 0
        return self.__cards[self.__index]

    def shuffle(self):
        random.shuffle(self.__cards)
        self.__index = 0

    def __str__(self):
        return " ".join([str(c) for c in self.__cards])

class Card:
    def __init__(self, suit, value):
        self.__suit = suit
        self.__value = value

    def get_suit(self):
        return self.suit

    def value_string(self):
        if self.__value == 1:
            return "A"
        
        if self.__value == 11:
            return "J"
        
        if self.__value == 12:
            return "Q"
        
        if self.__value == 13:
            return "K"
        
        return str(self.value_number())

    def value_number(self):
        return min(self.__value, 10)

    def clone(self):
        return Card(self.__suit, self.__value)

    def __str__(self):
        return self.value_string() + self.__suit

    def __eq__(self, other):
        return self.value_number() == other.value_number()