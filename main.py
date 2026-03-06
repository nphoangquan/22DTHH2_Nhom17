import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from google import genai
import yt_dlp
import asyncio
import subprocess
import json
from collections import deque
import re
from flask import Flask
from pathlib import Path
import threading

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
genai_api_key = os.getenv('GENAI_API_KEY')  # Thêm biến môi trường cho API key

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='$', intents=intents)
client = genai.Client(api_key=genai_api_key)

# Web server setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!", 200

def run_web():
    app.run(host="0.0.0.0", port=10000)

# Start web server in another thread
thread = threading.Thread(target=run_web)
thread.daemon = True
thread.start()

# --------- yt-dlp cookies + options (Render-safe) ---------
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

def resolve_cookie_path() -> str | None:
    """Find a usable cookies.txt on Render/locally.

    Priority order:
    1) ENV: YTDLP_COOKIES_PATH or COOKIES_PATH
    2) ./cookies.txt (repo)
    3) /etc/secrets/cookies.txt (Render Secret File mount)
    4) /opt/render/project/src/cookies.txt (Render project root)
    Returns None if nothing exists.
    """
    candidates = [
        os.getenv("YTDLP_COOKIES_PATH"),
        os.getenv("COOKIES_PATH"),
        "./cookies.txt",
        "/etc/secrets/cookies.txt",
        "/opt/render/project/src/cookies.txt",
    ]

    for path in candidates:
        if not path:
            continue
        p = Path(path)
        if p.is_file():
            return str(p.resolve())
    return None

RESOLVED_COOKIE_PATH = resolve_cookie_path()
if RESOLVED_COOKIE_PATH:
    print(f"yt-dlp: using cookies at: {RESOLVED_COOKIE_PATH}")
else:
    print("yt-dlp: no cookies.txt found. YouTube may request verification on Render.")

def build_ytdlp_opts(quiet: bool = True) -> dict:
    """Centralized yt-dlp options with optional cookies and good headers."""
    opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": quiet,
        "no_warnings": quiet,
        "http_headers": {"User-Agent": USER_AGENT},
        # Using android client can reduce verification prompts sometimes
        "extractor_args": {"youtube": {"player_client": ["android"]}},
    }
    if RESOLVED_COOKIE_PATH:
        opts["cookiefile"] = RESOLVED_COOKIE_PATH
    return opts

# Audio system variables
voice_clients = {}
music_queues = {}
current_songs = {}

# FFMPEG options cho audio-only
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 '
                      f'-headers "User-Agent: {USER_AGENT}"',
    'options': '-vn'  # Chỉ phát audio, không có video
}

class MusicPlayer:
    def __init__(self):
        self.queue = deque()
        self.current_song = None
        self.is_playing = False
        self.volume = 0.5
        
    def add_song(self, song):
        self.queue.append(song)
        
    def get_next_song(self):
        if self.queue:
            self.current_song = self.queue.popleft()
            return self.current_song
        self.current_song = None
        return None
        
    def clear_queue(self):
        self.queue.clear()
        self.current_song = None
        
    def get_queue_info(self):
        if not self.queue and not self.current_song:
            return "Không có âm thanh nào trong queue"
        
        info = f"🎵 **Đang phát:** {self.current_song['title'] if self.current_song else 'Không có'}\n\n"
        
        if self.queue:
            info += "📋 **Queue:**\n"
            for i, song in enumerate(self.queue, 1):
                info += f"{i}. {song['title']} - {song['duration']}\n"
        else:
            info += "📋 **Queue:** Trống"
            
        return info

async def get_audio_info(url):
    """Lấy thông tin âm thanh từ nhiều nguồn khác nhau"""
    ydl_opts = build_ytdlp_opts(quiet=True)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Xác định nguồn âm thanh
            source_type = "Unknown"
            if "youtube.com" in url or "youtu.be" in url:
                source_type = "YouTube"
            elif "soundcloud.com" in url:
                source_type = "SoundCloud"
            elif "spotify.com" in url:
                source_type = "Spotify"
            elif url.endswith(('.mp3', '.wav', '.flac', '.m4a', '.ogg')):
                source_type = "Direct Audio"
            else:
                source_type = "Other"
            
            return {
                'title': info.get('title', 'Unknown'),
                'duration': format_duration(info.get('duration', 0)),
                'url': info.get('url', url),
                'webpage_url': info.get('webpage_url', url),
                'thumbnail': info.get('thumbnail', ''),
                'uploader': info.get('uploader', 'Unknown'),
                'source_type': source_type,
                'original_url': url
            }
    except Exception as e:
        print(f"Lỗi khi lấy thông tin âm thanh: {e}")
        return None

def format_duration(seconds):
    """Format thời gian từ giây sang mm:ss"""
    if not seconds:
        return "Unknown"
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    return f"{int(minutes):02d}:{int(seconds):02d}"

async def play_next_song(voice_client, guild_id):
    """Phát âm thanh tiếp theo trong queue"""
    if guild_id not in music_queues:
        return
        
    player = music_queues[guild_id]
    next_song = player.get_next_song()
    
    if not next_song:
        player.is_playing = False
        current_songs[guild_id] = None
        return
        
    try:
        player.is_playing = True
        current_songs[guild_id] = next_song
        
        # Tạo FFmpeg source với audio options
        source = discord.FFmpegPCMAudio(next_song['url'], **FFMPEG_OPTIONS)
        voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(
            play_next_song(voice_client, guild_id), bot.loop
        ))
            
    except Exception as e:
        print(f"Lỗi khi phát âm thanh: {e}")
        await play_next_song(voice_client, guild_id)


@bot.event
async def on_ready():
    print(f"Bot đã sẵn sàng! Tên: {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")
    print("Bot đang hoạt động...")
    
    # Test chat_bot function
    try:
        test_response = chat_bot("Xin chào, bạn là ai?")
        print(f"Test AI response: {test_response}")
    except Exception as e:
        print(f"Lỗi khi test AI: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "cc" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} cấm chat!")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def helps(ctx):
    """Hiển thị danh sách tất cả các lệnh có sẵn"""
    embed = discord.Embed(
        title="🤖 Danh sách lệnh của Bot",
        description="Dưới đây là tất cả các lệnh bạn có thể sử dụng:",
        color=0x00ff00
    )
    
    # Lệnh cơ bản
    embed.add_field(
        name="📝 Lệnh cơ bản",
        value="`$hello` - Chào hỏi\n`$helps` - Hiển thị danh sách lệnh này",
        inline=False
    )
    
    # Lệnh AI
    embed.add_field(
        name="🤖 Lệnh AI",
        value="`$start <câu hỏi>` - Hỏi AI",
        inline=False
    )
    
    # Lệnh audio/voice
    embed.add_field(
        name="🎵 Lệnh Audio/Voice",
        value="`$play <URL>` - Phát âm thanh từ bất kỳ link nào\n`$playfile` - Phát âm thanh từ file upload\n`$search <từ khóa>` - Tìm kiếm và phát âm thanh\n`$audio` - Bot tham gia kênh thoại\n`$skip` - Bỏ qua âm thanh hiện tại\n`$pause` - Tạm dừng âm thanh\n`$resume` - Tiếp tục phát âm thanh\n`$stop` - Dừng phát và xóa queue\n`$queue` - Hiển thị danh sách phát\n`$now` - Hiển thị âm thanh đang phát\n`$remove <số>` - Xóa âm thanh khỏi queue\n`$shuffle` - Xáo trộn queue\n`$volume [0-100]` - Điều chỉnh âm lượng\n`$leave` - Bot rời khỏi kênh voice",
        inline=False
    )
    
    # Lệnh quản lý
    embed.add_field(
        name="⚙️ Lệnh quản lý",
        value="Bot tự động xóa tin nhắn chứa 'cc' và cảnh báo người dùng",
        inline=False
    )
    
    embed.set_footer(text=f"Được yêu cầu bởi {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    
    await ctx.send(embed=embed)

@bot.command()
async def start(ctx, *, message):
    try:
        if not message:
            await ctx.send("Hãy nhập nội dung câu hỏi sau lệnh start.")
            return
            
        response = chat_bot(message)
        
        # Kiểm tra độ dài tin nhắn (Discord giới hạn 2000 ký tự)
        if len(response) > 2000:
            # Chia tin nhắn thành các phần nhỏ hơn
            chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
            for i, chunk in enumerate(chunks):
                if i == 0:
                    await ctx.send(f"**Trả lời (phần {i+1}/{len(chunks)}):**\n{chunk}")
                else:
                    await ctx.send(f"**Tiếp theo (phần {i+1}/{len(chunks)}):**\n{chunk}")
        else:
            await ctx.send(f"{response}")
            
    except Exception as e:
        print(f"Lỗi trong command start: {e}")
        await ctx.send("Có lỗi xảy ra hãy thực lại sau.")

@bot.command()
async def audio(ctx, *, url=None):
    """Tham gia kênh voice và phát âm thanh"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    voice_channel = ctx.author.voice.channel
    guild_id = ctx.guild.id
    
    # Khởi tạo music player nếu chưa có
    if guild_id not in music_queues:
        music_queues[guild_id] = MusicPlayer()
    
    # Tham gia kênh voice
    try:
        if guild_id in voice_clients and voice_clients[guild_id].is_connected():
            voice_client = voice_clients[guild_id]
        else:
            voice_client = await voice_channel.connect()
            voice_clients[guild_id] = voice_client
            
        await ctx.send(f"✅ Đã tham gia kênh **{voice_channel.name}**")
        
        # Nếu có URL, thêm vào queue và phát
        if url:
            await add_song_to_queue(ctx, url, voice_client, guild_id)
            
    except Exception as e:
        await ctx.send(f"❌ Lỗi khi tham gia kênh voice: {e}")

async def add_song_to_queue(ctx, url, voice_client, guild_id):
    """Thêm âm thanh vào queue"""
    # Kiểm tra URL hợp lệ
    if not re.match(r'https?://', url) and not url.endswith(('.mp3', '.wav', '.flac', '.m4a', '.ogg')):
        await ctx.send("❌ URL không hợp lệ! Hỗ trợ: YouTube, SoundCloud, Spotify, direct audio links (.mp3, .wav, .flac, .m4a, .ogg)")
        return
        
    await ctx.send("🔍 Đang tìm kiếm âm thanh...")
    
    # Lấy thông tin âm thanh
    song_info = await get_audio_info(url)
    if not song_info:
        await ctx.send("❌ Không thể lấy thông tin âm thanh! Vui lòng kiểm tra URL.")
        return
        
    # Thêm vào queue
    player = music_queues[guild_id]
    player.add_song(song_info)
    
    # Tạo embed thông tin âm thanh
    embed = discord.Embed(
        title="🎵 Đã thêm vào queue",
        description=f"**{song_info['title']}**",
        color=0x00ff00
    )
    embed.add_field(name="⏱️ Thời lượng", value=song_info['duration'], inline=True)
    embed.add_field(name="👤 Uploader", value=song_info['uploader'], inline=True)
    embed.add_field(name="📡 Nguồn", value=song_info['source_type'], inline=True)
    embed.add_field(name="🔗 Link", value=f"[{song_info['source_type']}]({song_info['webpage_url']})", inline=False)
    
    if song_info['thumbnail']:
        embed.set_thumbnail(url=song_info['thumbnail'])
        
    await ctx.send(embed=embed)
    
    # Nếu không có bài hát nào đang phát, bắt đầu phát
    if not player.is_playing:
        await play_next_song(voice_client, guild_id)

@bot.command()
async def play(ctx, *, url):
    """Phát âm thanh từ URL"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    if not url:
        await ctx.send("❌ Hãy cung cấp URL âm thanh! Hỗ trợ: YouTube, SoundCloud, Spotify, direct audio links")
        return
        
    voice_channel = ctx.author.voice.channel
    guild_id = ctx.guild.id
    
    # Khởi tạo music player nếu chưa có
    if guild_id not in music_queues:
        music_queues[guild_id] = MusicPlayer()
    
    # Tham gia kênh voice nếu chưa có
    if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
        try:
            voice_client = await voice_channel.connect()
            voice_clients[guild_id] = voice_client
            await ctx.send(f"✅ Đã tham gia kênh **{voice_channel.name}**")
        except Exception as e:
            await ctx.send(f"❌ Lỗi khi tham gia kênh voice: {e}")
            return
    else:
        voice_client = voice_clients[guild_id]
    
    await add_song_to_queue(ctx, url, voice_client, guild_id)

@bot.command()
async def playfile(ctx):
    """Phát âm thanh từ file được upload"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    if not ctx.message.attachments:
        await ctx.send("❌ Hãy upload file âm thanh! Hỗ trợ: .mp3, .wav, .flac, .m4a, .ogg")
        return
        
    attachment = ctx.message.attachments[0]
    
    # Kiểm tra định dạng file
    allowed_extensions = ['.mp3', '.wav', '.flac', '.m4a', '.ogg']
    if not any(attachment.filename.lower().endswith(ext) for ext in allowed_extensions):
        await ctx.send("❌ Định dạng file không được hỗ trợ! Hỗ trợ: .mp3, .wav, .flac, .m4a, .ogg")
        return
        
    voice_channel = ctx.author.voice.channel
    guild_id = ctx.guild.id
    
    # Khởi tạo music player nếu chưa có
    if guild_id not in music_queues:
        music_queues[guild_id] = MusicPlayer()
    
    # Tham gia kênh voice nếu chưa có
    if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
        try:
            voice_client = await voice_channel.connect()
            voice_clients[guild_id] = voice_client
            await ctx.send(f"✅ Đã tham gia kênh **{voice_channel.name}**")
        except Exception as e:
            await ctx.send(f"❌ Lỗi khi tham gia kênh voice: {e}")
            return
    else:
        voice_client = voice_clients[guild_id]
    
    await ctx.send("🔍 Đang xử lý file âm thanh...")
    
    # Tạo thông tin âm thanh từ file
    song_info = {
        'title': attachment.filename,
        'duration': 'Unknown',
        'url': attachment.url,
        'webpage_url': attachment.url,
        'thumbnail': '',
        'uploader': ctx.author.name,
        'source_type': 'Uploaded File',
        'original_url': attachment.url
    }
    
    # Thêm vào queue
    player = music_queues[guild_id]
    player.add_song(song_info)
    
    # Tạo embed thông tin âm thanh
    embed = discord.Embed(
        title="🎵 Đã thêm file vào queue",
        description=f"**{song_info['title']}**",
        color=0x00ff00
    )
    embed.add_field(name="👤 Uploader", value=song_info['uploader'], inline=True)
    embed.add_field(name="📡 Nguồn", value=song_info['source_type'], inline=True)
    embed.add_field(name="📁 File", value=f"[Download]({song_info['webpage_url']})", inline=False)
    
    await ctx.send(embed=embed)
    
    # Nếu không có bài hát nào đang phát, bắt đầu phát
    if not player.is_playing:
        await play_next_song(voice_client, guild_id)

@bot.command()
async def skip(ctx):
    """Bỏ qua âm thanh hiện tại"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    guild_id = ctx.guild.id
    if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
        await ctx.send("❌ Bot không ở trong kênh voice!")
        return
        
    voice_client = voice_clients[guild_id]
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("⏭️ Đã bỏ qua âm thanh hiện tại!")
    else:
        await ctx.send("❌ Không có âm thanh nào đang phát!")

@bot.command()
async def stop(ctx):
    """Dừng phát âm thanh và xóa queue"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    guild_id = ctx.guild.id
    if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
        await ctx.send("❌ Bot không ở trong kênh voice!")
        return
        
    voice_client = voice_clients[guild_id]
    voice_client.stop()
    
    if guild_id in music_queues:
        music_queues[guild_id].clear_queue()
        music_queues[guild_id].is_playing = False
        current_songs[guild_id] = None
        
    await ctx.send("⏹️ Đã dừng phát âm thanh và xóa queue!")

@bot.command()
async def pause(ctx):
    """Tạm dừng âm thanh"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    guild_id = ctx.guild.id
    if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
        await ctx.send("❌ Bot không ở trong kênh voice!")
        return
        
    voice_client = voice_clients[guild_id]
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send("⏸️ Đã tạm dừng âm thanh!")
    else:
        await ctx.send("❌ Không có âm thanh nào đang phát!")

@bot.command()
async def resume(ctx):
    """Tiếp tục phát âm thanh"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    guild_id = ctx.guild.id
    if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
        await ctx.send("❌ Bot không ở trong kênh voice!")
        return
        
    voice_client = voice_clients[guild_id]
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send("▶️ Đã tiếp tục phát âm thanh!")
    else:
        await ctx.send("❌ Âm thanh không bị tạm dừng!")

@bot.command()
async def queue(ctx):
    """Hiển thị danh sách phát"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    guild_id = ctx.guild.id
    if guild_id not in music_queues:
        await ctx.send("❌ Không có queue nào!")
        return
        
    player = music_queues[guild_id]
    queue_info = player.get_queue_info()
    
    embed = discord.Embed(
        title="📋 Danh sách phát",
        description=queue_info,
        color=0x00ff00
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def now(ctx):
    """Hiển thị âm thanh đang phát"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    guild_id = ctx.guild.id
    if guild_id not in current_songs or not current_songs[guild_id]:
        await ctx.send("❌ Không có âm thanh nào đang phát!")
        return
        
    song = current_songs[guild_id]
    
    embed = discord.Embed(
        title="🎵 Đang phát",
        description=f"**{song['title']}**",
        color=0x00ff00
    )
    embed.add_field(name="⏱️ Thời lượng", value=song['duration'], inline=True)
    embed.add_field(name="👤 Uploader", value=song['uploader'], inline=True)
    embed.add_field(name="📡 Nguồn", value=song['source_type'], inline=True)
    embed.add_field(name="🔗 Link", value=f"[{song['source_type']}]({song['webpage_url']})", inline=False)
    
    if song['thumbnail']:
        embed.set_thumbnail(url=song['thumbnail'])
        
    await ctx.send(embed=embed)

@bot.command()
async def leave(ctx):
    """Bot rời khỏi kênh voice"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    guild_id = ctx.guild.id
    if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
        await ctx.send("❌ Bot không ở trong kênh voice!")
        return
        
    voice_client = voice_clients[guild_id]
    voice_client.stop()
    await voice_client.disconnect()
    
    # Xóa dữ liệu
    if guild_id in voice_clients:
        del voice_clients[guild_id]
    if guild_id in music_queues:
        del music_queues[guild_id]
    if guild_id in current_songs:
        del current_songs[guild_id]
        
    await ctx.send("👋 Đã rời khỏi kênh voice!")

@bot.command()
async def volume(ctx, vol: int = None):
    """Điều chỉnh âm lượng (0-100)"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    guild_id = ctx.guild.id
    if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
        await ctx.send("❌ Bot không ở trong kênh voice!")
        return
        
    if vol is None:
        # Hiển thị âm lượng hiện tại
        current_vol = int(music_queues[guild_id].volume * 100)
        await ctx.send(f"🔊 Âm lượng hiện tại: **{current_vol}%**")
        return
        
    if not 0 <= vol <= 100:
        await ctx.send("❌ Âm lượng phải từ 0-100!")
        return
        
    voice_client = voice_clients[guild_id]
    voice_client.source.volume = vol / 100
    music_queues[guild_id].volume = vol / 100
    
    await ctx.send(f"🔊 Đã điều chỉnh âm lượng thành **{vol}%**!")

@bot.command()
async def search(ctx, *, query):
    """Tìm kiếm và phát âm thanh từ YouTube"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    if not query:
        await ctx.send("❌ Hãy nhập từ khóa tìm kiếm!")
        return
        
    voice_channel = ctx.author.voice.channel
    guild_id = ctx.guild.id
    
    # Khởi tạo music player nếu chưa có
    if guild_id not in music_queues:
        music_queues[guild_id] = MusicPlayer()
    
    # Tham gia kênh voice nếu chưa có
    if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
        try:
            voice_client = await voice_channel.connect()
            voice_clients[guild_id] = voice_client
            await ctx.send(f"✅ Đã tham gia kênh **{voice_channel.name}**")
        except Exception as e:
            await ctx.send(f"❌ Lỗi khi tham gia kênh voice: {e}")
            return
    else:
        voice_client = voice_clients[guild_id]
    
    await ctx.send(f"🔍 Đang tìm kiếm trên YouTube: **{query}**")
    
    # Tìm kiếm trên YouTube
    search_url = f"ytsearch1:{query}"
    song_info = await get_audio_info(search_url)
    
    if not song_info:
        await ctx.send("❌ Không tìm thấy kết quả nào!")
        return
    
    # Thêm vào queue
    player = music_queues[guild_id]
    player.add_song(song_info)
    
    # Tạo embed thông tin âm thanh
    embed = discord.Embed(
        title="🎵 Đã tìm thấy và thêm vào queue",
        description=f"**{song_info['title']}**",
        color=0x00ff00
    )
    embed.add_field(name="⏱️ Thời lượng", value=song_info['duration'], inline=True)
    embed.add_field(name="👤 Uploader", value=song_info['uploader'], inline=True)
    embed.add_field(name="📡 Nguồn", value=song_info['source_type'], inline=True)
    embed.add_field(name="🔗 Link", value=f"[{song_info['source_type']}]({song_info['webpage_url']})", inline=False)
    
    if song_info['thumbnail']:
        embed.set_thumbnail(url=song_info['thumbnail'])
        
    await ctx.send(embed=embed)
    
    # Nếu không có bài hát nào đang phát, bắt đầu phát
    if not player.is_playing:
        await play_next_song(voice_client, guild_id)

@bot.command()
async def remove(ctx, index: int):
    """Xóa âm thanh khỏi queue theo vị trí"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    guild_id = ctx.guild.id
    if guild_id not in music_queues:
        await ctx.send("❌ Không có queue nào!")
        return
        
    player = music_queues[guild_id]
    
    if not player.queue:
        await ctx.send("❌ Queue trống!")
        return
        
    if index < 1 or index > len(player.queue):
        await ctx.send(f"❌ Vị trí không hợp lệ! Queue có {len(player.queue)} âm thanh.")
        return
        
    # Xóa âm thanh khỏi queue (index bắt đầu từ 1)
    removed_song = player.queue[index - 1]
    del player.queue[index - 1]
    
    await ctx.send(f"🗑️ Đã xóa âm thanh: **{removed_song['title']}**")

@bot.command()
async def shuffle(ctx):
    """Xáo trộn queue"""
    if not ctx.author.voice:
        await ctx.send("❌ Bạn phải ở trong kênh voice để sử dụng lệnh này!")
        return
        
    guild_id = ctx.guild.id
    if guild_id not in music_queues:
        await ctx.send("❌ Không có queue nào!")
        return
        
    player = music_queues[guild_id]
    
    if len(player.queue) < 2:
        await ctx.send("❌ Cần ít nhất 2 âm thanh để xáo trộn!")
        return
        
    import random
    random.shuffle(player.queue)
    
    await ctx.send("🔀 Đã xáo trộn queue!")


def chat_bot(message):
    try:
        filtered_message = message
        ai_source_keywords = [
            "gemini", "google", "openai", "chatgpt", "claude", "anthropic",
            "bạn được tạo bởi", "bạn được phát triển bởi", "ai model", "language model",
            "trained on", "được huấn luyện", "data source", "nguồn dữ liệu",
            "who created you", "who made you", "what are you", "bạn là gì", "bạn là AI nào"
        ]
        
        # Thay thế từ khóa bằng câu hỏi chung
        for keyword in ai_source_keywords:
            if keyword.lower() in filtered_message.lower():
                filtered_message = "Tôi là một trợ lý AI được thiết kế để giúp đỡ bạn. Bạn có thể hỏi tôi về bất kỳ chủ đề nào khác."
                break
        
        # Nếu không có từ khóa cấm, gọi AI bình thường
        if filtered_message == message:
            # Thêm prompt để giới hạn độ dài câu trả lời
            prompt = f"{message}\n\nHãy trả lời ngắn gọn, súc tích trong khoảng 1500 ký tự trở xuống."
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
            response_text = response.text
            
            # Giới hạn độ dài câu trả lời
            if len(response_text) > 1800:
                response_text = response_text[:1800] + "...\n\n*[Câu trả lời đã được cắt ngắn do giới hạn độ dài]*"
            
            return response_text
        else:
            return filtered_message
            
    except Exception as e:
        print(f"Lỗi khi gọi AI: {e}")
        return "Xin lỗi, có lỗi xảy ra khi xử lý yêu cầu."


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
