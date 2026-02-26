import discord
from datetime import datetime

class EmbedBuilder:
    @staticmethod
    def now_playing(track, requester, node_name):
        embed = discord.Embed(color=0xFFFFFF) # White accent
        
        # Header with platform icon logic
        icon = "🎵"
        if "spotify" in track.uri: icon = "<:spotify:123456789>" # Replace with actual IDs
        elif "youtube" in track.uri: icon = "<:youtube:123456789>"

        embed.title = f"{icon} **Now Playing** ✨"
        embed.description = f"**` {track.title} `**\n\u200b" # Invisible char for spacing
        
        # Info Grid (Row 1)
        embed.add_field(name="🎼 Artist", value=f"`{track.author}`", inline=True)
        embed.add_field(name="⏱ Duration", value=f"`{format_ms(track.length)}`", inline=True)
        embed.add_field(name="👤 Requested By", value=requester.mention, inline=True)
        
        # Info Grid (Row 2)
        embed.add_field(name="🌐 Node", value=f"`{node_name}`", inline=True)
        finish_time = datetime.now().timestamp() + (track.length / 1000)
        embed.add_field(name="🕒 Finish Time", value=f"<t:{int(finish_time)}:t>", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)

        embed.set_image(url=track.artwork)
        embed.set_footer(text="Powered by Voi Music • Premium Aesthetic", icon_url=requester.display_avatar.url)
        return embed

def format_ms(ms):
    seconds = int((ms / 1000) % 60)
    minutes = int((ms / (1000 * 60)) % 60)
    return f"{minutes:02d}:{seconds:02d}"
