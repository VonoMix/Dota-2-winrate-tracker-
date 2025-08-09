import requests

def fetch_hero_data():
    try:
        response = requests.get("https://api.opendota.com/api/heroes")
        response.raise_for_status()
        heroes = response.json()
        id_to_name = {hero["id"]: hero["localized_name"] for hero in heroes}
        return id_to_name
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных о героях: {e}")
        return None

def get_dota_buff_data(player_id):
    url = f"https://api.opendota.com/api/players/{player_id}/recentMatches"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных о матчах: {e}")
        return None

id_to_name = fetch_hero_data()

if id_to_name is None:
    print("Не удалось загрузить данные героев. Завершаем программу.")
    exit(1)  

player_id = 910074422
matches = get_dota_buff_data(player_id)
winned_matches = 0
total_matches = 10

if matches:
    for match in matches[:10]:
        player_side = "Radiant" if match["player_slot"] < 128 else "Dire"
        if (player_side == "Radiant" and match["radiant_win"]) or \
           (player_side == "Dire" and not match["radiant_win"]):
            result = "Win"
            winned_matches += 1
        else:
            result = "Loss"
        hero_id = match["hero_id"]
        hero_name = id_to_name.get(hero_id, "Unknown Hero")  # здесь id_to_name точно определён
        print(f"Match ID: {match['match_id']}, Hero: {hero_name}, Kills: {match['kills']}, Deaths: {match['deaths']}, Assists: {match['assists']}, Side: {player_side}, Result: {result}")
else:
    print("Нет данных о матчах")

if total_matches > 0:
    win_rate = (winned_matches / total_matches) * 100
    print(f"\nПроцент побед за последние {total_matches} матчей: {win_rate:.2f}%")
else:
    print("Нет матчей для анализа.")
