# app.py

import streamlit as st
import random
from api import select_random_pokemons
from pokemon import Pokemon

def main():
    st.set_page_config(page_title="Pokémon Tournament Simulator", page_icon=":trophy:", layout="wide")
    st.title("Pokémon Tournament Simulator")
    st.sidebar.title("Settings")

    # Initialize session state variables
    if 'pokemons' not in st.session_state:
        st.session_state['pokemons'] = []
    if 'champion' not in st.session_state:
        st.session_state['champion'] = None
    if 'tournament_results' not in st.session_state:
        st.session_state['tournament_results'] = []
    if 'show_champion' not in st.session_state:
        st.session_state['show_champion'] = False

    # Sidebar for selecting the number of Pokémon
    num_pokemons = st.sidebar.slider(
        "Select Number of Pokémon",
        min_value=4,
        max_value=16,
        step=4,
        value=8,
        help="Choose how many Pokémon will participate in the tournament."
    )

    # Button to fetch Pokémon data in the sidebar
    if st.sidebar.button("Fetch Pokémon"):
        fetch_pokemons(num_pokemons)

    # If Pokémon data is available, display them
    if st.session_state['pokemons']:
        st.header("Participating Pokémon")
        for pokemon in st.session_state['pokemons']:
            display_pokemon(pokemon)

        # Button to start the tournament in the sidebar
        if st.sidebar.button("Start Tournament"):
            champion, tournament_results = run_tournament(st.session_state['pokemons'])
            st.session_state['champion'] = champion
            st.session_state['tournament_results'] = tournament_results
            st.session_state['show_champion'] = False  # Reset the show champion flag

        # If the tournament has been run, display the tournament results
        if st.session_state['champion'] and st.session_state['tournament_results']:
            display_tournament_results(st.session_state['tournament_results'])

            # Move the "Show Champion" button to the sidebar
            if st.sidebar.button("Show Champion"):
                st.session_state['show_champion'] = True

            if st.session_state['show_champion']:
                display_champion(st.session_state['champion'])

    else:
        st.write("Click **Fetch Pokémon** in the sidebar to get the list of participating Pokémon.")

def fetch_pokemons(num_pokemons):
    """Fetches Pokémon data and stores it in the session state."""
    with st.spinner("Fetching Pokémon Data..."):
        pokemon_data_list = select_random_pokemons(num_pokemons=num_pokemons)
        pokemons = [Pokemon(data) for data in pokemon_data_list]
        st.session_state['pokemons'] = pokemons
        st.session_state['champion'] = None
        st.session_state['tournament_results'] = []
        st.session_state['show_champion'] = False
    st.success(f"Successfully fetched data for {num_pokemons} Pokémon!")

def display_pokemon(pokemon):
    """Displays a Pokémon's details without the ID."""
    st.markdown(f"### {pokemon.name}")
    cols = st.columns([1, 2])
    with cols[0]:
        if pokemon.image_url:
            st.image(pokemon.image_url, width=120)
        else:
            st.write("No image available.")
    with cols[1]:
        st.markdown(f"**Types:** {', '.join(pokemon.types)}")
        st.markdown("**Stats:**")
        stats_str = ", ".join([f"{stat_name.replace('-', ' ').title()}: {stat_value}" for stat_name, stat_value in pokemon.stats.items()])
        st.write(stats_str)
    st.divider()

def run_tournament(pokemons):
    """Runs the tournament and returns the champion and the results."""
    tournament_results = []
    round_number = 1
    current_pokemons = pokemons.copy()
    while len(current_pokemons) > 1:
        round_results = {'round': round_number, 'battles': []}
        next_round = []
        for i in range(0, len(current_pokemons), 2):
            pokemon1 = current_pokemons[i]
            pokemon2 = current_pokemons[i + 1]

            winner = battle_pokemon(pokemon1, pokemon2)
            next_round.append(winner)
            round_results['battles'].append({'pokemon1': pokemon1, 'pokemon2': pokemon2, 'winner': winner})
        tournament_results.append(round_results)
        current_pokemons = next_round
        round_number +=1

    champion = current_pokemons[0]
    return champion, tournament_results

def battle_pokemon(pokemon1, pokemon2):
    """Simulates a battle between two Pokémon and returns the winner."""
    score1 = pokemon1.get_battle_score()
    score2 = pokemon2.get_battle_score()

    if score1 > score2:
        winner = pokemon1
    elif score2 > score1:
        winner = pokemon2
    else:
        winner = random.choice([pokemon1, pokemon2])

    return winner

def display_tournament_results(tournament_results):
    """Displays the tournament results with all rounds and battles."""
    for round_info in tournament_results:
        st.header(f"Round {round_info['round']}")
        for battle in round_info['battles']:
            pokemon1 = battle['pokemon1']
            pokemon2 = battle['pokemon2']
            winner = battle['winner']

            st.markdown(f"**{pokemon1.name}** vs **{pokemon2.name}**")
            cols = st.columns(3)
            with cols[0]:
                if pokemon1.image_url:
                    st.image(pokemon1.image_url, width=100)
                else:
                    st.write("No image available.")
                st.markdown(f"**Score:** {pokemon1.get_battle_score()}")
            with cols[1]:
                st.markdown("<h3 style='text-align: center;'>VS</h3>", unsafe_allow_html=True)
            with cols[2]:
                if pokemon2.image_url:
                    st.image(pokemon2.image_url, width=100)
                else:
                    st.write("No image available.")
                st.markdown(f"**Score:** {pokemon2.get_battle_score()}")

            st.success(f"**Winner:** {winner.name}")
            st.divider()

def display_champion(champion):
    """Displays the champion on a separate page with decorations."""
    st.markdown(
        f"""
        <div style="
            background-color: #FFDE00;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        ">
            <h1 style="font-size: 50px; color: #3B4CCA;">🏆 {champion.name} 🏆</h1>
        """,
        unsafe_allow_html=True
    )
    if champion.image_url:
        st.image(champion.image_url, width=300)
    else:
        st.write("No image available.")

    st.markdown(
        f"""
            <h2>Types: {', '.join(champion.types)}</h2>
            <h3>Stats:</h3>
            <p style="font-size: 18px;">
        """,
        unsafe_allow_html=True
    )

    stats_html = ""
    for stat_name, stat_value in champion.stats.items():
        stats_html += f"{stat_name.replace('-', ' ').title()}: {stat_value}<br>"

    st.markdown(stats_html + "</p></div>", unsafe_allow_html=True)
    st.balloons()

if __name__ == "__main__":
    main()
