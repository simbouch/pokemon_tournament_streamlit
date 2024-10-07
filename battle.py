# battle.py

import random
from type_chart import type_chart

def calculate_type_effectiveness(attacking_pokemon, defending_pokemon):
    """Calculates the type effectiveness multiplier."""
    multiplier = 1.0
    for attack_type in attacking_pokemon.types:
        for defense_type in defending_pokemon.types:
            effectiveness = type_chart.get(attack_type, {}).get(defense_type, 1)
            multiplier *= effectiveness
    return multiplier


def battle_pokemon(pokemon1, pokemon2):
    """Simulates a battle between two Pokémon considering type effectiveness and returns the winner."""
    score1 = pokemon1.get_battle_score()
    score2 = pokemon2.get_battle_score()

    # Type effectiveness
    effectiveness1 = calculate_type_effectiveness(pokemon1, pokemon2)
    effectiveness2 = calculate_type_effectiveness(pokemon2, pokemon1)

    # Randomness and critical hits
    randomness1 = random.uniform(0.85, 1.0)
    critical_hit1 = 1.5 if random.random() < 0.1 else 1  # 10% chance of critical hit

    randomness2 = random.uniform(0.85, 1.0)
    critical_hit2 = 1.5 if random.random() < 0.1 else 1  # 10% chance of critical hit

    adjusted_score1 = score1 * effectiveness1 * randomness1 * critical_hit1
    adjusted_score2 = score2 * effectiveness2 * randomness2 * critical_hit2

    print(f"\nBattle between {pokemon1.name} and {pokemon2.name}!")
    print(f"{pokemon1.name}'s Base Score: {score1}")
    print(f"{pokemon2.name}'s Base Score: {score2}")
    print(f"{pokemon1.name}'s Adjusted Score: {adjusted_score1:.2f} (Effectiveness x{effectiveness1}, Random x{randomness1:.2f}, Critical Hit x{critical_hit1})")
    print(f"{pokemon2.name}'s Adjusted Score: {adjusted_score2:.2f} (Effectiveness x{effectiveness2}, Random x{randomness2:.2f}, Critical Hit x{critical_hit2})")

    if adjusted_score1 > adjusted_score2:
        winner = pokemon1
    elif adjusted_score2 > adjusted_score1:
        winner = pokemon2
    else:
        winner = random.choice([pokemon1, pokemon2])
        print("It's a tie! Winner selected at random.")

    print(f"Winner: {winner.name}")
    return winner
