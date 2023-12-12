import json
import requests
import sqlite3
import os

url = "https://api-football-v1.p.rapidapi.com/v3/players"
query_params = {
    "league": "179",
    "season": "2022",
    "page": 1 
}
headers = {
    "X-RapidAPI-Key": "1e705204e6mshc048b497fc855ebp13e036jsn27841de4c463",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}
all_players_data = []

while True:
    response = requests.get(url, headers=headers, params=query_params)

    if response.status_code == 200:
        data = response.json()
        players = data.get('response', [])
        all_players_data.extend(players)

        if data['paging'].get('current') < data['paging'].get('total'): 
            query_params['page'] += 1  
        else:
            break  
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        break  

if all_players_data:  
    file_path = r"finalproject/scotplayers.json"
    with open(file_path, 'w') as json_file:
        json.dump(all_players_data, json_file)  
    print("Data written to scotplayers.json successfully.")
else:
    print("No data retrieved or an error occurred during retrieval.")



def create_table():
    db_path = r"finalproject\football.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attackers (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            club TEXT,
            appearances INTEGER,
            position TEXT,
            goals INTEGER,
            UNIQUE(id) 
        )
    ''')

    conn.commit()
    conn.close()

def insert_players_data(players_data):
    db_path = r"finalproject\football.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for i in range(0, len(players_data), 25):
        batch = players_data[i:i + 25]  

        for player in batch:
                position = player['statistics'][0]['games']['position']
                if position.lower() == 'attacker':
                    player_id = player['player']['id']
                    first_name = player['player']['firstname']  
                    last_name = player['player']['lastname']                     
                    games_appearances = player['statistics'][0]['games']['appearences']
                    goals_scored = player['statistics'][0]['goals']['total']
                    club_name = player['statistics'][0]['team']['name']

                    print(f"Inserting: {player_id}, {first_name}, {last_name}, {club_name}, {games_appearances}, {position}, {goals_scored}")

                    cursor.execute('''
                        INSERT OR IGNORE INTO attackers (id, first_name, last_name, club, appearances, position, goals)        
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (player_id, first_name, last_name, club_name, games_appearances, position, goals_scored))

        conn.commit()

    conn.close()

file_path = r"finalproject\scotplayers.json"
with open(file_path, 'r') as file:
    player_data_from_file = json.load(file)

create_table()

insert_players_data(player_data_from_file)

url = "https://api.sportmonks.com/v3/football/players/countries/1161"
api_token = "bTFkpunfnlsQvHXEPym7cX2vRYMZwi7LpV06YGEe2BaMTf1fbPyyGFVkMXck"

all_player_data = []

while url:
    response = requests.get(url, params={'api_token': api_token})
    data = response.json()

    if 'error' in data:
        print(f"Error encountered: {data['error']['message']}")
        break  

    all_player_data.extend(data['data'])

    pagination = data.get('pagination', {})
    url = pagination.get('next_page')

script_directory = r"finalproject"

db_filename = os.path.join(script_directory, 'football.db')
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    firstname TEXT,
    lastname TEXT,
    country_id INTEGER
)
''')

for player in all_player_data:
    cursor.execute('''
        INSERT INTO players (firstname, lastname, country_id)
        VALUES (?, ?, ?)
    ''', (player['firstname'], player['lastname'], player['country_id']))

conn.commit()
conn.close()

file_path = r"finalproject\leagues_data.json"
with open(file_path, 'w') as json_file:
    json.dump(all_player_data, json_file, indent=2)
print("Player data written to 'player_data.json'")


