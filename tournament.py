# tournament.py

from pokemon import Pokemon
from battle import battle_pokemon

def run_tournament(pokemons):
    """Runs the tournament and returns the champion."""
    round_number = 1
    while len(pokemons) > 1:
        print(f"\n--- Round {round_number} ---")
        next_round = []
        for i in range(0, len(pokemons), 2):
            pokemon1 = pokemons[i]
            pokemon2 = pokemons[i + 1]
            winner = battle_pokemon(pokemon1, pokemon2)
            next_round.append(winner)
        pokemons = next_round
        round_number += 1

    champion = pokemons[0]
    print(f"\nChampion of the Tournament: {champion.name}! 🏆")
    return champion
