import discord
from discord import app_commands
from discord.ext import commands
import wavelink
from utils.embed_builder import EmbedBuilder

class MusicControlView(discord.ui.View):
    def __init__(self, player):
        super().__init__(timeout=None)
        self.player = player

    @discord.ui.button(emoji="<:shuffle:123>", style=discord.ButtonStyle.gray)
    async def shuffle(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.player.queue.shuffle()
        await interaction.response.send_message("🔀 Queue Shuffled", ephemeral=True)

    @discord.ui.button(emoji="<:pause:123>", style=discord.ButtonStyle.blurple)
    async def pause_resume(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.player.pause(not self.player.paused)
        await interaction.response.send_message("⏸ Toggled Pause", ephemeral=True)

    @discord.ui.button(emoji="<:stop:123>", style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.player.disconnect()
        await interaction.response.send_message("⏹ Player Stopped", ephemeral=True)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play", description="Play any song or Spotify link")
    async def play(self, interaction: discord.Interaction, search: str):
        if not interaction.user.voice:
            return await interaction.response.send_message("Join a VC first!")

        await interaction.response.defer()
        
        tracks = await wavelink.Playable.search(search)
        if not tracks:
            return await interaction.followup.send("No results found.")

        if not interaction.guild.voice_client:
            vc = await interaction.user.voice.channel.connect(cls=wavelink.Player)
        else:
            vc = interaction.guild.voice_client

        track = tracks[0]
        await vc.queue.put_wait(track)
        
        if not vc.playing:
            await vc.play(vc.queue.get())
        
        embed = EmbedBuilder.now_playing(track, interaction.user, vc.node.identifier)
        await interaction.followup.send(embed=embed, view=MusicControlView(vc))

async def setup(bot):
    await bot.add_cog(Music(bot))
