import sys
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

BASE_URL = r"https://fishery.jackboxgames.com/artifact/gallery/RapBattleGame/"
BASE_IMG_URL = r"https://s3.amazonaws.com/jbg-blobcast-artifacts/"

_, battle_id, destination_folder = sys.argv

destination_folder = Path(destination_folder)
if destination_folder.exists():
    i = input(f"{destination_folder} already exists, overwrite? (Y/N)")
    if i.lower() != "y":
        exit()

destination_folder.mkdir(parents=True, exist_ok=True)

response = requests.get(BASE_URL + battle_id)
data = response.json()
rounds = data["gameData"]


def download_image(uri, path):
    print(f"Downloading {uri} to {path}")
    content = requests.get(uri).content
    path.write_bytes(content)
    print(f"Downloaded {path}")
    return True


executor = ThreadPoolExecutor()

for r in rounds:
    round_name = r["title"]
    for c in r["children"]:
        player_name = c["title"]
        file_path = destination_folder / (round_name + "--" + player_name + ".gif")
        image_uri = BASE_IMG_URL + c["twitterOptions"]["imageGifUri"]
        executor.submit(download_image, image_uri, file_path)
