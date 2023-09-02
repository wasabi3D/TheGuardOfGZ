import discord
from discord.ext import commands
from discord.utils import get
import servstats

async def respond_messagecount(cxt: discord.Interaction, year: int, week: int):
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
        if data_ == 0 or data_ is None: continue
        embed.add_field(name=data_[0], value=str(data_[1]), inline=False)

    await cxt.response.send_message(embed=embed)

async def respond_vocaltime(cxt: discord.Interaction, year: int, week: int):
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
        processed_stats.append((displayed_name, data[servstats.StatType.VOCALTIME]))

    processed_stats.sort(key=lambda b: b[1], reverse=True)
    embed = discord.Embed(
        title="Statistics", description="Vocal time", color=0xFF5733
    )

    for data_ in processed_stats:
        minutes, seconds = round(data_[1]) // 60, round(data_[1] % 60)
        hours, minutes = minutes // 60, minutes % 60
        days, hours = hours // 24, hours % 24
        if not any([days, hours, minutes, seconds]): continue
        units = [(days, "d"), (hours, "h"), (minutes, "m"), (seconds, "s")]
        prev = False
        val = "".join([f"{unit}{unit_sign}" if (prev := (prev or unit != 0)) else "" for unit, unit_sign in units])
        embed.add_field(name=data_[0], value=val, inline=False)

    await cxt.response.send_message(embed=embed)


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
        await respond_messagecount(cxt, year, week)

    @bot.tree.command(name="curweekmsgcount", guild=guild_gz)
    async def _curweekmessagecount(cxt: discord.Interaction):
        await respond_messagecount(cxt, *servstats.getCurrentWeekID().split("-"))
    
    @bot.tree.command(name="vocaltime", guild=guild_gz)
    async def _voicetime(cxt: discord.Interaction, year: int, week: int):
        await respond_vocaltime(cxt, year, week)

    @bot.tree.command(name="curweekvocaltime", guild=guild_gz)
    async def _voicetime(cxt: discord.Interaction):
        await respond_vocaltime(cxt, *servstats.getCurrentWeekID().split("-"))
