# app.py

import streamlit as st
import random
from api import select_random_pokemons
from pokemon import Pokemon
from type_chart import type_chart

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

            winner, battle_details = battle_pokemon(pokemon1, pokemon2)
            next_round.append(winner)
            round_results['battles'].append(battle_details)
        tournament_results.append(round_results)
        current_pokemons = next_round
        round_number +=1

    champion = current_pokemons[0]
    return champion, tournament_results

def battle_pokemon(attacker, defender):
    """Simulates a battle between two Pokémon and returns the winner with detailed scoring."""
    score1 = attacker.get_battle_score()
    score2 = defender.get_battle_score()

    # Type effectiveness
    effectiveness1 = calculate_type_effectiveness(attacker, defender)
    effectiveness2 = calculate_type_effectiveness(defender, attacker)

    # Randomness and critical hits
    randomness1 = random.uniform(0.85, 1.0)
    critical_hit1 = 1.5 if random.random() < 0.1 else 1

    randomness2 = random.uniform(0.85, 1.0)
    critical_hit2 = 1.5 if random.random() < 0.1 else 1

    adjusted_score1 = score1 * effectiveness1 * randomness1 * critical_hit1
    adjusted_score2 = score2 * effectiveness2 * randomness2 * critical_hit2

    # Determine the winner
    if adjusted_score1 > adjusted_score2:
        winner = attacker
    elif adjusted_score2 > adjusted_score1:
        winner = defender
    else:
        winner = random.choice([attacker, defender])

    battle_details = {
        'attacker': attacker,
        'defender': defender,
        'winner': winner,
        'score1': score1,
        'score2': score2,
        'adjusted_score1': adjusted_score1,
        'adjusted_score2': adjusted_score2,
        'effectiveness1': effectiveness1,
        'effectiveness2': effectiveness2,
        'randomness1': randomness1,
        'randomness2': randomness2,
        'critical_hit1': critical_hit1,
        'critical_hit2': critical_hit2
    }

    return winner, battle_details

def calculate_type_effectiveness(attacking_pokemon, defending_pokemon):
    """Calculates the type effectiveness multiplier."""
    multiplier = 1.0
    for attack_type in attacking_pokemon.types:
        for defense_type in defending_pokemon.types:
            effectiveness = type_chart.get(attack_type, {}).get(defense_type, 1)
            multiplier *= effectiveness
    return multiplier

def display_tournament_results(tournament_results):
    """Displays the tournament results with all rounds and battles."""
    for round_info in tournament_results:
        st.header(f"Round {round_info['round']}")
        for battle in round_info['battles']:
            attacker = battle['attacker']
            defender = battle['defender']
            winner = battle['winner']

            st.markdown(f"**{attacker.name}** vs **{defender.name}**")
            cols = st.columns(3)
            with cols[0]:
                if attacker.image_url:
                    st.image(attacker.image_url, width=100)
                else:
                    st.write("No image available.")
                st.write(f"Base Score: {battle['score1']}")
                st.write(f"Adjusted Score: {battle['adjusted_score1']:.2f}")
                st.write(f"Type Effectiveness: x{battle['effectiveness1']}")
                st.write(f"Randomness: x{battle['randomness1']:.2f}")
                if battle['critical_hit1'] > 1:
                    st.write("Critical Hit!")
            with cols[1]:
                st.markdown("<h3 style='text-align: center;'>VS</h3>", unsafe_allow_html=True)
            with cols[2]:
                if defender.image_url:
                    st.image(defender.image_url, width=100)
                else:
                    st.write("No image available.")
                st.write(f"Base Score: {battle['score2']}")
                st.write(f"Adjusted Score: {battle['adjusted_score2']:.2f}")
                st.write(f"Type Effectiveness: x{battle['effectiveness2']}")
                st.write(f"Randomness: x{battle['randomness2']:.2f}")
                if battle['critical_hit2'] > 1:
                    st.write("Critical Hit!")
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
