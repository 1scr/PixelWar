import discord
import dotenv
import glob
import io
import math
import os
import shutil

from PIL import Image

from deta import Deta

dotenv.load_dotenv()

deta = Deta(os.getenv("DATAKEY"))
games = deta.Base("games")
users = deta.Base("users")
saves = deta.Drive("saves")

bot = discord.Bot()

class Color:
	def __init__(self, value: str = "#ffffff"):
		self.value = value
	
	def is_valid(self) -> bool:
		for char in range(len(self.value)):
			if (char == 0 and self.value[char] != "#") or (char != 0 and self.value[char] not in "0123456789abcdef") or len(self.value) != 7:
				return False
		
		return True

class Stats:
	def __init__(self, attacks: int = 0, losses: int = 0, frequency: int = 0, pixels: int = 0):
		self.attacks = attacks
		self.losses = losses
		self.frequency = frequency
		self.pixels = pixels
	
	def strike(self) -> None:
		self.attacks = 0
		self.losses = 0
		self.frequency = 0
		self.pixels = 0
	
	def to_dict(self) -> dict:
		return { "attacks": self.attacks, "losses": self.losses, "frequency": self.frequency, "pixels": self.pixels }
	
	def update_from_dict(self, data: dict) -> None:
		if "attacks" in data.keys(): self.attacks = data["attacks"]
		if "losses" in data.keys(): self.losses = data["losses"]
		if "frequency" in data.keys(): self.frequency = data["frequency"]
		if "pixels" in data.keys(): self.pixels = data["pixels"]

class Pixel:
	def __init__(self, color: Color = Color(), position: tuple | list = ("M", "13"), author: int = 0):
		self.color = color
		self.position = "-".join([ str(ord(position[0]) - 64), position[1] ])
		self.author = author

		self.update_from_dict(self.to_dict())
	 
	def is_valid(self) -> bool:
		valid = True
		if type(self.color) == Color:
			valid = self.color.is_valid()
		else:
			valid = False

		for position in self.position.split("-"):
			for digit in position:
				if not digit.isdigit():
					valid = False

					break
			else:
				if not 1 <= int(position) <= 26:
					valid = False
		
		return valid
	
	def to_dict(self) -> dict[str | int]:
		return { "place": self.position, "color": self.color.value, "author": str(self.author) }
	
	def update_from_dict(self, data: dict):
		if "color" in data.keys(): self.color = Color(data["color"])
		if "place" in data.keys(): self.position = data["place"]
		if "author" in data.keys(): self.author = int(data["author"])

		if not self.is_valid(): self = Pixel()

class User:
	def __init__(self, id: int, stats: Stats = Stats(), isAdmin: bool = False, timestamp: int = 0):
		self.id = id
		self.stats = stats
		self.isAdmin = isAdmin
		self.timestamp = timestamp

		user = users.get(str(id))
		if user is None:
			users.put(key = str(id), data = self.to_dict())
		
		self.update_from_dict(self.to_dict())
	   
	def add_pixel(self, count: int = 1) -> None:
		self.stats.pixels += count
	
	def change_status(self, switch: bool = None) -> None:
		self.isAdmin = bool(1 - int(self.isAdmin)) if switch is None else switch
	
	def is_admin(self) -> bool:
		return self.isAdmin
	
	def get_score(self) -> float:
		pixels = self.stats.pixels
		attacks = self.stats.attacks
		losses = self.stats.losses
		return 3 * (math.floor(pixels) + 3.7 * math.floor(attacks)) / (math.floor(losses / 1.4) + 1) / (500 * (1 / math.floor(pixels + 1)))

	def to_dict(self) -> dict[str | int]:
		return {"id": str(self.id), "isAdmin": self.isAdmin, "stats": self.stats.to_dict(), "timestamp": str(self.timestamp)}
	
	def update_from_dict(self, data: dict) -> None:
		if "id" in data.keys(): self.id = int(data["id"])
		if "stats" in data.keys(): self.stats = data["stats"]
		if "isAdmin" in data.keys(): self.isAdmin = data["isAdmin"]
		if "timestamp" in data.keys(): self.timestamp = int(data["timestamp"])

		new_stats = Stats()
		new_stats.update_from_dict(self.stats)
		self.stats = new_stats

class Team:
	def __init__(self, name: str = "New Team", members: list[User] = [], pixels: int = 0, color: Color = Color(), invites: list = []):
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
	
	def set_color(self, color: Color) -> None:
		if color.is_valid():
			self.color = color
	
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


		if type(self.color) == Color:
			str_color = self.color.value
		else:
			str_color = self.color

		return {"name": self.name, "pixels": self.pixels, "color": str_color, "members": member_dicts, "invites": invites_str}

	def update_from_dict(self, data: dict) -> None:
		if "name" in data.keys(): self.name = data["name"]
		if "pixels" in data.keys(): self.pixels = data["pixels"]
		if "members" in data.keys(): self.members = data["members"]
		if "color" in data.keys(): self.color = Color(data["color"])
		if "invites" in data.keys(): self.invites = data["invites"] if data["invites"] is not None else []

		if self.members is None: self.members = []

		classified_members = []
		for user in self.members:
			if type(user) == dict:
				currentUser = User(user["id"])
				currentUser.update_from_dict(user)

				users.put(key = str(currentUser.id), data = currentUser.to_dict())

				classified_members.append(currentUser)
			elif type(user) == User:
				users.put(key = str(user.id), data = user.to_dict())
				
				classified_members.append(user)
		
		int_invites = []
		for user in self.invites:
			if type(user) == str:
				int_invites.append(user)
		
		self.invites = int_invites  
		self.members = classified_members

		if type(self.color) != Color:
			self.color = Color(self.color)
		
class Game:
	def __init__(self, id: int):
		self.id:int = id
		self.pixels: list[Pixel] = []
		self.teams: list[Team] = []
		self.status = 0
		self.blacklist = []
		self.saves = 0

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
			self.saves = game["saves"]

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
	
	def search_pixel(self, place: tuple) -> Pixel | None:
		self.update_from_dict(self.to_dict())
		
		for pixel in self.pixels:
			if tuple(pixel.position.split("-")) == place: return pixel
		
		return None
	
	def search_user(self, id: int) -> dict[User | Team] | None:
		for team in self.teams:
			for member in team.members:
				if id == member.id: return { "user": member, "team": team }
		
		return None
	
	def generate_gif(self):
		os.mkdir("gif_preview")

		i = 0
		for image in saves.list(prefix = str(self.id))["names"]:
			image_bytes = saves.get(image).read()
			_image = Image.open(io.BytesIO(image_bytes))
			_image.save(f"gif_preview/image_{i}.png")
			i += 1
	
		frames = [ Image.open(image) for image in glob.glob(f"gif_preview/*.PNG") ]
		frame_one = frames[0]
		frame_one.save("lastgif.gif", format = "GIF", append_images = frames, save_all = True, duration = 100, loop = 0)

		shutil.rmtree("gif_preview")

	def save_image(self, image: bytes):
		saves.put(data = image, name = f"{self.id}_{self.saves + 1}")
		self.saves += 1

		self.save()

	def to_dict(self) -> dict[str | list]:
		team_dicts = []
		pixel_dicts = []

		for team in self.teams:
			if type(team) == dict:
				currentTeam = Team()
				currentTeam.update_from_dict(team)
				team_dicts.append(currentTeam.to_dict())
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

		return {"id": str(self.id), "pixels": pixel_dicts, "teams": team_dicts, "gameStatus": self.status, "blacklist": str_bl, "saves": self.saves}
	
	def update_from_dict(self, data: dict):
		if "pixels" in data.keys(): self.pixels = data["pixels"]
		if "teams" in data.keys(): self.teams = data["teams"]
		if "gameStatus" in data.keys(): self.status = data["gameStatus"]
		if "blacklist" in data.keys(): self.blacklist = data["blacklist"]
		if "saves" in data.keys(): self.saves = data["saves"]

		classified_pixels = []
		for pixel in self.pixels:
			if type(pixel) == dict:
				currentPixel = Pixel()
				currentPixel.update_from_dict(pixel)

				classified_pixels.append(currentPixel)
			elif type(pixel) == Pixel:
				classified_pixels.append(pixel)

		classified_teams = []
		for team in self.teams:
			if type(team) == dict:
				currentTeam = Team()
				currentTeam.update_from_dict(team)

				classified_teams.append(currentTeam)
			elif type(team) == Team:
				classified_teams.append(team)
		
		int_blacklist = []
		for id in self.blacklist:
			if type(id) == str:
				int_blacklist.append(int(id))

		self.teams = classified_teams
		self.pixels = classified_pixels
		self.blacklist = int_blacklist
		
	def save(self) -> None:
		games.update(key = str(self.id), updates = self.to_dict())