from __future__ import unicode_literals
import discord
import youtube_dl
from discord.utils import get
import sqlite3

#from re import L
#zfrom discord.ext import commands


class VociderousClient(discord.Client):
    async def on_ready(self):
        await client.change_presence(activity = discord.Game("by 𝔙𝔞𝔫𝔬𝔡𝔦𝔲𝔪#7923"))
        for guild in self.guilds:
            print(f'{self.user} подключились к чату:{guild.name}(id: {guild.id})')
        await self.join_voice(bot_voicechannel_id)

    async def join_voice(self, channel_id):
        voice_channel = client.get_channel(channel_id)
        await voice_channel.connect()

    async def on_message(self, message):
        if message.channel.id == bot_txtchannel_id:
            if '!stream' in message.content:
               radio = VociferousRadioPlayer()
               await radio.choose_genre(message.content)
            elif 'https://www.youtube.com/watch?' in message.content:
                YT_videoplayer = VociferousYTPlayer()
                await YT_videoplayer.youtube_audio(message)
    
    
class VociferousYTPlayer(VociderousClient, discord.Client):
    def __init__(self):
        super().__init__()

    async def youtube_audio(self, message):
        status_message = await message.channel.send("Preparing the song...")
        link = [message.content]
        able_to_play = await self.download_song(link)
        if able_to_play:
            await self.play_song('Downloaded_music/' + link[0].split('v=')[1] + '.m4a', status_message)
            await status_message.edit(content="Playing")
        else:
            await status_message.edit(content="Song is already playing")

    async def download_song(self, link):  
        try:
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
                return True
        except:
            return False

    async def play_song(self, name, status_message):
        await status_message.edit(content="Ready to play!")
        voice = get(client.voice_clients)
        voice.play(discord.FFmpegPCMAudio(name))


class VociferousRadioPlayer(VociderousClient, discord.Client):
    def __init__(self):
        super().__init__()
    
    async def choose_genre(self, msg):
        genre = " ".join(msg.split()[1::])
        link = await self.get_link_by_genre(genre)
        if link:
            await self.youtube_radio(link)
    
    async def get_link_by_genre(self, genre):
        try:
            con = sqlite3.connect('Radiostations.db')
            cur = con.cursor()
            link = cur.execute("""SELECT * FROM Links_by_genres WHERE Genre = ?""", (genre,)).fetchall()[0][1]
            con.close()
            return link
        except:
            channel = client.get_channel(bot_txtchannel_id)
            await channel.send("Sorry, we don't have this genre")
            return

    async def youtube_radio(self, link):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist':'True'}    
        voice = get(client.voice_clients)
        ydl = youtube_dl.YoutubeDL(YDL_OPTIONS)
        with ydl:
            info = ydl.extract_info(link, download=False)
            I_URL = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(I_URL, **FFMPEG_OPTIONS)
            voice.pause()
            voice.play(source)
            #voice.is_playing()


global bot_txtchannel_id
global bot_voicechannel_id
bot_txtchannel_id = 961626634472030349
bot_voicechannel_id = 960538088629747757

client = VociderousClient()
TOKEN = ""
client.run(TOKEN)
