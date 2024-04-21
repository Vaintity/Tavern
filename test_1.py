import requests

def game_id_check(value):
        link_game = "https://www.cheapshark.com/api/1.0/games"
        response = requests.get(link_game, params={"id": value})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return "0"
        
id = input("Enter id: ")
print(game_id_check(id))