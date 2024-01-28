# IMPORTANT: Assurez-vous que ce fichier ne soit pas en train de s'éxécuter si vous avez
# effectué des changements non sauvegardés !

# Un système de webhook serait plus adapté à ce genre de mise à jour mais les machines sur
# lesquelles est censé tourner ce script ne sont pas configurées pour recvoir des webhooks

import dotenv
import os
import requests
import time

dotenv.load_dotenv()

repo_url = "https://raw.githubusercontent.com/okayhappex/PixelWar"
file_paths = [
    "main.py",
    "bot/utils.py",
    "bot/embeds.py",
    "bot/images.py",
    "bot/infos.py"
]

def update_bot():
    for file_path in file_paths:
        print(f"Mise à jour de {file_path} depuis {repo_url}/master/{file_path} ...")
        github_url = f"{repo_url}/main/{file_path}"

        response = requests.get(github_url, headers = { 'authorization': os.getenv('GITHUB_PAT') })
        
        if response.status_code == 200:
            if os.path.basename(file_path) == "main.py":
                content = content.replace('TOKEN', 'TOKEN_DEV')
                content = content.replace('autoUpdate = True', 'autoUpdate = False')

            with open(file_path, "w", encoding="utf-8") as local_file:
                if os.path.basename(file_path) == "main.py":
                    local_file.write('')
                    time.sleep(3)
                
                local_file.write(response.text)
                print(f"- {file_path} mis à jour avec succès !")
        else:
            print(f"- Erreur {response.status_code} - Impossible de mettre à jour {file_path}")

def check_release() -> tuple:
    global old_tag

    response = requests.get(f"https://api.github.com/repos/okayhappex/PixelWar/releases", headers = { 'method': 'GET', 'authorization': os.getenv('GITHUB_PAT') })

    if response.status_code == 200:
        releases = response.json()
        release = releases[0]

        if release['tag_name'] != old_tag:
            return True, release['tag_name']
        else:
            return False,
    else:
        print(f"Erreur {response.status_code} - Impossible de vérifier la release")
        return None