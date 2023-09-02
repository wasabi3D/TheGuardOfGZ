import discord
from discord.ext import commands as dcmd
import botcmd
import servstats
import sys



def main():
    token = sys.argv[1]
    intents = discord.Intents.all()
    bot = dcmd.Bot(command_prefix="/", intents=intents)
    guild_gz = discord.Object(id=687998122777116707)  # Gaming Zone Guild Object


    @bot.event
    async def on_message(message: discord.Message):
        if message.author == bot.user:
            return
        servstats.onMessage(message)
        await bot.process_commands(message)

    @bot.event
    async def on_voice_state_update(member: discord.member, before: discord.VoiceState, after: discord.VoiceState):
        servstats.onVoiceStateChange(member, before, after)

    @bot.event
    async def on_ready():
        await bot.tree.sync(guild=guild_gz)
        servstats.onReady(bot, guild_gz.id)
        print(f"{bot.user} has connected to Discord")

    botcmd.registerCommands(bot, guild_gz)

    bot.run(token)
    servstats.save(force=True)


if __name__ == "__main__":
    main()
