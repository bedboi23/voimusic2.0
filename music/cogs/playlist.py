import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class Playlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "playlists.json"
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f: json.dump({}, f)

    @app_commands.command(name="playlist-save", description="Save current queue to a Voi Playlist")
    async def save(self, interaction: discord.Interaction, name: str):
        vc = interaction.guild.voice_client
        if not vc or vc.queue.is_empty:
            return await interaction.response.send_message("❌ Nothing in the queue to save.", ephemeral=True)

        tracks = [t.uri for t in vc.queue]
        
        with open(self.db_path, "r") as f:
            data = json.load(f)
        
        user_id = str(interaction.user.id)
        if user_id not in data: data[user_id] = {}
        
        data[user_id][name] = tracks
        
        with open(self.db_path, "w") as f:
            json.dump(data, f)

        await interaction.response.send_message(f"✅ Saved **{len(tracks)}** tracks to playlist: `{name}`")

    @app_commands.command(name="playlist-load", description="Load one of your saved playlists")
    async def load(self, interaction: discord.Interaction, name: str):
        # Implementation to fetch from JSON and add to Wavelink Queue
        await interaction.response.send_message("🔄 Loading your Voi Playlist...")

async def setup(bot):
    await bot.add_cog(Playlist(bot))
