import discord
from discord.ext import commands
import sys


def main():
    token = sys.argv[1]
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="/", intents=intents)
    guild_gz = discord.Object(id=687998122777116707)  # Gaming Zone Guild Object

    @bot.event
    async def on_ready():
        await bot.tree.sync(guild=guild_gz)
        print(f"{bot.user} has connected to Discord")

    @bot.event
    async def on_message(message: discord.Message):
        if message.author == bot.user:
            return
        await bot.process_commands(message)

    @bot.tree.command(name="ping", guild=guild_gz)
    async def _ping(cxt: discord.Interaction):
        await cxt.response.send_message("Pong!")

    @bot.tree.command(name="add", guild=guild_gz)
    async def _add(cxt: discord.Interaction, a: int, b: int):
        await cxt.response.send_message(f"{a}+{b}={a + b}")

    bot.run(token)


if __name__ == "__main__":
    main()
