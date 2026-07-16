from uno.player import Player, BotPlayer
from uno.game import Game
from uno.deck import Deck
from uno.card import WildCard
import random

PLAY_AGAIN_CHOICES = {"yes", "y", "yeah"}

def create_players(deck: Deck) -> list[Player]:
    players = []

    while True:
        try:
            name = input("Enter your name: ")
            players.append(Player(deck, name))
            break

        except ValueError:
            print("You need to actually type a name — spaces by themselves won't work! Try again.")

    while True:
        try:
            bot_count = int(input("How many opponents do you want? "))
            
            if bot_count < 1:
                print("You need at least one opponent.")
                continue
            
            max_bots = Game.MAX_PLAYERS - 1

            if bot_count > max_bots:
                print(f"That's too many! Maximum {max_bots} opponents.")
                continue

            break

        except ValueError:
            print("Please enter a valid integer.")

    for i in range(bot_count):
        players.append(BotPlayer(deck, f"Bot {i+1}"))

    random.shuffle(players)

    return players

def show_welcome():
    print("\n" + "-" * 40)
    print("🃏 WELCOME TO UNO! 🃏".center(40))
    print("-" * 40)
    print("\n📌 HOW TO PLAY:")
    print("  • Match cards by color or number")
    print("  • Action cards: Skip, Reverse, Draw Two")
    print("  • Wild cards: Change color or Draw Four")
    print("  • First to empty their hand WINS! 🏆")
    print("💡 Tip: Plan your moves wisely and use action cards strategically.\n")
    print("Let the game begin! 🎮".center(40))
    print("\n" + "-" * 40)

def start_game():
    deck = Deck()

    players = create_players(deck)

    game = Game(deck, players)

    starting_card = deck.draw_card()
    
    while isinstance(starting_card, WildCard):
        deck.draw_pile.insert(0, starting_card)
        starting_card = deck.draw_card()
    
    deck.discard(starting_card)

    while game.is_running:
        game.process_turn()

def main():
    show_welcome()

    while True:
        start_game()

        choice = input("\n🔄 Play again? (y/n): ")
        
        if choice.strip().lower() not in PLAY_AGAIN_CHOICES:
            break

if __name__ == "__main__":
    main()
