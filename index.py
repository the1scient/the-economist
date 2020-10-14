import os
import time
import aiohttp
import discord
import importlib
import os
import sys

from discord.ext import commands
from utils import permissions, default, http, dataIO
from utils.data import Bot, HelpFormat

config = default.get("economist.json")
print("Fazendo login no Discord com o token: " +config.token+ ".")

bot = Bot(
    command_prefix=config.prefix,
    prefix=config.prefix,
    command_attrs=dict(hidden=True),
    help_command=HelpFormat()
)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")
        print("[{0}] - COMANDOS carregados".format(name))

bot.run(config.token)
