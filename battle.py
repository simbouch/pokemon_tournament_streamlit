# battle.py

import random

def battle_pokemon(pokemon1, pokemon2):
    """Simulates a battle between two Pokémon and returns the winner."""
    score1 = pokemon1.get_battle_score()
    score2 = pokemon2.get_battle_score()

    print(f"\nBattle between {pokemon1.name} and {pokemon2.name}!")
    print(f"{pokemon1.name}'s Score: {score1}")
    print(f"{pokemon2.name}'s Score: {score2}")

    if score1 > score2:
        winner = pokemon1
    elif score2 > score1:
        winner = pokemon2
    else:
        # In case of a tie, select a winner at random
        winner = random.choice([pokemon1, pokemon2])
        print("It's a tie! Winner selected at random.")

    print(f"Winner: {winner.name}")
    return winner
