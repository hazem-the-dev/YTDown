import tkinter as tk
import yt_dlp as youtube_dl
from tkinter import messagebox
import os 
from moviepy import VideoFileClip, AudioFileClip
from moviepy import VideoFileClip


def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showrror("Error", "Please enter a valid Youtube URL")
        return
    try:
        # first we download the video
        ydl_opts_video = {
            'format': 'bestvideo[ext=mp4]',
            'outtmpl': '%(title)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts_video) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_file = f"{info_dict['title']}.mp4"
            print(f"Downloaded video {video_file}")

        # second we download the audio
        ydl_opts_audio = {
            'format': 'bestaudio[ext=webm]',
            'outtmpl': '%(title)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts_audio) as ydl:
            audio_file = f"{info_dict['title']}.webm"
            print(f"Starting download for audio {audio_file}")
            ydl.download([url])

    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")
        print("Error details:", e)
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)

    video_clip = video_clip.set_audio(audio_clip)

    output_file = f"{url.split('=')[-1]}_merged.mp4"
    video_clip.write_videofile(output_file, codec='libx264')

    os.remove(video_file)
    os.remove(audio_file)

    messagebox.showinfo("Success","Download and merging complete")

root = tk.Tk()
print("Created root window")

root.title("Youtube Video Downloader")
root.geometry("400x200")


url_label = tk.Label(root, text="Enter Youtube URL: ")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

download_btn = tk.Button(root, text="Download", command=download_video)
download_btn.pack(pady=20)

print("Starting GUI")
root.mainloop()