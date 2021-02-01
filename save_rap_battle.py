import sys, requests
from pathlib import Path

BASE_URL = r'https://fishery.jackboxgames.com/artifact/gallery/RapBattleGame/'
BASE_IMG_URL = r'https://s3.amazonaws.com/jbg-blobcast-artifacts/'

_, battle_id, destination_folder = sys.argv

destination_folder = Path(destination_folder)
if destination_folder.exists():
    i = input(f'{destination_folder} already exists, overwrite? (Y/N)')
    if i.lower() != 'y':
        exit()

response = requests.get(BASE_URL + battle_id)
data = response.json()
rounds = data['gameData']

for r in rounds:
    round_name = r['title']
    round_dir = destination_folder / round_name
    round_dir.mkdir(parents=True, exist_ok=True)
    for c in r['children']:
        player_name = c['title']
        image_uri = BASE_IMG_URL + c['twitterOptions']['imageGifUri']
        file_path = destination_folder / round_name / (player_name + '.gif')

        print(f'Downloading {round_name} image for {player_name}: {image_uri}')
        content = requests.get(image_uri).content
        file_path.write_bytes(content)
        
print("Done!")

