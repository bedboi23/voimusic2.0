import discord
import os
import asyncio
import wavelink
from discord.ext import commands

class VoiBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=None, intents=intents)

    async def setup_hook(self):
        # Lavalink Node Setup
        nodes = [wavelink.Node(uri=os.getenv("LAVALINK_URL"), password=os.getenv("LAVALINK_PASSWORD"))]
        await wavelink.Pool.connect(nodes=nodes, client=self)
        
        # Load Cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {self.user} | Premium Minimal Active')
        await self.change_presence(activity=discord.Streaming(name="Voi Music", url="https://twitch.tv/voi"))

bot = VoiBot()
bot.run(os.getenv("DISCORD_TOKEN"))
