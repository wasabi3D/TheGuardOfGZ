import discord
from discord.ext import commands
from discord.utils import get
import servstats


def registerCommands(bot: commands.Bot, guild_gz: discord.Object):
    @bot.tree.command(name="ping", guild=guild_gz)
    async def _ping(cxt: discord.Interaction):
        await cxt.response.send_message("Pong!")

    @bot.tree.command(name="add", guild=guild_gz)
    async def _add(cxt: discord.Interaction, a: int, b: int):
        await cxt.response.send_message(f"{a}+{b}={a + b}")

    @bot.tree.command(name="curweek", guild=guild_gz)
    async def _curweek(cxt: discord.Interaction):
        await cxt.response.send_message(servstats.getCurrentWeekID())

    @bot.tree.command(name="msgcount", guild=guild_gz)
    async def _messagecount(cxt: discord.Interaction, year: int, week: int):
        stats = servstats.getStats(year, week)
        if stats is None:
            await cxt.response.send_message(
                "Statistics for that week are not available."
            )
            return

        processed_stats = []
        if cxt.guild is None:
            return

        for uid, data in stats.items():
            member = cxt.guild.get_member(uid)
            if not isinstance(member, discord.Member):
                continue
            displayed_name = f"{member.name}"
            if member.nick is not None:
                displayed_name += f" (aka. {member.nick})"
            processed_stats.append((displayed_name, data[servstats.StatType.MSGNUM]))

        processed_stats.sort(key=lambda b: b[1], reverse=True)
        embed = discord.Embed(
            title="Statistics", description="Message count", color=0xFF5733
        )

        for data_ in processed_stats:
            embed.add_field(name=data_[0], value=str(data_[1]), inline=False)

        await cxt.response.send_message(embed=embed)
