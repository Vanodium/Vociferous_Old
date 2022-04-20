from __future__ import unicode_literals
import discord
from discord.ext import commands
import youtube_dl
from discord.utils import get


class YLBotClient(discord.Client):
    async def on_ready(self):
        await client.change_presence(activity = discord.Game("by 𝔙𝔞𝔫𝔬𝔡𝔦𝔲𝔪#7923"))
        for guild in self.guilds:
            print(f'{self.user} подключились к чату:{guild.name}(id: {guild.id})')
        await self.join_voice(960538088629747757)

    async def join_voice(self, channel_id):
        voice_channel = client.get_channel(channel_id)
        await voice_channel.connect()

    async def on_message(self, message):
        if 'https://www.youtube.com/watch?' in message.content:
            await message.channel.send("The song has been added to очередь...")
            await self.download_song([message.content])
            await message.channel.send("The song is ready to play")
        

    async def download_song(self, link):  
        file_title = link[0].split('v=')[1]
        ydl_opts = {
                'outtmpl': 'Downloaded_music/%(id)s.%(ext)s',
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                    'preferredquality': '96',
                }],
            }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(link)
        await self.play_song('Downloaded_music/' + file_title + '.m4a')


    async def play_song(self, name):
        voice = get(client.voice_clients)
        voice.play(discord.FFmpegPCMAudio(name))
        print('The song is playing')




client = YLBotClient()
TOKEN = "123"
client.run(TOKEN)
