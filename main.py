import discord
from discord.ext import commands
from discord_buttons_plugin import *
import os


channel_id = ""
player_name_score = {}
num_players = 0
num_players_selected = 0
game_started = False
round_started = False
selections = {
	"one" : [],
	"three" : [],
	"five" : []
}


client = commands.Bot(command_prefix = ".")
buttons = ButtonsClient(client)


@client.event
async def on_ready():
	print("Strategy Bots is ready")


@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("No such command")


async def reset():
	global game_started, round_started, num_players, num_players_selected, player_name_score, selections, channel_id
	game_started = False
	round_started = False
	num_players = 0
	num_players_selected = 0
	player_name_score.clear()
	selections["one"].clear()
	selections["three"].clear()
	selections["five"].clear()
	channel_id = None


def add_scores(vote, up, embed : discord.Embed):
	if len(selections[vote]) == 1:
		player_name_score[selections[vote][0]] += up
		embed.description += str(selections[vote][0] + " has moved up " + str(up) + " step")
		if vote == "three" or vote == "five":
			embed.description += "s"
		embed.description += "\n"


def check_winners():
	winners = []
	for key, value in player_name_score.items():
		if value >= 10:
			winners.append(str(key))
	if winners:
		return winners
	else:
		return None


async def end_round(ctx):
	global round_started, num_players_selected, selections
	round_started = False
	num_players_selected = 0
	embed1 = discord.Embed(title = "All Votes", description = "", color = 0x0000FF)
	for key, value in selections.items():
		for name in value:
			embed1.description += str(name + " chose " + key + "\n")
	embed2 = discord.Embed(title = "Unique Votes", description = "", color = 0x0000FF)
	add_scores("one", 1, embed2)
	add_scores("three", 3, embed2)
	add_scores("five", 5, embed2)
	if embed2.description == "":
		embed2.description = "No one had a unqiue vote"
	embed3 = discord.Embed(title = "Current Scores", description = "", color = 0x0000FF)
	for key, value in player_name_score.items():
		embed3.description += str(key + " is on step " + str(value) + "\n")
	await ctx.channel.send(embed = embed1)
	await ctx.channel.send(embed = embed2)
	await ctx.channel.send(embed = embed3)
	selections["one"].clear()
	selections["three"].clear()
	selections["five"].clear()
	winners = check_winners()
	if winners is not None:
		embed4 = discord.Embed(title = "Game Over", description = "", color = 0x0000FF)
		for win in winners:
			embed4.description += str(win + " has won the game\n")
			await ctx.channel.send(embed = embed4)
		await reset()


async def add_vote(ctx, vote):
	global round_started, selections, num_players_selected
	if round_started:
		username = ctx.member.name
		if username not in selections[vote]:
			num_players_selected += 1
		if username in player_name_score:
			selections[vote].append(username)
		await ctx.reply(content = f"{vote} clicked", flags = MessageFlags().EPHEMERAL)
		if num_players_selected == num_players:
			await end_round(ctx)
			

@buttons.click
async def one_clicked(ctx):
	await add_vote(ctx, "one")


@buttons.click
async def three_clicked(ctx):
	await add_vote(ctx, "three")


@buttons.click
async def five_clicked(ctx):
	await add_vote(ctx, "five")
			

@client.command()
async def start(ctx, *args : discord.Member):
	global game_started, num_players, channel_id
	if len(args) == 0:
		await ctx.send("Please enter more players")
		return
	if not game_started:
		channel_id = ctx.channel.id
		game_started = True
		embed_description = []
		for arg in args:
			arg = str(arg)
			arg = arg[:-5]
			player_name_score[arg] = 0
			embed_description.append(arg)
		num_players = len(player_name_score)
		embed = discord.Embed (
			title = "Players",
			description = "\n".join(embed_description),
			color = 0x0000FF
		)
		await ctx.send(embed = embed)
	else:
		await ctx.send("Game in progress")


@client.command()
async def next(ctx):
	global game_started, round_started
	if game_started:
		if ctx.channel.id != channel_id:
			await ctx.send("Game in progress")
		elif round_started:
			await ctx.send("Round in progress")
		else:
			round_started = True
			embed = discord.Embed(title = "Choose a vote", color = 0x0000FF)
			await buttons.send(embed = embed, channel = ctx.channel.id, components = [
				ActionRow([
					Button(label = "1", custom_id = "one_clicked"),
					Button(label = "3", custom_id = "three_clicked"),
					Button(label = "5", custom_id = "five_clicked")
				])
			])
	else:
		await ctx.send("Game has not started")


@client.command()
async def end(ctx):
	global game_started
	if game_started and ctx.channel.id == channel_id:
		await ctx.send("Game has ended")
		await reset()
	else:
		await ctx.send("No game to end")


folder = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(folder, "token.txt")
with open(my_file, "r") as file:
	token = file.readline()
	file.close()
	client.run(token)
