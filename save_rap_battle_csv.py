import csv
import requests
import sys
from collections import namedtuple

BASE_URL = r"https://fishery.jackboxgames.com/artifact/gallery/RapBattleGame/"
BASE_IMG_URL = r"https://s3.amazonaws.com/jbg-blobcast-artifacts/"

Rap = namedtuple(
    "Rap",
    [
        "game_tag",
        "game_id",
        "player_name",
        "round_number",
        "text",
        "image_uri",
    ],
)


def get_game_data(game_id):
    response = requests.get(BASE_URL + game_id)
    return response.json()


def collect_raps(game_tag, game_id):
    game_data = get_game_data(game_id)
    rounds = game_data["gameData"]
    raps = []
    for r in rounds:
        round_number = int(r["title"].split()[-1])
        for c in r["children"]:
            player_name = c["title"]
            text = c["twitterOptions"]["defaultText"].split("#")[0]
            image_uri = BASE_IMG_URL + c["twitterOptions"]["imageGifUri"]
            raps.append(
                Rap(game_tag, game_id, player_name, round_number, text, image_uri)
            )

    return raps


def write_raps_to_csv(raps, dest):
    with open(dest, 'w', newline='') as f:
        writer = csv.writer(f, )
        writer.writerow(Rap._fields)
        writer.writerows(raps)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        game_ids = [line.split() for line in f]

    raps = []
    for game_tag, game_id in game_ids:
        raps += collect_raps(game_tag, game_id)

    write_raps_to_csv(raps, sys.argv[2])
