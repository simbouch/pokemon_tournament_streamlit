# app.py

import streamlit as st
import random
from api import select_random_pokemons
from pokemon import Pokemon
from type_chart import type_chart

def main():
    # Set Page Configuration
    st.set_page_config(page_title="Pokémon Tournament Simulator", page_icon=":trophy:", layout="wide")
    
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Tournament", "Champion", "Settings"])

    # Initialize session state variables
    if 'pokemons' not in st.session_state:
        st.session_state['pokemons'] = []
    if 'champion' not in st.session_state:
        st.session_state['champion'] = None
    if 'tournament_results' not in st.session_state:
        st.session_state['tournament_results'] = []
    if 'weights' not in st.session_state:
        st.session_state['weights'] = {
            'hp': 1.0,
            'attack': 2.0,
            'defense': 1.5,
            'special-attack': 2.0,
            'special-defense': 1.5,
            'speed': 1.0
        }

    # Page Navigation
    if page == "Home":
        home_page()
    elif page == "Tournament":
        tournament_page()
    elif page == "Champion":
        champion_page()
    elif page == "Settings":
        settings_page()

def home_page():
    st.title("Home")
    
    # Sidebar for selecting the number of Pokémon
    num_pokemons = st.sidebar.slider(
        "Select Number of Pokémon",
        min_value=4,
        max_value=16,
        step=4,
        value=8,
        help="Choose how many Pokémon will participate in the tournament."
    )

    # Button to fetch Pokémon data
    if st.sidebar.button("Fetch Pokémon"):
        fetch_pokemons(num_pokemons)

    # Display fetched Pokémon
    if st.session_state['pokemons']:
        st.header("Participating Pokémon")
        for pokemon in st.session_state['pokemons']:
            display_pokemon(pokemon)
    else:
        st.write("Click **Fetch Pokémon** in the sidebar to get the list of participating Pokémon.")

def tournament_page():
    st.title("Tournament")
    
    pokemons = st.session_state.get('pokemons', [])
    
    if not pokemons:
        st.warning("No Pokémon fetched. Please go to the Home page and fetch Pokémon first.")
        return

    if st.button("Run Tournament"):
        with st.spinner("Running the tournament..."):
            try:
                champion, tournament_results = run_tournament(pokemons)
                st.session_state['champion'] = champion
                st.session_state['tournament_results'] = tournament_results
                st.success("Tournament completed!")
            except Exception as e:
                st.error(f"An error occurred during the tournament: {e}")

    # Display tournament results if available
    if st.session_state.get('tournament_results'):
        display_tournament_results(st.session_state['tournament_results'])

def champion_page():
    st.title("Champion")
    
    champion = st.session_state.get('champion', None)
    
    if not champion:
        st.warning("No champion yet. Please run the tournament first on the Tournament page.")
        return

    display_champion(champion)

def settings_page():
    st.title("Settings")
    
    st.write("Configure your tournament settings here.")
    
    # Adjust weights for battle score calculation
    st.subheader("Battle Score Weights")
    st.write("Adjust the importance of each stat in calculating the battle score.")
    
    weights = st.session_state['weights']
    
    # Update each weight using a slider
    weights['hp'] = st.slider("HP Weight", 0.5, 2.0, weights['hp'], 0.1)
    weights['attack'] = st.slider("Attack Weight", 1.0, 3.0, weights['attack'], 0.1)
    weights['defense'] = st.slider("Defense Weight", 1.0, 3.0, weights['defense'], 0.1)
    weights['special-attack'] = st.slider("Special Attack Weight", 1.0, 3.0, weights['special-attack'], 0.1)
    weights['special-defense'] = st.slider("Special Defense Weight", 1.0, 3.0, weights['special-defense'], 0.1)
    weights['speed'] = st.slider("Speed Weight", 0.5, 2.0, weights['speed'], 0.1)
    
    st.session_state['weights'] = weights
    
    st.success("Battle score weights updated!")

def fetch_pokemons(num_pokemons):
    """Fetches Pokémon data and stores it in the session state."""
    try:
        with st.spinner("Fetching Pokémon Data..."):
            pokemon_data_list = select_random_pokemons(num_pokemons=num_pokemons)
            pokemons = [Pokemon(data) for data in pokemon_data_list]
            st.session_state['pokemons'] = pokemons
            st.session_state['champion'] = None
            st.session_state['tournament_results'] = []
        st.success(f"Successfully fetched data for {num_pokemons} Pokémon!")
    except Exception as e:
        st.error(f"An error occurred while fetching Pokémon data: {e}")

def display_pokemon(pokemon):
    """Displays a Pokémon's details without the ID."""
    cols = st.columns([1, 3])
    with cols[0]:
        if pokemon.image_url:
            st.image(pokemon.image_url, width=120)
        else:
            st.write("No image available.")
    with cols[1]:
        st.markdown(f"### {pokemon.name}")
        st.markdown(f"**Types:** {', '.join(pokemon.types)}")
        stats_str = ", ".join([f"{stat_name.replace('-', ' ').title()}: {stat_value}" for stat_name, stat_value in pokemon.stats.items()])
        st.write(f"**Stats:** {stats_str}")
    st.markdown("---")

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
            if i + 1 < len(current_pokemons):
                pokemon2 = current_pokemons[i + 1]
                winner, battle_details = battle_pokemon(pokemon1, pokemon2)
                next_round.append(winner)
                round_results['battles'].append(battle_details)
            else:
                # Odd number: Pokémon1 advances automatically
                next_round.append(pokemon1)
                battle_details = {
                    'attacker': pokemon1,
                    'defender': None,
                    'winner': pokemon1,
                    'score1': pokemon1.get_battle_score(st.session_state['weights']),
                    'score2': None,
                    'adjusted_score1': pokemon1.get_battle_score(st.session_state['weights']),
                    'adjusted_score2': None,
                    'effectiveness1': 1.0,
                    'effectiveness2': 1.0,
                    'randomness1': 1.0,
                    'randomness2': 1.0,
                    'critical_hit1': 1,
                    'critical_hit2': 1
                }
                round_results['battles'].append(battle_details)
        tournament_results.append(round_results)
        current_pokemons = next_round
        round_number +=1

    champion = current_pokemons[0]
    return champion, tournament_results

def battle_pokemon(attacker, defender):
    """Simulates a battle between two Pokémon and returns the winner with detailed scoring."""
    # Retrieve weights from session state
    weights = st.session_state.get('weights', {
        'hp': 1.0,
        'attack': 2.0,
        'defense': 1.5,
        'special-attack': 2.0,
        'special-defense': 1.5,
        'speed': 1.0
    })
    
    # Calculate battle scores using dynamic weights
    score1 = attacker.get_battle_score(weights)
    score2 = defender.get_battle_score(weights)

    # Type effectiveness
    effectiveness1 = calculate_type_effectiveness(attacker, defender)
    effectiveness2 = calculate_type_effectiveness(defender, attacker)

    # Randomness and critical hits
    randomness1 = random.uniform(0.85, 1.0)
    critical_hit1 = 1.5 if random.random() < 0.1 else 1

    randomness2 = random.uniform(0.85, 1.0)
    critical_hit2 = 1.5 if random.random() < 0.1 else 1

    # Adjust scores based on effectiveness, randomness, and critical hits
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

            if defender:
                # Display battle between two Pokémon
                cols = st.columns([2, 1, 2])
                with cols[0]:
                    if attacker.image_url:
                        st.image(attacker.image_url, width=100)
                    else:
                        st.write("No image available.")
                    st.markdown(f"**{attacker.name}**")
                    st.write(f"Base Score: {battle['score1']}")
                    st.write(f"Adjusted Score: {battle['adjusted_score1']:.2f}")
                    st.write(f"Type Effectiveness: x{battle['effectiveness1']}")
                    st.write(f"Randomness: x{battle['randomness1']:.2f}")
                    if battle['critical_hit1'] > 1:
                        st.write("**Critical Hit!**")

                with cols[1]:
                    st.markdown("<h3 style='text-align: center;'>VS</h3>", unsafe_allow_html=True)

                with cols[2]:
                    if defender.image_url:
                        st.image(defender.image_url, width=100)
                    else:
                        st.write("No image available.")
                    st.markdown(f"**{defender.name}**")
                    st.write(f"Base Score: {battle['score2']}")
                    st.write(f"Adjusted Score: {battle['adjusted_score2']:.2f}")
                    st.write(f"Type Effectiveness: x{battle['effectiveness2']}")
                    st.write(f"Randomness: x{battle['randomness2']:.2f}")
                    if battle['critical_hit2'] > 1:
                        st.write("**Critical Hit!**")

                st.success(f"**Winner:** {winner.name}")
                st.markdown("---")
            else:
                # Display Pokémon advancing automatically
                st.markdown(f"**{attacker.name}** advances automatically.")
                st.markdown("---")

def display_champion(champion):
    """Displays the champion on a decorated page with animations."""
    st.markdown(
        f"""
        <div style="
            background-color: #FFD700;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        ">
            <h1 style="font-size: 50px; color: #FF4500;">🏆 {champion.name} 🏆</h1>
            <h2>Types: {', '.join(champion.types)}</h2>
            <h3>Stats:</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display Stats
    stats = champion.stats
    stats_formatted = ", ".join([f"{stat.replace('-', ' ').title()}: {value}" for stat, value in stats.items()])
    st.write(f"**Stats:** {stats_formatted}")

    # Display Image
    if champion.image_url:
        st.image(champion.image_url, width=300)
    else:
        st.write("No image available.")
    
    # Celebrate the Champion
    st.balloons()

if __name__ == "__main__":
    main()
