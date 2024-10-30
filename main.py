from blackjack import BlackjackGame

play_again = "y"

while play_again.lower()[0] == "y":
    BlackjackGame(100, verbose=True).play()
    play_again = input("Play again? (y/n) ")