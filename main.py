from blackjack import BlackjackGame

play_again = "y"
chips = int(input("How many chips to start with? "))
game = BlackjackGame(chips, verbose=True)

while play_again.lower()[0] == "y":
    bet = int(input("How much to bet? "))
    game.play(bet)
    play_again = input(f"You have {game.chips} chips. Play again? (y/n) ")