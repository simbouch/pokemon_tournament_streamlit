# pokemon_tournament_streamlit
 Pokémon Tournament Simulator
Welcome to the Pokémon Tournament Simulator, a web application built with Streamlit that simulates a tournament between randomly selected Pokémon using data from the PokeAPI. The app fetches real-time Pokémon data, displays their stats and images, and simulates battles based on their stats to determine a champion.

Table of Contents
Description
Features
Project Structure
Requirements
Installation
Usage
Screenshots
Future Enhancements
Acknowledgments
Description
This project is a web-based application that allows users to simulate a Pokémon tournament. Users can select the number of participating Pokémon, and the app will fetch their data from the PokeAPI. The Pokémon are displayed with their images, types, and stats. The tournament proceeds through elimination rounds until a champion is crowned.

Features
Interactive Web Interface: Built with Streamlit for a user-friendly experience.
Random Pokémon Selection: Fetches random Pokémon data from the PokeAPI.
Pokémon Details: Displays images, types, and stats of each Pokémon.
Battle Simulation: Simulates battles based on the total stats of Pokémon.
Tournament Progression: Shows each round and the winners until the champion is determined.
Responsive Design: Accessible via web browsers on various devices.
Project Structure
Copy code
pokemon_tournament_streamlit/
├── app.py
├── api.py
├── pokemon.py
├── requirements.txt
app.py: The main Streamlit application.
api.py: Handles API requests to the PokeAPI.
pokemon.py: Defines the Pokemon class.
requirements.txt: Contains all the Python dependencies required to run the app.
Requirements
Python 3.6 or higher
Python Packages
The required packages are listed in requirements.txt. They include:

streamlit
requests
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/simbouch/pokemon_tournament_streamlit.git
cd pokemon_tournament_streamlit
Create a virtual environment (recommended):

bash
Copy code
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy code
venv\Scripts\activate
On macOS/Linux:

bash
Copy code
source venv/bin/activate
Install the required packages:

bash
Copy code
pip install -r requirements.txt
The requirements.txt file includes all the necessary dependencies for the project.

Usage
Run the Streamlit app:

bash
Copy code
streamlit run app.py
Open the app in your browser:

Streamlit should automatically open a new browser tab. If not, navigate to the URL provided in the terminal (usually http://localhost:8501).

Use the app:

Select the number of Pokémon in the sidebar.
Click on "Start Tournament" to begin.
Watch as the tournament progresses through each round.
View details of each battle and the champion.
