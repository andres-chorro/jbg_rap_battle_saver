import sys, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

BASE_URL = r'https://fishery.jackboxgames.com/artifact/gallery/RapBattleGame/'
BASE_IMG_URL = r'https://s3.amazonaws.com/jbg-blobcast-artifacts/'

_, battle_id, destination_folder = sys.argv

destination_folder = Path(destination_folder)
if destination_folder.exists():
    i = input(f'{destination_folder} already exists, overwrite? (Y/N)')
    if i.lower() != 'y':
        exit()

destination_folder.mkdir(parents=True, exist_ok=True)

response = requests.get(BASE_URL + battle_id)
data = response.json()
rounds = data['gameData']

def download_image(uri, dest):
    print(f'Downloading {uri} to {dest}')
    content = requests.get(uri).content
    file_path.write_bytes(content)
    print(f'Downloaded {dest}')

futures = []
with ThreadPoolExecutor() as executor:
    for r in rounds:
        round_name = r['title']
        for c in r['children']:
            player_name = c['title']
            file_path = destination_folder / (round_name + '_' + player_name + '.gif')
            image_uri = BASE_IMG_URL + c['twitterOptions']['imageGifUri']
            futures.append(executor.submit(download_image, image_uri, file_path))
        
for f in futures:
    print(f.exception())
