# pokemon.py

class Pokemon:
    def __init__(self, data):
        """
        Initializes a Pokemon object with data from the PokeAPI.
        """
        self.name = data['name'].capitalize()
        self.id = data['id']
        self.types = [t['type']['name'] for t in data['types']]
        self.stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        self.image_url = data['sprites']['front_default']

    def get_battle_score(self):
        """
        Calculates a battle score based on all stats.
        """
        total_score = sum(self.stats.values())
        return total_score

    def __str__(self):
        """
        Returns a string representation of the Pokémon, including stats.
        """
        types_str = ', '.join(self.types)
        stats_lines = [
            f"  {stat_name.replace('-', ' ').title()}: {stat_value}"
            for stat_name, stat_value in self.stats.items()
        ]
        stats_str = '\n'.join(stats_lines)
        return (
            f"Selected Pokémon: {self.name}\n"
            f"ID: {self.id}\n"
            f"Types: {types_str}\n"
            f"Stats:\n{stats_str}\n"
            + "-" * 40
        )
