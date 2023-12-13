import dotenv
import os
import random

from deta import Deta
import discord

import botinfos
import embeds
import utils

dotenv.load_dotenv()

deta = Deta(os.getenv("DATAKEY"))

bot = discord.Bot(description = botinfos.description)
team = bot.create_group(name = "team", description = "Commandes liées aux équipes")
pixel = bot.create_group(name = "map", description = "Commandes liées à la map")
matchmaking = bot.create_group(name = "game", description = "Commandes liées à la partie")

embed = embeds.Embed(bot)

baseTeam = utils.Team()

global testMode
testMode = False

@bot.event
async def on_ready():
	print("Ready !")
	print("Connected as", bot.user)

@matchmaking.command(name = "mode", description = "Changer le mode de jeu")
@discord.default_permissions(manage_events = True)
async def gamemode(ctx: discord.ApplicationContext, mode: int):
	if 0 <= mode <= 2:
		game = utils.Game(ctx.channel.id)
		game.status = mode
		game.save()

		await ctx.send_response(embed = embed.matchMaking(( mode, )).gameModeSet())
	else:
		await ctx.send_response(embed = embed.matchMaking().invalidGameMode())

@matchmaking.command(name = "blacklist-set", description = "Gérer la blacklist")
@discord.default_permissions(manage_events = True)
async def manage_bl(ctx: discord.ApplicationContext, member: discord.Member, blacklisted: bool = True):
	if member is None:
		await ctx.send_response(embed = embed.matchMaking(( member.name, )).memberNotFound())
	else:
		game = utils.Game(ctx.channel.id)
		if blacklisted:
			if member.id not in game.blacklist: game.blacklist.append(str(member.id))
		else:
			if member.id in game.blacklist: game.blacklist.remove(str(member.id))
			
		game.save()
		await ctx.send_response(embed = embed.matchMaking(( member.name, blacklisted )).memberBlacklisted())
	
@matchmaking.command(name = "show-blacklist", description = "Montrer la blacklist")
@discord.default_permissions(manage_events = True)
async def show_bl(ctx: discord.ApplicationContext):
	game: utils.Game = utils.Game(ctx.channel.id)
	blacklist: list[str] = game.blacklist

	if len(blacklist) == 0:
		description = """```\nIl n'y a pas de membre blacklisté actuellement.\n```
		"""
	else:
		description = f"""```\nIl y a {len(blacklist)} membre{'s' if len(blacklist) > 1 else ''} blacklisté{'s' if len(blacklist) > 1 else ''}:\n"""

		for id in blacklist:
			member = await bot.fetch_user(int(id))
			name = member.name if type(member) == discord.User else "Inconnu"
			
			description += f"\n{id} ({name})"
		
		description += "\n```"
		
	bl_embed = discord.Embed(title = "Blacklist de la partie", description = description, color = discord.Colour.from_rgb(0, 100, 255))
	
	await ctx.send_response(embed = bl_embed)

@matchmaking.command(name = "leaderboard")
async def leaderboard(ctx: discord.ApplicationContext, maximum: int | None = 5):
	game: utils.Game = utils.Game(ctx.channel.id)

	teams = game.teams
	members: list[utils.User] = []

	if game.status != 1:
		if game.status == 0:
			await ctx.send_response(embed = embed.matchMaking().gameNotStarted())
		else:
			await ctx.send_response(embed = embed.matchMaking().gameInTrainingMode())
		return

	for team in teams:
		members.extend(team.members)

	if maximum == 0 or maximum > len(members): maximum = len(members)
	
	title = f"Top {maximum} de la partie"
	if len(members) == 0:
		description = "Aucun pixel n'a été placé."
	else:
		members.sort(key = lambda member : -member.pixels)
		description = ":warning: Le nombre de pixels inclut également les pixels volés ou placés plusieurs fois, et la fiabilité du classement peut donc être compromise.\n"
		
		slot = 0
		while slot < maximum:
			member = await bot.fetch_user(int(members[slot].id))
			description += f"""\n**{':first_place:' if slot == 0 else ':second_place:' if slot == 1 else ':third_place:' if slot == 2 else ':medal:'} | <@{member.id}> - {members[slot].pixels} pixel{'s' if members[slot].pixels > 1 else ''}**"""
			slot += 1

	await ctx.send_response(embed = discord.Embed(title = title, description = description, color = discord.Colour.from_rgb(50, 100, 255)))

@team.command(name = "create", description = "Créer une équipe")
async def create(ctx: discord.ApplicationContext, name: str, color: str) -> None:
	color: list | tuple = color.split(",")
	color = [int(clr) for clr in color]
	color = tuple(color)

	game = utils.Game(ctx.channel.id)
	teams = game.teams

	if str(ctx.author.id) in game.blacklist: return

	if game.status != 1:
		if game.status == 0:
			await ctx.send_response(embed = embed.matchMaking().gameNotStarted())
		else:
			await ctx.send_response(embed = embed.matchMaking().gameInTrainingMode())
		return

	teamNames = [team.name for team in teams]
	teamColors = [team.color for team in teams]

	user = utils.User(ctx.author.id, 0, True)

	for team in teams:
		for member in team.members:
			if member.id == user.id:
				await ctx.send_response(embed = embed.teams(( team.name, )).alreadyInTeam())
				return
	
	if len(color) != 3 or not utils.RGB(color[0], color[1], color[2]).is_valid():
		await ctx.send_response(embed = embed.teams(( color, )).colorInvalid())
	elif name in teamNames or color in teamColors:
		if color in teamColors:
			await ctx.send_response(embed = embed.teams(( color, )).colorAlreadyTaken())
		else:
			await ctx.send_response(embed = embed.teams(( team.name, )).alreadyExisting())
	else:
		newTeam: utils.Team = utils.Team(name, [ user ], 0, color, [ str(user.id) ])

		teams.append(newTeam)
		game.teams = teams
		game.save()
		await ctx.send_response(embed = embed.teams(( name, color )).teamCreated())

@team.command(name = "leave", description = "Quitter ou supprimer une équipe")
async def leave(ctx: discord.ApplicationContext):
	game = utils.Game(ctx.channel.id)
	teams: list[utils.Team] = game.teams

	if str(ctx.author.id) in game.blacklist: return

	user: utils.User = utils.User(ctx.author.id)

	if game.status != 1:
		if game.status == 0:
			await ctx.send_response(embed = embed.matchMaking().gameNotStarted())
		else:
			await ctx.send_response(embed = embed.matchMaking().gameInTrainingMode())
		return

	if len(teams) == 0:
		await ctx.send_response(embed = embed.matchMaking().noTeam())
		return

	for team in teams:
		broke = False
		if team.pixels is None: team.pixels = 0
	
		for member in team.members:
			if member.id == user.id:
				if member.is_admin():
					teams.remove(team)
					await ctx.send_response(embed = embed.teams(( team.name, team.color )).teamDeleted())
				else:
					team.members.remove(member)
					await ctx.send_response(embed = embed.teams(( team.name, team.color )).teamLeft())

				broke = True
				break
		if broke: break
	else:
		await ctx.send_response(embed.teams(( team.name, )).notInvited())
		return

	game.teams = teams
	game.save()

@team.command(name = "invite", description = "Inviter un joueur dans son équipe")
async def invite(ctx: discord.ApplicationContext, member: discord.Member):
	game = utils.Game(ctx.channel.id)
	teams: list[utils.Team] = game.teams

	if str(ctx.author.id) in game.blacklist: return

	if game.status != 1:
		if game.status == 0:
			await ctx.send_response(embed = embed.matchMaking().gameNotStarted())
		else:
			await ctx.send_response(embed = embed.matchMaking().gameInTrainingMode())
		return

	if len(teams) == 0:
		await ctx.send_response(embed = embed.matchMaking().noTeam())
		return

	user = utils.User(ctx.author.id, isAdmin = True)

	currentTeam: utils.Team | None = None
	teamIndex: int | None = None

	broke = False
	for team in teams:
		for teamMember in team.members:
			if teamMember.id == user.id and teamMember.is_admin():
				currentTeam = team
				teamIndex = teams.index(team)

				broke = True
				break
		if broke: break
	else:
		await ctx.send_response(embed = embed.teams().notInAnyTeam())
		return

	currentTeam.invite(member.id)

	teams[teamIndex] = currentTeam
	game.teams = teams
	game.save()

	await ctx.send_response(embed = embed.teams(( team.name, member.name, team.color )).memberInvited())

@team.command(name = "join", description = "Rejoindre une équipe")
async def join(ctx: discord.ApplicationContext, name: str):
	game = utils.Game(str(ctx.channel.id))
	teams: list[utils.Team] = game.teams

	if str(ctx.author.id) in game.blacklist: return

	if game.status != 1:
		if game.status == 0:
			await ctx.send_response(embed = embed.matchMaking().gameNotStarted())
		else:
			await ctx.send_response(embed = embed.matchMaking().gameInTrainingMode())
		return

	if len(teams) == 0:
		await ctx.send_response(embed = embed.matchMaking().noTeam())
		return

	user = utils.User(ctx.author.id) 
	currentTeam: utils.Team | None = None
	teamIndex: int | None = None

	for team in teams:
		if team.name == name: 
			currentTeam = team
			teamIndex = teams.index(team)
			break
		
		for member in team.members:
			if member.id == user.id:
				await ctx.send_response(embed = embed.teams(( team.name, )).alreadyInTeam())
				return
	else:
		await ctx.send_response(embed = embed.teams(( name, )).notExisting())
		return

	if type(currentTeam.invites) != list or str(user.id) not in currentTeam.invites:
		await ctx.send_response(embed = embed.teams(( currentTeam.name, )).notInvited())
		return
	
	if currentTeam.members is None:
		user.isAdmin = True
		currentTeam.members = []
	
	currentTeam.add_member(user)
	currentTeam.invites.remove(str(user.id))

	teams[teamIndex] = currentTeam
	game.teams = teams
	game.save()

	if currentTeam.pixels is None: currentTeam.pixels = []
	await ctx.send_response(embed = embed.teams(( currentTeam.name, currentTeam.color )).teamJoined())

@pixel.command(name = "place", description = "Placer un pixel")
async def place(ctx: discord.ApplicationContext, place: str, color: str | None = None):
	game = utils.Game(ctx.channel.id)
	teams: list[utils.Team] = game.teams

	if str(ctx.author.id) in game.blacklist: return

	if game.status != 1:
		if game.status == 0:
			await ctx.send_response(embed = embed.matchMaking().gameNotStarted())
			return
		else:
			chanMembers = ctx.channel.members
			currentTeam = baseTeam

			for member in chanMembers:
				currentTeam.add_member(utils.User(member.id))
			
			if len(currentTeam.members) == 0:
				currentTeam.members.append(utils.User(ctx.author.id))
			
			currentTeam.invites = []

			teams.clear()
			game.save()
			teams.append(currentTeam)
	
	if color is None:
		color = "0, 0"
	
	place: list[str] = place.split("-")
	color: list[str] = [ clr.replace(" ", "") for clr in color.split(",") ]
	color: list[int] = [ int(clr) for clr in color if clr.isnumeric() ]
	
	for team in teams:
		member_found = False    

		for member in team.members:
			if member.id == ctx.author.id:
				member.add_pixel()
				member_index = team.members.index(member)
				team.members[member_index] = member

				currentTeam = team
				team_index = teams.index(team)

				if len(color) != 3: color = team.color
				
				member_found = True
				break
		
		if member_found:
			break
	else:
		await ctx.send_response(embed = embed.teams().notInAnyTeam())
		return
	
	if type(color) != utils.RGB:
		color: utils.RGB = utils.RGB(color[0], color[1], color[2])

	if not color.is_valid():
		await ctx.send_response(embed = embed.game().invalidPixel())
		await ctx.send(embed = embed.game().invalidColor())
		return
	
	px = utils.Pixel(color, place)
	if not px.is_valid():
		await ctx.send_response(embed = embed.game().invalidPixel())
		return
	
	currentTeam.add_pixel()
	game.add_pixel(px)
	game.teams[team_index] = currentTeam
	game.save()

	message = embed.game(( ctx.author.name, px.color, px.position, ctx.channel.id )).placedPixel()

	if not testMode: await ctx.send_response(embed = message[0], file = message[1])

bot.run(os.getenv("TOKEN"))