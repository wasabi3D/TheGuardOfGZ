import discord
import sys


def main():
    token = sys.argv[1]
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to Discord")

    @client.event
    async def on_message(message: discord.Message):
        if message.author == client.user:
            return

        await message.channel.send("Hello!")

    print(token, type(token))
    client.run(token)


if __name__ == "__main__":
    main()
