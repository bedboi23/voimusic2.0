import discord
import wavelink
from .embed_builder import EmbedBuilder

class VoiPlayer(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = None  # To store the last interaction context
        self.waiting = False
        self.loop_mode = "None" # Options: None, Track, Queue

    async def do_next(self):
        if self.queue.is_empty:
            # Radio Mode / AutoPlay Logic
            if hasattr(self, "autoplay") and self.autoplay:
                # Logic to fetch related tracks from Wavelink
                pass
            return await self.context.send("✨ Queue finished. Add more songs to keep the vibe going!")

        track = self.queue.get()
        await self.play(track)
        
        # Re-send the Now Playing UI
        embed = EmbedBuilder.now_playing(track, self.context.user, self.node.identifier)
        from cogs.music import MusicControlView # Local import to avoid circularity
        await self.context.channel.send(embed=embed, view=MusicControlView(self))

    async def handle_event(self, event):
        if event == "TrackEndEvent":
            await self.do_next()
