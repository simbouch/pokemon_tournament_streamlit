# app.py

import streamlit as st
import random
from api import select_random_pokemons
from pokemon import Pokemon

def main():
    st.title("Pokémon Tournament Simulator")
    st.sidebar.title("Settings")

    num_pokemons = st.sidebar.slider(
        "Select Number of Pokémon",
        min_value=4,
        max_value=16,
        step=4,
        value=8,
        help="Choose how many Pokémon will participate in the tournament."
    )

    if st.sidebar.button("Start Tournament"):
        run_tournament_app(num_pokemons)

def run_tournament_app(num_pokemons):
    st.header("Fetching Pokémon Data...")
    pokemon_data_list = select_random_pokemons(num_pokemons=num_pokemons)
    pokemons = [Pokemon(data) for data in pokemon_data_list]

    st.success(f"Successfully fetched data for {num_pokemons} Pokémon!")

    # Display Pokémon details
    st.header("Participating Pokémon")
    for pokemon in pokemons:
        display_pokemon(pokemon)

    # Run the tournament
    champion = run_tournament_streamlit(pokemons)
    st.balloons()
    st.success(f"The Champion is **{champion.name}**! 🏆")
    st.header("Champion Details")
    display_pokemon(champion)

def display_pokemon(pokemon):
    st.subheader(f"{pokemon.name} (ID: {pokemon.id})")
    cols = st.columns(2)
    with cols[0]:
        if pokemon.image_url:
            st.image(pokemon.image_url)
        else:
            st.write("No image available.")
    with cols[1]:
        st.write(f"**Types:** {', '.join(pokemon.types)}")
        st.write("**Stats:**")
        for stat_name, stat_value in pokemon.stats.items():
            st.write(f"- {stat_name.replace('-', ' ').title()}: {stat_value}")
    st.write("---")

def run_tournament_streamlit(pokemons):
    round_number = 1
    while len(pokemons) > 1:
        st.header(f"Round {round_number}")
        next_round = []
        for i in range(0, len(pokemons), 2):
            pokemon1 = pokemons[i]
            pokemon2 = pokemons[i + 1]

            winner = battle_pokemon_streamlit(pokemon1, pokemon2)
            next_round.append(winner)
        pokemons = next_round
        round_number += 1
    champion = pokemons[0]
    return champion

def battle_pokemon_streamlit(pokemon1, pokemon2):
    score1 = pokemon1.get_battle_score()
    score2 = pokemon2.get_battle_score()

    st.write(f"**{pokemon1.name}** vs **{pokemon2.name}**")
    cols = st.columns(2)
    with cols[0]:
        if pokemon1.image_url:
            st.image(pokemon1.image_url)
        else:
            st.write("No image available.")
        st.write(f"Score: {score1}")
    with cols[1]:
        if pokemon2.image_url:
            st.image(pokemon2.image_url)
        else:
            st.write("No image available.")
        st.write(f"Score: {score2}")

    if score1 > score2:
        winner = pokemon1
    elif score2 > score1:
        winner = pokemon2
    else:
        winner = random.choice([pokemon1, pokemon2])
        st.info("It's a tie! Winner selected at random.")

    st.success(f"Winner: **{winner.name}**")
    st.write("---")
    return winner

if __name__ == "__main__":
    main()


