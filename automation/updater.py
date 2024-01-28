# IMPORTANT: Assurez-vous que ce fichier ne soit pas en train de s'éxécuter si vous avez
# effectué des changements non sauvegardés !

from flask import Flask, request, abort
import os
import requests

def update_bot(repo_url, file_paths):
    for file_path in file_paths:
        print(f"Mise à jour de {file_path} depuis {repo_url}/main/{file_path}...")
        github_url = f"{repo_url}/main/{file_path}"

        response = requests.get(github_url)
        
        if response.status_code == 200:
            if os.path.basename(file_path) == "main.py":
                content = content.replace('TOKEN_DEV', 'TOKEN')

            with open(file_path, "w", encoding="utf-8") as local_file:
                local_file.write(response.text)
                print(f"{file_path} mis à jour avec succès !")
        else:
            print(f"Erreur {response.status_code} - Impossible de mettre à jour {file_path}.")

repo_url = "https://raw.githubusercontent.com/okayhappex/PixelWar"
file_paths = [
    "main.py",
    "bot/utils.py",
    "bot/embeds.py",
    "bot/images.py",
    "bot/utils.py"
]

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('Content-Type') == 'application/json':
        payload = request.json

        if 'release' in payload.get('event'):
            release = payload['release']
            release_tag = release['tag_name']
            release_name = release['name']

            print(f"Version {release_tag} publiée. Le bot va essayer de se mettre à jour")
            print(f"Tag: {release_tag}")
            print(f"Name: {release_name}")
            print("------------------------------")
            update_bot(repo_url, file_paths)

            return 'Webhook received!', 200
        else:
            return 'Event not supported', 400

    return abort(415)    

if __name__ == '__main__':
    app.run(port=5000)