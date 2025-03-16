# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2025-03-13 18:48:27
# @Last Modified by:   Your name
# @Last Modified time: 2025-03-16 15:59:45
import os
import re
import time
import pyautogui
import discord
from discord.ext import commands
from pynput.mouse import Controller, Button
from datetime import datetime
from dotenv import load_dotenv
import psutil
import asyncio
import webbrowser
import subprocess
from yt_dlp import YoutubeDL
from discord import FFmpegPCMAudio, Embed
from discord.ui import Button, View
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import platform  # Thêm thư viện platform
import socket  # Thêm thư viện socket

# Cấu hình bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "#"  # Tiền tố lệnh

# Khởi tạo bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Đường dẫn lưu file tải về
UPLOAD_FOLDER = "G:/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Biến toàn cục cho Selenium (nếu cần)
driver = None

# ID Discord của bạn
ALLOWED_USER_ID = 815952271421472808

# Danh sách phát nhạc
queue = []

# Hàm kiểm tra ID người dùng
def is_allowed_user(ctx):
    return ctx.author.id == ALLOWED_USER_ID

# Hàm in thông báo ra terminal
def log_action(action: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {action}")

# Sự kiện khi bot đăng nhập thành công
@bot.event
async def on_ready():
    log_action(f"đăng nhập thành công với tên: {bot.user.name}")

# Lệnh giới thiệu
@bot.command(name="introduce")
async def introduce(ctx):
    log_action(f"{ctx.author} đã sử dụng lệnh /introduce")
    await ctx.send(
        "👨‍💻 DEVELOPER | Cường GatsBy\n\n"
        "📩 Contact for Work:\n"
        "- Discord: cuonggatsby94\n"
        "- Telegram: @cuonggatsby94\n"
        "- GitHub: https://github.com/CuongGatsBy94\n\n"
        "🌟 DONATE:\n"
        "💳 02087212901 | cuonggatsby94\n"
        "Tienphongbank - Ngân hàng Tiên Phong\n\n"
    )

# Lệnh tắt máy
@bot.command(name="shutdown")
@commands.check(is_allowed_user)
async def shutdown(ctx):
    log_action(f"{ctx.author} đã sử dụng lệnh /shutdown")
    await ctx.send("Máy sẽ tắt sau 3 giây.")
    os.system("shutdown /s /t 3")

# Lệnh khởi động lại máy
@bot.command(name="restart")
@commands.check(is_allowed_user)
async def restart(ctx):
    log_action(f"{ctx.author} đã sử dụng lệnh /restart")
    await ctx.send("Máy sẽ khởi động lại sau 3 giây.")
    os.system("shutdown /r /t 3")

# Lệnh chụp màn hình
@bot.command(name="screenshot")
@commands.check(is_allowed_user)
async def screenshot(ctx):
    log_action(f"{ctx.author} đã sử dụng lệnh /screenshot")
    file_name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    screenshot_path = os.path.join(UPLOAD_FOLDER, file_name)

    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)

        with open(screenshot_path, 'rb') as f:
            await ctx.send(file=discord.File(f))

        os.remove(screenshot_path)
        await ctx.send("Đã chụp ảnh màn hình và gửi thành công!")
    except Exception as e:
        await ctx.send(f"Có lỗi xảy ra khi chụp ảnh màn hình: {e}")

# Lệnh tải file từ máy
@bot.command(name="downloadfile")
@commands.check(is_allowed_user)
async def download_file(ctx, file_path: str):
    log_action(f"{ctx.author} đã sử dụng lệnh /downloadfile")
    if not os.path.isfile(file_path):
        await ctx.send(f"Không tìm thấy file tại đường dẫn: {file_path}")
        return

    try:
        with open(file_path, 'rb') as f:
            await ctx.send(file=discord.File(f))
        await ctx.send(f"File đã được gửi thành công: {file_path}")
    except Exception as e:
        await ctx.send(f"Có lỗi xảy ra khi gửi file: {e}")

# Lệnh xóa file
@bot.command(name="deletefile")
@commands.check(is_allowed_user)
async def delete_file(ctx, file_path: str):
    log_action(f"{ctx.author} đã sử dụng lệnh /deletefile")
    if not os.path.isfile(file_path):
        await ctx.send(f"Không tìm thấy file tại đường dẫn: {file_path}")
        return

    try:
        os.remove(file_path)
        await ctx.send(f"File tại đường dẫn {file_path} đã được xóa thành công.")
    except Exception as e:
        await ctx.send(f"Có lỗi xảy ra khi xóa file: {e}")

# Lệnh hiển thị danh sách lệnh
@bot.command(name="menu")
async def menu(ctx):
    log_action(f"{ctx.author} đã sử dụng lệnh /menu")
    commands_list = [
        "🔻 #introduce ➡️ Giới thiệu về tôi.",
        "🔻 #shutdown ➡️ Tắt máy.",
        "🔻 #restart ➡️ Khởi động lại máy.",
        "🔻 #screenshot ➡️ Chụp ảnh màn hình.",
        "🔻 #downloadfile <đường dẫn> ➡️ Tải file từ máy.",
        "🔻 #deletefile <đường dẫn> ➡️ Xóa file trên máy.",
        "🔻 #play <tên bài hát> ➡️ Tìm kiếm và thêm vào danh sách phát.",
        "🔻 #queue ➡️ Hiển thị danh sách phát.",
        "🔻 #skip ➡️ Bỏ qua bài hát hiện tại.",
        "🔻 #stop ➡️ Dừng phát nhạc.",
        "🔻 #volume <0-100> ➡️ Điều chỉnh âm lượng.",
        "🔻 #systeminfo ➡️ Thông tin hệ thống.",
        "🔻 #tasklist ➡️ Danh sách tiến trình.",
        "🔻 #killtask <pid> ➡️ Dừng tiến trình.",
        "🔻 #type <text> ➡️ Nhập văn bản.",
        "🔻 #press <key> ➡️ Nhấn phím.",
        "🔻 #openweb <url> ➡️ Mở trang web.",
        "🔻 #openapp <path> ➡️ Mở ứng dụng.",
        "🔻 #remind <seconds> <message> ➡️ Đặt lời nhắc.",
    ]
    await ctx.send("\n".join(commands_list))

# Lệnh điều khiển chuột
mouse = Controller()

@bot.command(name="controlmouse")
async def control_mouse(ctx, action: str):
    log_action(f"{ctx.author} đã sử dụng lệnh /controlmouse")
    if action == "up":
        mouse.move(0, -30)  # Di chuyển lên
    elif action == "down":
        mouse.move(0, 30)  # Di chuyển xuống
    elif action == "left":
        mouse.move(-30, 0)  # Di chuyển sang trái
    elif action == "right":
        mouse.move(30, 0)  # Di chuyển sang phải
    elif action == "click":
        mouse.click(Button.left, 1)  # Click chuột trái
    else:
        await ctx.send("Hành động không hợp lệ. Các hành động hợp lệ: up, down, left, right, click.")
        return

    await ctx.send(f"Đã thực hiện hành động: {action}")

# Lệnh tìm kiếm và thêm vào danh sách phát
@bot.command(name="play")
async def play(ctx, *, query: str):
    log_action(f"{ctx.author} đã sử dụng lệnh /play với tìm kiếm: {query}")
    if not ctx.author.voice:
        await ctx.send("Bạn cần tham gia một voice channel trước!")
        return

    # Tìm kiếm bài hát trên YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extract_flat': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if not info['entries']:
                await ctx.send("Không tìm thấy bài hát phù hợp.")
                return

            # Lấy video đầu tiên từ kết quả tìm kiếm
            yt = info['entries'][0]
            queue.append(yt)
            await ctx.send(f"Đã thêm vào danh sách phát: {yt['title']}")

            # Nếu bot chưa kết nối đến voice channel, kết nối ngay
            if not ctx.voice_client:
                channel = ctx.author.voice.channel
                await channel.connect()

            # Nếu không có bài hát nào đang phát, bắt đầu phát
            if not ctx.voice_client.is_playing():
                play_next(ctx)
        except Exception as e:
            await ctx.send(f"Có lỗi xảy ra: {e}")

# Hàm phát bài hát tiếp theo trong danh sách
def play_next(ctx):
    if queue:
        yt = queue.pop(0)
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': os.path.join(UPLOAD_FOLDER, 'audio.mp3'),
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt['url']])

        ctx.voice_client.play(
            FFmpegPCMAudio(os.path.join(UPLOAD_FOLDER, "audio.mp3")),
            after=lambda e: play_next(ctx)
        )
        ctx.send(f"Đang phát: {yt['title']}")
        show_control_panel(ctx)

# Hiển thị bảng điều khiển
def show_control_panel(ctx):
    embed = Embed(title="Điều khiển phát nhạc", description="Sử dụng các nút bên dưới để điều khiển.")
    view = View()

    # Nút tạm dừng/tiếp tục
    pause_button = Button(style=discord.ButtonStyle.primary, label="⏯️ Tạm dừng/Tiếp tục")
    pause_button.callback = lambda interaction: toggle_pause(ctx, interaction)
    view.add_item(pause_button)

    # Nút bỏ qua bài hát
    skip_button = Button(style=discord.ButtonStyle.secondary, label="⏭️ Bỏ qua")
    skip_button.callback = lambda interaction: skip(ctx, interaction)
    view.add_item(skip_button)

    # Nút dừng phát nhạc
    stop_button = Button(style=discord.ButtonStyle.danger, label="⏹️ Dừng")
    stop_button.callback = lambda interaction: stop(ctx, interaction)
    view.add_item(stop_button)

    ctx.send(embed=embed, view=view)

# Xử lý nút tạm dừng/tiếp tục
async def toggle_pause(ctx, interaction):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await interaction.response.send_message("Đã tạm dừng phát nhạc.")
    else:
        ctx.voice_client.resume()
        await interaction.response.send_message("Đã tiếp tục phát nhạc.")

# Xử lý nút bỏ qua bài hát
async def skip(ctx, interaction):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await interaction.response.send_message("Đã bỏ qua bài hát hiện tại.")
    else:
        await interaction.response.send_message("Không có bài hát nào đang phát.")

# Xử lý nút dừng phát nhạc
async def stop(ctx, interaction):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        queue.clear()
        await interaction.response.send_message("Đã dừng phát nhạc và xóa danh sách phát.")

# Lệnh hiển thị danh sách phát
@bot.command(name="queue")
async def show_queue(ctx):
    log_action(f"{ctx.author} đã sử dụng lệnh /queue")
    if not queue:
        await ctx.send("Danh sách phát đang trống.")
        return

    queue_list = "\n".join([f"{i + 1}. {yt['title']}" for i, yt in enumerate(queue)])
    await ctx.send(f"Danh sách phát:\n{queue_list}")

# Lệnh bỏ qua bài hát hiện tại
@bot.command(name="skip")
async def skip(ctx):
    log_action(f"{ctx.author} đã sử dụng lệnh /skip")
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Đã bỏ qua bài hát hiện tại.")
    else:
        await ctx.send("Không có bài hát nào đang phát.")

# Lệnh dừng phát nhạc
@bot.command(name="stop")
async def stop(ctx):
    log_action(f"{ctx.author} đã sử dụng lệnh /stop")
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        queue.clear()
        await ctx.send("Đã dừng phát nhạc và xóa danh sách phát.")

# Điều chỉnh âm lượng
@bot.command(name="volume")
async def set_volume(ctx, level: int):
    log_action(f"{ctx.author} đã sử dụng lệnh /volume với mức âm lượng: {level}")
    if level < 0 or level > 100:
        await ctx.send("Âm lượng phải nằm trong khoảng 0 đến 100.")
        return

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        volume.SetMasterVolume(level / 100, None)

    await ctx.send(f"Đã đặt âm lượng thành {level}%.")

# Thông tin hệ thống
@bot.command(name="systeminfo")
async def system_info(ctx):
    log_action(f"{ctx.author} đã sử dụng lệnh /systeminfo")

    # Thông tin CPU
    cpu_count = psutil.cpu_count(logical=True)  # Tổng số core và thread
    cpu_freq = psutil.cpu_freq().current  # Tần số CPU hiện tại (MHz)
    cpu_usage = psutil.cpu_percent(interval=1)  # % sử dụng CPU

    # Thông tin RAM
    memory_info = psutil.virtual_memory()
    total_ram = memory_info.total / (1024 ** 3)  # Tổng RAM (GB)
    used_ram = memory_info.used / (1024 ** 3)  # RAM đã sử dụng (GB)
    ram_usage = memory_info.percent  # % sử dụng RAM

    # Thông tin ổ đĩa
    disk_info = psutil.disk_usage('/')
    total_disk = disk_info.total / (1024 ** 3)  # Tổng dung lượng ổ đĩa (GB)
    used_disk = disk_info.used / (1024 ** 3)  # Dung lượng đã sử dụng (GB)
    disk_usage = disk_info.percent  # % sử dụng ổ đĩa

    # Thông tin mạng
    hostname = socket.gethostname()  # Tên máy
    ip_address = socket.gethostbyname(hostname)  # Địa chỉ IP

    # Thông tin hệ điều hành
    os_name = platform.system()  # Tên hệ điều hành
    os_version = platform.version()  # Phiên bản hệ điều hành

    # Tạo embed để hiển thị thông tin
    embed = discord.Embed(
        title="🖥️ Thông tin hệ thống",
        description="Chi tiết thông tin hệ thống máy tính.",
        color=discord.Color.blue()
    )

    # Thêm các trường thông tin
    embed.add_field(
        name="💻 CPU",
        value=(
            f"- Số core/thread: {cpu_count}\n"
            f"- Tần số: {cpu_freq:.2f} MHz\n"
            f"- Sử dụng: {cpu_usage}%"
        ),
        inline=False
    )

    embed.add_field(
        name="🧠 RAM",
        value=(
            f"- Tổng RAM: {total_ram:.2f} GB\n"
            f"- Đã sử dụng: {used_ram:.2f} GB\n"
            f"- Sử dụng: {ram_usage}%"
        ),
        inline=False
    )

    embed.add_field(
        name="💾 Ổ đĩa",
        value=(
            f"- Tổng dung lượng: {total_disk:.2f} GB\n"
            f"- Đã sử dụng: {used_disk:.2f} GB\n"
            f"- Sử dụng: {disk_usage}%"
        ),
        inline=False
    )

    embed.add_field(
        name="🌐 Mạng",
        value=(
            f"- Tên máy: {hostname}\n"
            f"- Địa chỉ IP: {ip_address}"
        ),
        inline=False
    )

    embed.add_field(
        name="🖥️ Hệ điều hành",
        value=(
            f"- Tên: {os_name}\n"
            f"- Phiên bản: {os_version}"
        ),
        inline=False
    )

    # Gửi embed
    await ctx.send(embed=embed)

# Quản lý tiến trình
@bot.command(name="tasklist")
async def task_list(ctx):
    log_action(f"{ctx.author} đã sử dụng lệnh /tasklist")
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append(f"{proc.info['pid']}: {proc.info['name']}")

    message = "📋 **Danh sách tiến trình:**\n" + "\n".join(processes[:20])  # Giới hạn hiển thị 20 tiến trình
    await ctx.send(message)

@bot.command(name="killtask")
async def kill_task(ctx, pid: int):
    log_action(f"{ctx.author} đã sử dụng lệnh /killtask với PID: {pid}")
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        await ctx.send(f"Đã dừng tiến trình {pid}.")
    except psutil.NoSuchProcess:
        await ctx.send(f"Không tìm thấy tiến trình với PID {pid}.")

# Điều khiển bàn phím ảo
@bot.command(name="type")
async def type_text(ctx, *, text: str):
    log_action(f"{ctx.author} đã sử dụng lệnh /type với văn bản: {text}")
    pyautogui.typewrite(text)
    await ctx.send(f"Đã nhập văn bản: {text}")

@bot.command(name="press")
async def press_key(ctx, key: str):
    log_action(f"{ctx.author} đã sử dụng lệnh /press với phím: {key}")
    pyautogui.press(key)
    await ctx.send(f"Đã nhấn phím: {key}")

# Mở ứng dụng hoặc trang web
@bot.command(name="openweb")
async def open_web(ctx, url: str):
    log_action(f"{ctx.author} đã sử dụng lệnh /openweb với URL: {url}")
    webbrowser.open(url)
    await ctx.send(f"Đã mở trang web: {url}")

@bot.command(name="openapp")
async def open_app(ctx, app_path: str):
    log_action(f"{ctx.author} đã sử dụng lệnh /openapp với đường dẫn: {app_path}")
    try:
        subprocess.Popen(app_path)
        await ctx.send(f"Đã mở ứng dụng: {app_path}")
    except Exception as e:
        await ctx.send(f"Có lỗi xảy ra: {e}")

# Gửi tin nhắn định kỳ
@bot.command(name="remind")
async def remind(ctx, seconds: int, *, message: str):
    log_action(f"{ctx.author} đã sử dụng lệnh /remind với thời gian: {seconds} giây và nội dung: {message}")
    await ctx.send(f"Đã đặt lời nhắc sau {seconds} giây.")
    await asyncio.sleep(seconds)
    await ctx.send(f"⏰ Lời nhắc: {message}")

# Xử lý lỗi
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Bạn không có quyền sử dụng lệnh này.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Lệnh không tồn tại. Gõ `/menu` để xem danh sách lệnh.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Thiếu tham số. Vui lòng kiểm tra lại lệnh.")
    else:
        await ctx.send(f"Có lỗi xảy ra: {error}")

# Chạy bot
bot.run(TOKEN)