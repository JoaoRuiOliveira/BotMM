import discord
from discord.ext import commands
import json
import os

# Função para carregar as filas dos jogadores a partir de um ficheiro JSON
def load_queues():
    if not os.path.exists('data/queues.json'):
        return {}
    with open('data/queues.json', 'r') as f:
        return json.load(f)

# Função para guardar as filas de jogadores no ficheiro JSON
def save_queues(queues_data):
    with open('data/queues.json', 'w') as f:
        json.dump(queues_data, f, indent=4)

# Função para criar novas filas (caso ainda não existam)
def create_queue_if_not_exists(queues_data, game):
    if game not in queues_data:
        queues_data[game] = []
    return queues_data

class Matchmaking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues_data = load_queues()

    @commands.command()
    async def queue(self, ctx, game: str):
        """Adicionar um jogador à fila de espera para um jogo específico."""
        user = ctx.author
        game = game.lower()

        # Cria a fila se não existir
        self.queues_data = create_queue_if_not_exists(self.queues_data, game)

        # Verifica se o jogador já está na fila
        if user.id in self.queues_data[game]:
            await ctx.send(f'{user.name}, já estás na fila para {game}.')
            return

        # Adiciona o jogador à fila
        self.queues_data[game].append(user.id)
        save_queues(self.queues_data)

        await ctx.send(f'{user.name} entrou na fila para jogar {game}!')

        # Se houver jogadores suficientes, organiza uma partida
        if len(self.queues_data[game]) >= 10:  # Exemplo: 10 jogadores para LoL
            await self.organize_match(ctx, game)

    @commands.command()
    async def leave_queue(self, ctx, game: str):
        """Remover um jogador da fila."""
        user = ctx.author
        game = game.lower()

        # Verifica se a fila existe
        if game not in self.queues_data or user.id not in self.queues_data[game]:
            await ctx.send(f'{user.name}, não estás na fila para {game}.')
            return

        # Remove o jogador da fila
        self.queues_data[game].remove(user.id)
        save_queues(self.queues_data)

        await ctx.send(f'{user.name} saiu da fila para {game}.')

    async def organize_match(self, ctx, game):
        """Organiza uma partida quando houver jogadores suficientes na fila."""
        players_in_queue = self.queues_data[game][:10]  # Pega os 10 primeiros jogadores

        # Remove os jogadores da fila
        self.queues_data[game] = self.queues_data[game][10:]
        save_queues(self.queues_data)

        # Organiza as equipas
        team_1 = players_in_queue[:5]  # Exemplo: 5 jogadores para a equipa 1
        team_2 = players_in_queue[5:]  # 5 jogadores para a equipa 2

        # Envia as mensagens com as equipas
        team_1_names = [str(ctx.guild.get_member(player_id)) for player_id in team_1]
        team_2_names = [str(ctx.guild.get_member(player_id)) for player_id in team_2]

        await ctx.send(f'Partida organizada para {game}!\n\n'
                       f'Equipa 1: {", ".join(team_1_names)}\n'
                       f'Equipa 2: {", ".join(team_2_names)}')

async def setup(bot):
    await bot.add_cog(Matchmaking(bot))