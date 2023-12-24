import discord
import images
import utils

from PIL import ImageColor
from botinfos import colorScheme

error = colorScheme["error"]
success = colorScheme["success"]

class TeamEvents:
    def __init__(self, infos: tuple | list = ()) -> None:
        self.infos = infos
    
    # Errors
    def notExisting(self) -> discord.Embed:
        title = "<:member_error:1186272893286486087> Impossible de rejoindre l'équipe !"
        description = f"L'équipe **{self.infos[0]}** n'existe pas encore. Vous pouvez la créer dès maintenant avec la commande **</team create:1171236341695127582>**"
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)
    
    def notInvited(self) -> discord.Embed:
        title = "<:member_error:1186272893286486087> Impossible de rejoindre l'équipe."
        description = f"L'équipe **{self.infos[0]}** ne vous a pas invité. Demandez à son créateur de vous inviter."
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)

    def alreadyExisting(self) -> discord.Embed:
        title = "<:error:1186272869047603331> Impossible de créer l'équipe."
        description = f"L'équipe **{self.infos[0]}** existe déjà. \n> :bulb: **Astuce:** Sur ordinateur, tu peux appuyer sur la flèche du haut pour modifier ta commande."
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)

    def alreadyInTeam(self) -> discord.Embed:
        title = "<:error:1186272869047603331> Impossible de créer ou rejoindre l'équipe."
        description = f"Vous êtes déjà dans l'équipe **{self.infos[0]}**."
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)
    
    def inAnotherTeam(self) -> discord.Embed:
        title = "<:member_error:1186272893286486087> Impossible d'inviter le membre."
        description = f"{self.infos[1]} déjà dans l'équipe **{self.infos[0]}**."
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)
    
    def notInAnyTeam(self) -> discord.Embed:
        title = "<:error:1186272869047603331> Impossible d'effectuer l'action."
        description = "Vous n'avez pas d'équipe dans cette partie."
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)

    def colorAlreadyTaken(self) -> discord.Embed:
        title = "<:error:1186272869047603331> Impossible de créer l'équipe."
        description = f"La couleur `{self.infos[0].value}` est déjà prise.  \n> :bulb: **Astuce:** Sur ordinateur, tu peux appuyer sur la flèche du haut pour modifier ta commande."
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)

    def colorInvalid(self) -> discord.Embed:
        title = "<:error:1186272869047603331> Impossible de créer l'équipe."
        description = f"La couleur `{self.infos[0].value}` n'est pas dans le format demandé (hexadécimal).  \n> :bulb: **Astuce:** Sur ordinateur, tu peux appuyer sur la flèche du haut pour modifier ta commande."
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)

    
    # Success
    def teamCreated(self) -> discord.Embed:
        clr = ImageColor.getcolor(self.infos[1].value, "RGB")
        title = "<:team_success:1186280857212821536> L'équipe est créée !"
        description = f"L'équipe  **{self.infos[0]}** vient d'être créée !\n:bulb: **__Inviter un membre:__ </team invite:1165023654296436837>**"
        color = discord.Colour.from_rgb(*clr)

        return discord.Embed(title = title, description = description, color = color)
    
    def teamJoined(self) -> discord.Embed:
        clr = ImageColor.getcolor(self.infos[1].value, "RGB")
        title = "<:add_member:1186272821870084187> Vous avez rejoint l'équipe !"
        description = f"Tu viens de rejoindre l'équipe **{self.infos[0]}** !\n:bulb: **__Quitter l'équipe:__ </team leave:1165023654296436837>**"
        color = discord.Colour.from_rgb(*clr)

        return discord.Embed(title = title, description = description, color = color)
    
    def teamLeft(self) -> discord.Embed:
        clr = ImageColor.getcolor(self.infos[1].value, "RGB")
        title = "<:member_error:1186272893286486087> Vous avez quitté l'équipe !"
        description = f"Tu viens de quitter l'équipe **{self.infos[0]}** !\n:bulb: **__Rejoindre une autre équipe:__ </team join:1165023654296436837>**"
        color = discord.Colour.from_rgb(*clr)

        return discord.Embed(title = title, description = description, color = color)

    def teamDeleted(self) -> discord.Embed:
        clr = ImageColor.getcolor(self.infos[1].value, "RGB")
        title = "<:success:1186379716798730270> Équipe supprimée"
        description = f"Tu viens de supprimer l'équipe **{self.infos[0]}** !\n:bulb: **Astuce:** Tous les membres de cette équipe peuvent rejoindre une autre équipe."
        color = discord.Colour.from_rgb(*clr)

        return discord.Embed(title = title, description = description, color = color)

    def memberInvited(self) -> discord.Embed:
        clr = ImageColor.getcolor(self.infos[2].value, "RGB")
        title = "<:add_member:1186272821870084187> Nouvelle invitation"
        description = f"{self.infos[1]} peut désormais rejoindre l'équipe **{self.infos[0]}**"
        color = discord.Colour.from_rgb(*clr)

        return discord.Embed(title = title, description = description, color = color)

class MatchmakingEvents:
    def __init__(self, infos: tuple | list = ()) -> None:
        self.infos = infos
    
    # Error
    def noTeam(self) -> discord.Embed:
        title = "<:error:1186272869047603331> Impossible d'effectuer l'action"
        description = "Il n'y a actuellement aucune équipe sur le serveur.\n:bulb: **__Créer une équipe:__ </team create:1165023654296436837>**"
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))
         
        return discord.Embed(title = title, description = description, color = color)
    
    def gameNotStarted(self) -> discord.Embed:
        title = "<:error:1186272869047603331> Impossible d'effectuer l'action"
        description = "La partie n'a pas encore commencé, ou a été mise en pause par un administrateur.\n:bulb: **__Commencer une partie:__ Vous avez uniquement besoin de la permission `manageEvents` pour créer une partie.**"
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)
    
    def gameInTrainingMode(self) -> discord.Embed:
        title = "<:error:1186272869047603331> Impossible d'effectuer l'action"
        description = "La partie est en mode `Entraînement`, les fonctions de compétition comme le leaderboard ou les équipes sont desactivées."
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)
    
    def invalidGameMode(self) -> discord.Embed:
        title = "<:error:1186272869047603331> Impossible d'effectuer l'action"
        description = "## Modes acceptés:\n_ _\n**Non classé:** 2\n**Compétition:** 1\n**En pause:** 0"
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)
    
    def memberNotFound(self) -> discord.Embed:
        title = "<:error:1186272869047603331> Impossible d'effectuer l'action"
        description = f"Le membre **{self.infos[0]}** n'a pas pu être trouvé."
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)
    
    # Success
    def gameModeSet(self) -> discord.Embed:
        title = f"<:success:1186379716798730270> Mode de jeu basculé en mode `{'Non classé' if self.infos[0] == 2 else 'Compétition' if self.infos[0] == 1 else 'Arrêt'}`."
        description = "Le mode `Non classé` empêche la création d'équipe et désactive le leaderboard, tandis que le mode `Compétition` inclut toutes les fonctionnalités."
        color = discord.Colour.from_rgb(*ImageColor.getcolor(success, "RGB"))

        return discord.Embed(title = title, description = description, color = color)
    
    def memberBlacklisted(self) -> discord.Embed:
        title = f"<:add_member:1186272821870084187>Le membre a bien été {'ajouté' if self.infos[1] else 'retiré'}."
        description = f"<@{self.infos[0]}> sera incapable d'interagir avec le bot durant les parties (compétitions et parties non classées)"
        color = discord.Colour.from_rgb(*ImageColor.getcolor(success, "RGB"))

        return discord.Embed(title = title, description = description, color = color)

class GameEvents:
    def __init__(self, infos: tuple | list = ()) -> None:
        self.infos = infos

    # Error
    def invalidColor(self) -> discord.Embed:
        title = "<:error:1186272869047603331> Impossible de placer le pixel"
        description = "La couleur doit être sous le format RGB (sans les parenthèses).\n:bulb: **__Le format RGB:__ `(ROUGE, VERT, BLEU)` avec chaque nombre compris entre 0 et 255 inclus.**"
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)
    
    def invalidPixel(self) -> discord.Embed:
        title = "<:error:1186272869047603331> Impossible de placer le pixel"
        description = "Le pixel n'est pas valide. Un deuxième embed apparaîtra si la couleur est invalide."
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)
    
    def rateLimit(self) -> discord.Embed:
        title = "<:rate_limited:1186272917177249885> Impossible de placer le pixel."
        description = f"Vous pourrez placer un pixel <t:{self.infos[0]}:R>."
        color = discord.Colour.from_rgb(*ImageColor.getcolor(error, "RGB"))

        return discord.Embed(title = title, description = description, color = color)
    
    # Success
    def placedPixel(self) -> discord.Embed:
        clr = ImageColor.getcolor(self.infos[1].value, "RGB")
        title = "<:success:1186379716798730270> Le pixel a été placé."
        description = f"""**Auteur: `{self.infos[0]}`**\n**Couleur: `{clr}`**\n**Emplacement: `{chr(int(self.infos[2][0]) + 64)}-{self.infos[2][1]}`**"""
        color = discord.Colour.from_rgb(*ImageColor.getcolor(success, "RGB"))

        images.final(self.infos[3])
        map_attc = discord.File(open(f"lastmap.png", "rb"), filename = "map.png")

        embed = discord.Embed(title = title, description = description, color = color)
        embed.set_image(url = "attachment://map.png")

        return (embed, map_attc)
    
    def gif(self) -> discord.Embed:
        title = "<:success:1186379716798730270> Voici votre gif tant convoîté"
        description = f"""Partagez la partie avec vos amis !\n_Merci d'utiliser cette commande avec modération._""" # Phrase à garder ou non selon les performances et l'utilisation de votre machine
        color = discord.Colour.from_rgb(*ImageColor.getcolor(success, "RGB"))

        map_attc = discord.File(open(f"lastgif.gif", "rb"), filename = "gif.gif")

        embed = discord.Embed(title = title, description = description, color = color)
        embed.set_image(url = "attachment://gif.gif")

        return (embed, map_attc)