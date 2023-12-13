import discord
import images
import utils

class TeamEvents:
    def __init__(self, infos: tuple | list = ()) -> None:
        self.infos = infos
    
    # Errors
    def notExisting(self) -> discord.Embed:
        title = "Impossible de rejoindre l'équipe !"
        description = f"L'équipe **__{self.infos[0]}__** n'existe pas encore. Vous pouvez la créer dès maintenant avec la commande **</team create:2000>**"
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)
    
    def notInvited(self) -> discord.Embed:
        title = "Impossible de rejoindre l'équipe."
        description = f"L'équipe **__{self.infos[0]}__** ne vous a pas invité. Demandez à son créateur de vous inviter."
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)

    def alreadyExisting(self) -> discord.Embed:
        title = "Impossible de créer l'équipe."
        description = f"L'équipe **__{self.infos[0]}__** existe déjà. \n> :bulb: **Astuce:** Sur ordinateur, tu peux appuyer sur la flèche du haut pour modifier ta commande."
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)

    def alreadyInTeam(self) -> discord.Embed:
        title = "Impossible de créer ou rejoindre l'équipe."
        description = f"Vous êtes déjà dans l'équipe **__{self.infos[0]}__**."
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)
    
    def inAnotherTeam(self) -> discord.Embed:
        title = "Impossible d'inviter le membre."
        description = f"{self.infos[1]} déjà dans l'équipe **__({self.infos[0]})__**."
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)
    
    def notInAnyTeam(self) -> discord.Embed:
        title = "Impossible d'effectuer l'action."
        description = "Vous n'avez pas d'équipe dans cette partie."
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)

    def colorAlreadyTaken(self) -> discord.Embed:
        title = "Impossible de créer l'équipe."
        description = f"La couleur **__({self.infos[0]})__** est déjà prise.  \n> :bulb: **Astuce:** Sur ordinateur, tu peux appuyer sur la flèche du haut pour modifier ta commande."
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)

    def colorInvalid(self) -> discord.Embed:
        title = "Impossible de créer l'équipe."
        description = f"La couleur **__({self.infos[0]})__** n'est pas dans le format demandé: `(0~255, 0~255, 0~255)`.  \n> :bulb: **Astuce:** Sur ordinateur, tu peux appuyer sur la flèche du haut pour modifier ta commande."
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)
    
    # Success
    def teamCreated(self) -> discord.Embed:
        clr = utils.RGB(self.infos[1][0], self.infos[1][1], self.infos[1][2])
        title = "L'équipe est créée !"
        description = f"L'équipe  **__({self.infos[0]})__** vient d'être créée !\n:bulb: **__Inviter un membre:__ </team invite:2000>**"
        color = discord.Colour.from_rgb(clr.red, clr.green, clr.blue)

        return discord.Embed(title = title, description = description, color = color)
    
    def teamJoined(self) -> discord.Embed:
        clr = self.infos[1]
        title = "Vous avez rejoint l'équipe !"
        description = f"Tu viens de rejoindre l'équipe  **__({self.infos[0]})__** !\n:bulb: **__Quitter l'équipe:__ </team leave:2000>**"
        color = discord.Colour.from_rgb(clr.red, clr.green, clr.blue)

        return discord.Embed(title = title, description = description, color = color)
    
    def teamLeft(self) -> discord.Embed:
        clr = self.infos[1]
        title = "Vous avez quitté l'équipe !"
        description = f"Tu viens de quitter l'équipe  **__({self.infos[0]})__** !\n:bulb: **__Rejoindre une autre équipe:__ </team join:2000>**"
        color = discord.Colour.from_rgb(clr.red, clr.green, clr.blue)

        return discord.Embed(title = title, description = description, color = color)

    def teamDeleted(self) -> discord.Embed:
        clr = self.infos[1]
        title = "Vous avez supprimé l'équipe !"
        description = f"Tu viens de supprimer l'équipe  **__({self.infos[0]})__** !\n:bulb: **Astuce:** Tous les membres de cette équipe peuvent rejoindre une autre équipe."
        color = discord.Colour.from_rgb(clr.red, clr.green, clr.blue)

        return discord.Embed(title = title, description = description, color = color)

    def memberInvited(self) -> discord.Embed:
        clr = self.infos[2]
        title = "Membre invité avec succès !"
        description = f"{self.infos[1]} a rejoint l'équipe  **__({self.infos[0]})__** !"
        color = discord.Colour.from_rgb(clr.red, clr.green, clr.blue)

        return discord.Embed(title = title, description = description, color = color)

class MatchmakingEvents:
    def __init__(self, infos: tuple | list = ()) -> None:
        self.infos = infos
    
    # Error
    def noTeam(self) -> discord.Embed:
        title = "Impossible d'effectuer l'action"
        description = "Il n'y a actuellement aucune équipe sur le serveur.\n:bulb: **__Créer une équipe:__ </team create:2000>**"
        color = discord.Colour.from_rgb(200, 0, 0)
         
        return discord.Embed(title = title, description = description, color = color)
    
    def gameNotStarted(self) -> discord.Embed:
        title = "Impossible d'effectuer l'action"
        description = "La partie n'a pas encore commencé, ou a été mise en pause par un administrateur.\n:bulb: **__Commencer une partie:__ Vous avez uniquement besoin de la permission `manageEvents` pour créer une partie.**"
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)
    
    def gameInTrainingMode(self) -> discord.Embed:
        title = "Impossible d'effectuer l'action"
        description = "La partie est en mode `Entraînement`, les fonctions de compétition comme le leaderboard ou les équipes sont desactivées."
        color = discord.Colour.from_rgb(255, 110, 0)

        return discord.Embed(title = title, description = description, color = color)
    
    def invalidGameMode(self) -> discord.Embed:
        title = "Impossible d'effectuer l'action"
        description = "## Modes acceptés:\n_ _\n**Non classé:** 2\n**Compétition:** 1\n**En pause:** 0"
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)
    
    def memberNotFound(self) -> discord.Embed:
        title = "Impossible d'effectuer l'action"
        description = f"Le membre **__{self.infos[0]}__** n'a pas pu être trouvé."
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)
    
    # Success
    def gameModeSet(self) -> discord.Embed:
        title = f"Mode de jeu basculé en mode `{'Non classé' if self.infos[0] == 2 else 'Compétition' if self.infos[0] == 1 else 'Arrêt'}`."
        description = "Le mode `Non classé` empêche la création d'équipe et désactive le leaderboard, tandis que le mode `Compétition` inclut toutes les fonctionnalités."
        color = discord.Colour.from_rgb(80, 200, 60)

        return discord.Embed(title = title, description = description, color = color)
    
    def memberBlacklisted(self) -> discord.Embed:
        title = f"{self.infos[0]} a bien été `{'ajouté' if self.infos[1] else 'retiré'}`."
        description = "Le membre sera incapable d'interagir avec le bot durant les parties (compétitions et parties non classées)"
        color = discord.Colour.from_rgb(80, 200, 60)

        return discord.Embed(title = title, description = description, color = color)

class GameEvents:
    def __init__(self, infos: tuple | list = ()) -> None:
        self.infos = infos

    # Error
    def invalidColor(self) -> discord.Embed:
        title = "Impossible de placer le pixel"
        description = "La couleur doit être sous le format RGB (sans les parenthèses).\n:bulb: **__Le format RGB:__ `(ROUGE, VERT, BLEU)` avec chaque nombre compris entre 0 et 255 inclus.**"
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)
    
    def invalidPixel(self) -> discord.Embed:
        title = "Impossible de placer le pixel"
        description = "Le pixel n'est pas valide. Un deuxième embed apparaîtra si la couleur est invalide."
        color = discord.Colour.from_rgb(200, 0, 0)

        return discord.Embed(title = title, description = description, color = color)
    
    # Success
    def placedPixel(self) -> discord.Embed:
        clr = self.infos[1]
        title = "Le pixel a été placé !"
        description = f"""**__Auteur__: `{self.infos[0]}`**\n**__Couleur__: `({clr.red}, {clr.green}, {clr.green})`**\n**__Emplacement__: `{chr(int(self.infos[2][0]) + 64)}-{self.infos[2][1]}`**"""
        color = discord.Colour.from_rgb(clr.red, clr.green, clr.blue)

        images.final(self.infos[3])
        map_attc = discord.File(open(f"lastmap.png", "rb"), filename = "map.png")

        embed = discord.Embed(title = title, description = description, color = color)
        embed.set_image(url = "attachment://map.png")

        return (embed, map_attc)

class Embed:
    def __init__(self, client: discord.Bot = None):
        self.client = client

    def teams(self, infos: tuple | list = ()) -> TeamEvents:
        return TeamEvents(tuple(infos))
    
    def matchMaking(self, infos: tuple | list = ()) -> MatchmakingEvents:
        return MatchmakingEvents(tuple(infos))
    
    def game(self, infos: tuple | list = ()) -> GameEvents:
        return GameEvents(tuple(infos))