# Pixelwar

**Pré-requis:**
- Python 3.11 ou supérieur
- Un compte [développeur](https://discord.com/developers) sur Discord
- Un compte [Deta](https://deta.space)

## Commandes

### Commandes de modération: `manage`
**Permission par défaut: `manage_events`**

* **[`/manage gamemode <mode: nombre>`](https://github.com/okayhappex/PixelWar/blob/e0cd342b1206efe12fe3adb620bbfec1bbeaf4a7/main.py#L42)** Cette commande permet de changer le mode de la partie. `mode` prend un chiffre entre 0 et 2 inclus, chaque chiffre signifiant respectivement `paused` (toutes les commandes sont desactivées), `competition` (toutes les commandes sont activées) et `training` (les commandes `game` et `team` sont desactivées).
* **[`/manage blacklist-set <membre: Utilisateur> <blacklisted: booléen>`](https://github.com/okayhappex/PixelWar/blob/e0cd342b1206efe12fe3adb620bbfec1bbeaf4a7/main.py#L54)** Cette commande permet d'ajouter ou d'enlever un utilisateur de la blacklist. Un utilisateur blacklisté sera ignoré par le bot lorsqu'il tentera d'effectuer une commande.
* **[`/manage blacklist-show`](https://github.com/okayhappex/PixelWar/blob/e0cd342b1206efe12fe3adb620bbfec1bbeaf4a7/main.py#L69)** Cette commande montre tous les membres dans la blacklist.

**La blacklist agit sur tous les utilisateurs étant dedans, même les administrateurs. Les commandes de modération sont en revanche toujours accessibles à ceux-ci**

### Commandes liées à la partie: `game`
**Permission par défaut: `@everyone`**

* **[`/game leaderboard <maximum: nombre = 5>`](https://github.com/okayhappex/PixelWar/blob/e0cd342b1206efe12fe3adb620bbfec1bbeaf4a7/main.py#L92) _(Compétition uniquement)_** Cette commande affiche le classement de la partie. Si `maximum` est trop grand ou égal à 0, tous les membres de la partie seront affichés.
* **[`/game generate-gif`](https://github.com/okayhappex/PixelWar/blob/e0cd342b1206efe12fe3adb620bbfec1bbeaf4a7/main.py#L128) Cette commande permet d'afficher toutes les sauvegardes de la partie sous la forme d'un gif.

### Commandes liées aux équipes: `team` _(Compétition uniquement)_
**Permission par défaut: `@everyone`**

* **[`/team create <name: texte> <color: hexadécimal>`](https://github.com/okayhappex/PixelWar/blob/e0cd342b1206efe12fe3adb620bbfec1bbeaf4a7/main.py#L136)** Cette commande crée une équipe et y ajoute automatiquement l'utilisateur. La couleur doit être en hexadécimal et
* 
