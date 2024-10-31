import random

class BlackjackPlayer:
    def __init__(self):
        pass

    def play(self):
        pass

class HumanBlackjackPlayer(BlackjackPlayer):
    def __init__(self):
        super().__init__()

    def play(self, game, hand, split_num=0):
        hand.playing = not hand.is_blackjack()

        if split_num > 0:
            print(f"Split hand #{split_num}:")

        print(f"Chips: {game.chips}")
        print(f"  Bet: {hand.bet}")
        print()
        print(game.dealer)
        print(hand)

        while hand.playing:
            choices = ["STAND", "HIT", "DOUBLE"]

            if hand.can_split():
                choices.append("SPLIT")
                
            prompt = "What to do? (" + ", ".join(choices) + ") "

            print()
            next_action = input(prompt).strip()

            if next_action.upper() == "STAND":
                hand.stand()
            elif next_action.upper() == "HIT":
                hand.hit()
            elif next_action.upper() == "DOUBLE":
                if game.chips >= hand.bet * 2:
                    hand.double_down()
                else:
                    print("You do not have enough chips to double down")

            elif next_action.upper() == "SPLIT":
                if hand.can_split():
                    new_hands = hand.split()

                    for hand_num, hand in enumerate(new_hands):
                        game.player_hands.append(hand)

                        print()
                        self.play(game, hand, split_num=hand_num + 1)

                    game.player_hands.remove(self)
                else:
                    print("You cannot split this hand")
            else:
                print("Invalid command, try again")

class AutoBlackjackPlayer(BlackjackPlayer):
    def __init__(self):
        super().__init__()

        # Map tuples (dealer upcard, hand total, soft or not, splittable or not) to maps of choices to scores
        self.decision_scores = {}

        # Keep track of all decisions made in previous game (list of tuples described above, plus the choice made for each)
        self.previous_decisions = None

    def play(self, game, hand, split_num=0):
        if split_num == 0:
            self.previous_decisions = []

        hand.playing = not hand.is_blackjack()

        if split_num > 0:
            print(f"Split hand #{split_num}:")

        print(f"Chips: {game.chips}")
        print(f"  Bet: {hand.bet}")
        print()
        print(game.dealer)
        print(hand)

        while hand.playing:
            choices = ["STAND", "HIT", "DOUBLE"]

            if hand.can_split():
                choices.append("SPLIT")

            print()
            next_action = random.choice(choices)
            self.previous_decisions.append( (game.dealer.get_cards()[1].value_number(), hand.get_total().get_value(), hand.get_total().get_soft(), hand.can_split(), next_action) )
            
            if next_action.upper() == "STAND":
                hand.stand()
            elif next_action.upper() == "HIT":
                hand.hit()
            elif next_action.upper() == "DOUBLE":
                if game.chips >= hand.bet * 2:
                    hand.double_down()
                else:
                    print("You do not have enough chips to double down")

            elif next_action.upper() == "SPLIT":
                if hand.can_split():
                    new_hands = hand.split()

                    for hand_num, hand in enumerate(new_hands):
                        game.player_hands.append(hand)

                        print()
                        self.play(game, hand, split_num=hand_num + 1)

                    if self in game.player_hands:
                        game.player_hands.remove(self)
                else:
                    print("You cannot split this hand")
            else:
                print("Invalid command, try again")

    def increment_decision_scores(self, increment):
        # Update choice scores for each previous decision made
        # (increment score for choice for combination of upcard, hand total, soft or not, splittable or not)
        for decision in self.previous_decisions:
            t = decision[:len(decision) - 1]
            choice = decision[-1]
            
            if not t in self.decision_scores:
                self.decision_scores[t] = {}

            if choice in self.decision_scores[t]:
                self.decision_scores[t][choice] += increment
            else:
                self.decision_scores[t][choice] = increment

class SmartAutoBlackjackPlayer(BlackjackPlayer):
    def __init__(self, decision_scores):
        super().__init__()

        # Learned decision scores
        self.decision_scores = decision_scores

    def play(self, game, hand, split_num=0):
        hand.playing = not hand.is_blackjack()

        if split_num > 0:
            print(f"Split hand #{split_num}:")

        print(f"Chips: {game.chips}")
        print(f"  Bet: {hand.bet}")
        print()
        print(game.dealer)
        print(hand)

        while hand.playing:
            situation = (game.dealer.get_cards()[1].value_number(), hand.get_total().get_value(), hand.get_total().get_soft(), hand.can_split())

            if situation in self.decision_scores and len(self.decision_scores[situation]) > 0:
                possible_actions = self.decision_scores[situation]

                next_action = ""

                for action in possible_actions:
                    if not next_action in possible_actions or possible_actions[action] > possible_actions[next_action]:
                        next_action = action
            else:
                choices = ["STAND", "HIT", "DOUBLE"]

                if hand.can_split():
                    choices.append("SPLIT")

                next_action = random.choice(choices)

            print()

            if next_action.upper() == "STAND":
                hand.stand()
            elif next_action.upper() == "HIT":
                hand.hit()
            elif next_action.upper() == "DOUBLE":
                if game.chips >= hand.bet * 2:
                    hand.double_down()
                else:
                    print("You do not have enough chips to double down")

            elif next_action.upper() == "SPLIT":
                if hand.can_split():
                    new_hands = hand.split()

                    for hand_num, hand in enumerate(new_hands):
                        game.player_hands.append(hand)

                        print()
                        self.play(game, hand, split_num=hand_num + 1)

                    if self in game.player_hands:
                        game.player_hands.remove(self)
                else:
                    print("You cannot split this hand")
            else:
                print("Invalid command, try again")