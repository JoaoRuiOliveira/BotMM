import discord
from discord.ext import commands
from discord import app_commands
import json
import os


def load_players():
    if not os.path.exists('data/players.json'):
        return {}
    with open('data/players.json', 'r') as f:
        return json.load(f)
    
def save_players(players_data):
    with open('data/players.json', 'w') as f:
        json.dump(players_data, f, indent=4)


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players_data = load_players()


    # register = registar um jogador
    @app_commands.command(name='register', description='Registar um jogador')
    @app_commands.describe(
        elo='O elo do jogador' 
    )
    async def register(self, interaction: discord.Interaction, elo: int = 1500):
        user = interaction.user
        user_id = str(user.id)

        if user_id in self.players_data:
            await interaction.response.send_message(f'{user.name} já está registado!')
            return
        
        self.players_data[user_id] = {
            'name': user.name,
            'elo': elo
        }

        save_players(self.players_data)
        await interaction.response.send_message(f'{user.name} registado com sucesso! ELO: {elo}')

    # myelo = ver o elo do jogador
    @commands.command()
    async def myelo(self, ctx):
        user = ctx.author
        user_id = str(user.id)

        if user_id not in self.players_data:
            await ctx.send(f'{user.name} não está registado!')
            return

        elo = self.players_data[user_id]['elo']
        await ctx.send(f'{user.name} tem {elo} de elo')

async def setup(bot):
    await bot.add_cog(Player(bot))