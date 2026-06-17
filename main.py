import yt_dlp
import customtkinter as ctk
import threading

def download_process(data):
    if data['status'] == 'downloading':
        progress = data.get('_percent_str', '0%').strip()
        speed = data.get('_speed_str', '0B/s').strip()

        status_label.configure(text=f"Downloading: {progress} | Speed: {speed}")

        downloaded_bytes = data.get('downloaded_bytes',0)

        total_bytes = data.get('total_bytes') or data.get('total_bytes_estimate', 1)

        if total_bytes > 0 :
            rate = downloaded_bytes / total_bytes
            progress_label.set(rate)

    elif data['status'] == 'finished':
        print("\n Download complete, merging pieces")
        progress_label.set(1.0)


def video_download(target_url):
    settings={
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',

        'outtmpl': 'vids/%(title)s.%(ext)s',

        'concurrent_fragment_downloads': 5,

        'quiet': False, 
        'no_warnings': True,
        'progress_hooks': [download_process],
    }

    with yt_dlp.YoutubeDL(settings) as ydl:
        ydl.download([target_url])

def download_button_clicked():
    selected_url = url__input.get()

    if selected_url.startswith("http"):
        print("Starting download in background")

        worker = threading.Thread(target=video_download,args=(selected_url,))

        worker.start()
    else:
        print("Invalid URL. Try again")

# video_URL = input("Enter the video's URL:")

# if video_URL.startswith("http"):
#     print("Link accepted,processing.")
#     video_download(video_URL)
# else:
#     print("Error: Invalid Link.")


app = ctk.CTk()
app.title("DMP - Download Manager")
app.geometry("600x400")

header = ctk.CTkLabel(app, text="DMP- Video Downloader", font=("Arial",20,"bold"))
header.pack(pady=(30,20))

url__input = ctk.CTkEntry(app, width=400,height=20,placeholder_text="Enter Video URL")
url__input.pack(pady=10)

download_button = ctk.CTkButton(app, text="Start Download", width=200,height=40, command=download_button_clicked)
download_button.pack(pady=20)

status_label = ctk.CTkLabel(app, text="Status:Waiting...",font=("Arial",12))
status_label.pack(pady=10)

progress_label = ctk.CTkProgressBar(app, width=400)
progress_label.set(0)
progress_label.pack(pady=10)

app.mainloop()
