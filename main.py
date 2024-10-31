import blackjack
import sys
from players import HumanBlackjackPlayer, AutoBlackjackPlayer, SmartAutoBlackjackPlayer

def main():
    print("""
=================
|   BLACKJACK   |
=================
""")

    automate = input("Automate games? (y/n) ")

    if automate.lower()[0] == "y":
        games_to_play = int(input("How many games? "))

        dumb_game_results = {blackjack.WIN : 0, blackjack.LOSE : 0, blackjack.PUSH: 0, blackjack.BLACKJACK : 0}
        dumb_player = AutoBlackjackPlayer()
        dumb_game = blackjack.BlackjackGame(dumb_player, 0, verbose=True)

        for i in range(games_to_play):
            print(f"\nGame #{i + 1}:")
            results = dumb_game.play(0)

            for result in results:
                if result in dumb_game_results:
                    dumb_game_results[result] += 1
                else:
                    dumb_game_results[result] = 1
            
                if result == blackjack.WIN:
                    dumb_player.increment_decision_scores(1)
                elif result == blackjack.LOSE:
                    dumb_player.increment_decision_scores(-1)
                elif result == blackjack.PUSH:
                    dumb_player.increment_decision_scores(0.5)

        summarize_results("Dumb Player Results", dumb_game_results)

        with open(f"decision_scores/{games_to_play}_games.txt", "w") as out_file:
            out_file.write(f"Final scores from {games_to_play} games:\n")
            
            for entry in sorted(dumb_player.decision_scores.keys(), key=lambda t: t[0]):
                out_file.write("\n")
                out_file.write(f"Dealer {entry[0]}, ")

                if entry[2]:
                    out_file.write(f"Player {entry[1] - 10}/{entry[1]} ")
                else:
                    out_file.write(f"Player {entry[1]} ")

                if entry[3]:
                    out_file.write(f"(Splittable) ")

                out_file.write(f" -> {dumb_player.decision_scores[entry]}")

        print("Learned how to play blackjack. Now playing games again, but smarter...")

        smart_player = SmartAutoBlackjackPlayer(dumb_player.decision_scores)
        smart_game_results = {blackjack.WIN : 0, blackjack.LOSE : 0, blackjack.PUSH: 0, blackjack.BLACKJACK : 0}
        smart_game = blackjack.BlackjackGame(smart_player, 0, verbose=True)

        for i in range(games_to_play):
            print(f"\nGame #{i + 1}:")
            results = smart_game.play(0)

            for result in results:
                if result in smart_game_results:
                    smart_game_results[result] += 1
                else:
                    smart_game_results[result] = 1

        out_file = open(f"game_results/{games_to_play}_games.txt", "w")
        sys.stdout = out_file

        summarize_results("Smart Player Results", smart_game_results)
        summarize_results("Dumb Player Results", dumb_game_results)

        out_file.close()

    else:
        play_again = "y"
        chips = int(input("How many chips to start with? "))
        game = blackjack.BlackjackGame(HumanBlackjackPlayer(), chips, verbose=True)

        while play_again.lower()[0] == "y":
            bet = int(input("How much to bet? "))
            game.play(bet)
            print()
            play_again = input(f"You have {game.chips} chips. Play again? (y/n) ")

def summarize_results(title, game_results):
    width = len(title) + 4
    print()
    print("=" * width)
    print(title.center(width))
    print("=" * width)
    print(f"      Wins: {game_results[blackjack.WIN]}")
    print(f"    Losses: {game_results[blackjack.LOSE]}")
    print(f"    Pushes: {game_results[blackjack.PUSH]}")
    print(f"Blackjacks: {game_results[blackjack.BLACKJACK]}")
    print(f"  Win rate: {(game_results[blackjack.WIN] + game_results[blackjack.BLACKJACK]) / sum(game_results.values()) * 100:.2f}%")
    print()

main()