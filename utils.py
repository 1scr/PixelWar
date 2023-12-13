import discord
import dotenv
import logging
import os

from deta import Deta

dotenv.load_dotenv()

deta = Deta(os.getenv("DATAKEY"))
games = deta.Base("games")

bot = discord.Bot()

class RGB:
    def __init__(self, red: int = 255, green: int = 180, blue: int = 75):
        self.red = red
        self.green = green
        self.blue = blue
    
    def is_valid(self) -> bool:
        color = (self.red, self.green, self.blue)
        color_set = range(256)

        valid = True
        for level in color:
            if type(level) not in (float, int):
                valid = False
                break

            if not level in color_set:
                valid = False
                break
        
        return valid

class Pixel:
    def __init__(self, color: RGB = RGB(), position: tuple | list = ("M", "13")):
        self.color = color
        self.position = [ str(ord(position[0]) - 64), position[1] ]

        self.update_from_dict(self.to_dict())
     
    def is_valid(self) -> bool:
        if type(self.color) == RGB:
            valid = self.color.is_valid()
        else:
            valid = RGB(self.color[0], self.color[1], self.color[2]).is_valid()


        for position in self.position:
            for digit in position:
                if not digit.isdigit():
                    valid = False

                    break
            else:
                if not 1 <= int(position) <= 26:
                    valid = False
        
        return valid
    
    def to_dict(self) -> dict[str | int]:
        color = [self.color.red, self.color.green, self.color.blue]
        return {"place":self.position, "color": color}
    
    def update_from_dict(self, data: dict):
        if "color" in data.keys(): self.color = RGB(data["color"][0], data["color"][1], data["color"][2])
        if "place" in data.keys(): self.position = data["place"]

        if not self.is_valid(): self = Pixel()
    

class User:
    def __init__(self, id: int, pixels: int = 0, isAdmin: bool = False):
        self.id = id
        self.pixels = pixels
        self.isAdmin = isAdmin
        user = bot.get_user(id)

        self.username = user.name if type(user) in [discord.User, discord.Member] else "Unknown user"
       
    def add_pixel(self, count: int = 1) -> None:
        self.pixels += count
    
    def change_status(self, switch: bool = None) -> None:
        self.isAdmin = bool(1 - int(self.isAdmin)) if switch is None else switch
    
    def is_admin(self) -> bool:
        return self.isAdmin

    def to_dict(self) -> dict[str | int]:
        return {"id": str(self.id), "username": self.username, "isAdmin": self.isAdmin, "pixels": self.pixels}
    
    def update_from_dict(self, data: dict) -> None:
        if "id" in data.keys(): self.id = int(data["id"])
        if "username" in data.keys(): self.username = data["username"]
        if "pixels" in data.keys(): self.pixels = data["pixels"]
        if "isAdmin" in data.keys(): self.isAdmin = data["isAdmin"]

class Team:
    def __init__(self, name: str = "New Team", members: list[User] = [], pixels: int = 0, color: RGB = RGB(), invites: list = []):
        self.name = name
        self.members = members
        self.pixels = pixels
        self.color = color
        self.invites = invites

        self.update_from_dict(self.to_dict())
    
    def add_member(self, member: User) -> None:
        self.members.append(member)

    def add_pixel(self, count: int = 1) -> None:
        self.pixels += count

    def invite(self, id: int) -> None:
        self.invites.append(id)
    
    def set_color(self, color: RGB) -> None:
        if color.is_valid():
            self.color = color
        else:
            logging.exception(f"RGB color {(color.red, color.green, color.blue)} is not valid.")
    
    def to_dict(self) -> dict[str | list]:
        member_dicts = []
        for member in self.members:
            if type(member) == dict:
                member_dicts.append(member)
            elif type(member) == User:
                member_dicts.append(member.to_dict())
        
        invites_str = []
        for id in self.invites:
            if type(id) == str:
                invites_str.append(id)
            elif type(id) == int:
                invites_str.append(str(id))

        self.members = member_dicts
        self.invites = invites_str
                        
        if type(self.color) == dict:
            self.color = [self.color["red"], self.color["green"], self.color["blue"]]

        if type(self.color) == RGB:
            self.color = [self.color.red, self.color.green, self.color.blue]

        return {"name": self.name, "pixels": self.pixels, "color": self.color, "members": self.members, "invites": self.invites}

    def update_from_dict(self, data: dict) -> None:
        if "name" in data.keys(): self.name = data["name"]
        if "pixels" in data.keys(): self.pixels = data["pixels"]
        if "members" in data.keys(): self.members = data["members"]
        if "color" in data.keys(): self.color = data["color"]
        if "invites" in data.keys(): self.invites = data["invites"] if data["invites"] is not None else []


        classified_members = []
        for user in self.members:
            if type(user) == dict:
                currentUser = User(user["id"])
                currentUser.update_from_dict(user)

                classified_members.append(currentUser)
            elif not type(user) == User:
                logging.error(f"User {user} is neither {type(User)} nor {type({})}.")
        
        int_invites = []
        for user in self.invites:
            if type(user) == str:
                int_invites.append(user)
        
        self.invites = int_invites  
        self.members = classified_members

        if type(self.color) != RGB:
            self.color = RGB(self.color[0], self.color[1], self.color[2])
        
class Game:
    def __init__(self, id: int):
        self.id:int = id
        self.pixels: list[Pixel] = []
        self.teams: list[Team] = []
        self.status = 0
        self.blacklist = []

        # 0 = Paused
        # 1 = Competition
        # 2 = Training

        game = games.get(str(id))
        if game is None:
            games.put(key = str(id), data = self.to_dict())
        else:
            self.teams = game["teams"]
            self.pixels = game["pixels"]
            self.status = game["gameStatus"]
            self.blacklist = game["blacklist"]

        self.update_from_dict(self.to_dict())
    
    def add_team(self, team: Team) -> None:
        self.teams.append(team.to_dict())
        self.update_from_dict(self.to_dict())
    
    def remove_team(self, team: Team) -> None:
        if team.to_dict() in self.teams:
            self.teams.remove(team.to_dict())
        self.update_from_dict(self.to_dict())
    
    def add_pixel(self, pixel: Pixel) -> None:
        if pixel.is_valid(): self.pixels.append(pixel)
        self.update_from_dict(self.to_dict())
    
    def remove_pixel(self, pixel: Pixel) -> None:
        if pixel.to_dict() in self.pixels:
            self.pixels.remove(pixel.to_dict())
        self.update_from_dict(self.to_dict())
    
    def to_dict(self) -> dict[str | list]:
        team_dicts = []
        pixel_dicts = []

        for team in self.teams:
            if type(team) == dict:
                team_dicts.append(team)
            elif type(team) == Team:
                team_dicts.append(team.to_dict())
        
        for pixel in self.pixels:
            if type(pixel) == dict:
                pixel_dicts.append(pixel)
            elif type(pixel) == Pixel:
                pixel_dicts.append(pixel.to_dict())
        
        str_bl = []
        for user in self.blacklist:
            str_bl.append(str(user))

        return {"id": str(self.id), "pixels": pixel_dicts, "teams": team_dicts, "gameStatus": self.status, "blacklist": str_bl}
    
    def update_from_dict(self, data: dict):
        if "pixels" in data.keys(): self.pixels = data["pixels"]
        if "teams" in data.keys(): self.teams = data["teams"]
        if "gameStatus" in data.keys(): self.status = data["gameStatus"]
        if "blacklist" in data.keys(): self.blacklist = data["blacklist"]

        classified_teams = []
        for team in self.teams:
            if type(team) == dict:
                currentTeam = Team()
                currentTeam.update_from_dict(team)

                classified_teams.append(currentTeam)
            elif not type(team) == Team:
                logging.error(f"Team {team} is neither {type(Team)} nor {type({})}.")
                break
        
        classified_pixels = []
        for pixel in self.pixels:
            if type(pixel) == dict:
                px = Pixel()
                px.update_from_dict(pixel)

                classified_pixels.append(px)
            elif not type(pixel) == Pixel:
                logging.error(f"Pixel {pixel} is neither {type(Pixel)} nor {type({})}.")
                break
        
        int_blacklist = []
        for id in self.blacklist:
            if type(id) == str:
                int_blacklist.append(int(id))


        self.teams = classified_teams
        self.pixels = classified_pixels
        self.blacklist = int_blacklist
        
    def save(self) -> None:
        games.update(key = str(self.id), updates = self.to_dict())