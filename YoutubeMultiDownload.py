import subprocess
import sys

try:  # Checks if ytdl is installed- installs if unavailable
    import youtube_dl
except ImportError as e:
    missing_pkg = 'youtube-dl'
    print("You're missing package: " + missing_pkg + " Installing... (This will take a while)\n\n")
    subprocess.check_call([sys.executable, "-m", "pip", "install", missing_pkg])
    import youtube_dl

try:  # Checks if moviepy is installed- installs if unavailable
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
except ImportError as e:
    missing_pkg = 'moviepy'
    print("You're missing package: "+missing_pkg+" Installing... (This will take a while)\n\n")
    subprocess.check_call([sys.executable, "-m", "pip", "install", missing_pkg])
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

import os

links = open("links.txt", "r")
for line in links.readlines():
    info = line.split(" ")
    link = info[0]
    time_info = info[1].split(":")
    time_m = int(time_info[0])
    time_s = int(time_info[1])
    time = time_m * 60 + time_s

    time_d = 4.25  # Time delta (time between timestamp and end of clip)
    time_b = 2  # Time buffer (time between beginning of clip and timestamp)

    ydl_opts = {"outtmpl": f"{link[-5:]}"}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
        except Exception as ex:
            print("*" * 40)
            print(f"not able to download {link}")
            print(ex)
            print("*" * 40)
        try:
            print(time_m, time_s)
            for vid in os.listdir():
                if vid.endswith(f"{link[-5:]}.mp4"):
                    ffmpeg_extract_subclip(f"{vid}", time - time_b,
                                           time + time_d, targetname=f"00{link[-8:]}.mp4")
                    os.remove(f"{vid}")
                elif vid.endswith(f"{link[-5:]}.mkv"):
                    ffmpeg_extract_subclip(f"{vid}", time - time_b,
                                           time + time_d, targetname=f"00{link[-8:]}.mkv")
                    os.remove(f"{vid}")
        except Exception as ex:
            print("*" * 40)
            print("could not cut video")
            print(ex)
            print("*" * 40)

links.close()
input("done...")
