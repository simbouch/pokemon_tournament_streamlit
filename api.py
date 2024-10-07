# api.py

import requests
import random
import time

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

def get_pokemon_data(pokemon_id):
    """Fetches Pokémon data from PokeAPI by ID."""
    try:
        response = requests.get(f"{BASE_URL}{pokemon_id}/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for Pokémon ID {pokemon_id}: {e}")
        return None

def select_random_pokemons(num_pokemons=16, max_pokemon_id=151):
    """Selects a list of unique random Pokémon IDs and fetches their data."""
    selected_pokemons = []
    selected_ids = set()

    while len(selected_pokemons) < num_pokemons:
        pokemon_id = random.randint(1, max_pokemon_id)
        if pokemon_id in selected_ids:
            continue  # Skip if we've already selected this ID

        data = get_pokemon_data(pokemon_id)
        if data:
            selected_pokemons.append(data)
            selected_ids.add(pokemon_id)
            # Print the Pokémon's name
            name = data['name'].capitalize()
            print(f"Selected Pokémon: {name}")
        time.sleep(0.2)  # Be kind to the API

    return selected_pokemons
