import subprocess
import sys
import os

try:  # Checks if ytdl is installed- installs if unavailable
    import youtube_dl
except ImportError as e:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'youtube-dl'])
    import youtube_dl

try:  # Checks if moviepy is installed- installs if unavailable
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
except ImportError as e:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'moviepy'])
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

links = None

try:
    links = open("links.txt", "r")
except FileNotFoundError as e:
    input(
        "Unable to start! Make sure you create a file called: 'links.txt' in this SAME folder as this program!\nPress "
        "any key to exit")
    sys.exit(-1)

for line in links.readlines():
    info = line.split(" ")
    link = info[0]

    ydl_opts = {"outtmpl": f"{link[-5:]}.mp4"}  # Fix file extension not being appended

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
        except youtube_dl.utils.DownloadError as ex:
            input("\nThis link does not work: " + f"{link}")
            sys.exit(-1)

    video = None

    for timestamp in info[1:]:
        try:
            time_info = timestamp.split(":")
            time_m = int(time_info[0])
            time_s = int(time_info[1])
            time = time_m * 60 + time_s
        except:
            print("\nCould not read the given timestamps\nbe sure to write them correctly in the links.txt file\n")
            sys.exit(-1)
        # Measured in seconds
        time_d = 4.25  # Time delta (time between timestamp and end of clip)
        time_b = 2  # Time buffer (time between beginning of clip and timestamp)

        try:
            print(time_m, time_s)
            i = 0
            for vid in os.listdir():
                if vid.endswith(f"{link[-5:]}.mp4"):
                    while f"00{link[-8:]}{i}.mp4" in os.listdir():
                        i += 1
                    ffmpeg_extract_subclip(f"{vid}", time - time_b,
                                           time + time_d, targetname=f"00{link[-8:]}{i}.mp4")
                    video = vid
                elif vid.endswith(f"{link[-5:]}.mkv"):
                    while f"00{link[-8:]}{i}.mkv" in os.listdir():
                        i += 1
                        print(os.listdir())
                    ffmpeg_extract_subclip(f"{vid}", time - time_b,
                                           time + time_d, targetname=f"00{link[-8:]}{i}.mkv")
                    video = vid
        except IOError as ex:
            input("\nCould not run! There was a video with the same filename '" + f"{link[-5:]}.mp4" + "' inside this "
                                                                                                       "folder\nPress "
                                                                                                       "any key to "
                                                                                                       "exit")
            sys.exit(-1)
        except:
            input("\nSomething went wrong\nCould not cut video")
            sys.exit(-1)
    os.remove(f"{video}")

links.close()
input("\nDone!")
