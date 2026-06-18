import yt_dlp
import customtkinter as ctk
import threading
from downloader import dmp_downloader
import requests
import os

dest_folder = os.path.join(os.path.expanduser("~"), "Downloads", "DMP_Downloads")

if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

os.chdir(dest_folder)

cancel_flag = threading.Event()

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
    def progress_hook(d):
        if cancel_flag.is_set():
            raise Exception("Cancelled")
    
    settings={
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',

        'outtmpl': 'vids/%(title)s.%(ext)s',

        'concurrent_fragment_downloads': 5,

        'quiet': False, 
        'no_warnings': True,
        'progress_hooks': [download_process,progress_hook],
        'nopart':False,
    }

    try:
        with yt_dlp.YoutubeDL(settings) as ydl:
            ydl.download([target_url])

        if not cancel_flag.is_set():
            print("\n[SUCCESS] yt-dlp download is complete!")
            status_label.configure(text="✅ Video downloaded!")
    
    except Exception as e:
        if "Cancelled" in str(e):
            print("\n[CLEANİNG] yt-dlp download cancelled!")
            status_label.configure(text="❌ Download cancelled.")
        else:
            print(f"\n[Error] yt-dlp has run to an error: {e}")
            status_label.configure(text="Error: Can't download the video.")

def smart_router(url):
    print("\n [Router] Communicating with server...")


    platforms=["youtube.com", "youtu.be", "twitter.com", "x.com", "instagram.com", "tiktok.com", "vimeo.com", "reddit.com", "yandex"]

    if any(site in url for site in platforms):
        print("[ROUTER] Link is from common platforms. yt-dlp ")
        video_download(url)
        return
        
    try:
        agent_Headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

        agent_Answer = requests.head(url, allow_redirects=True,timeout=5,headers=agent_Headers)

        content_type = answer.headers.get('Content-Type','').lower()
        print(f"[Router] Content type: {content_type}")

        if 'text/html' in content_type:
            print("[ROUTER] HTML detected. yt-dlp")
            video_download(url)
        else:
            print("[ROUTER] media file detected. DMP-Downloader")
            dmp_downloader(url,4,cancel_flag)

    except Exception as e:
        print(f"[ROUTER] Couldn't anaylze the file. {e}"),


def cancel_download():
    status_label.configure(text="Canceling... Please wait.")
    cancel_flag.set()

cancel_flag.clear()

def download_button_clicked():
    selected_url = url__input.get().strip()

    if selected_url.startswith("http"):
        status_label.configure(text= "Analyzing connection on network...")

        worker = threading.Thread(target=smart_router,args=(selected_url,))
        worker.start()
    else:
        print("Invalid URL. Try again")

def open_folder():
    current_folder = os.getcwd()

    try:
        os.startfile(current_folder)
        status_label.configure(text="📁 Downloads folder opened.")
    except Exception as e:
        status_label.configure(text=f"Error: File couldn't open ({e})")

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

folder_button = ctk.CTkButton(
    app,
    text="📁 Open Downloads",
    command=open_folder,
    fg_color="#4A4D50",    
    hover_color="#3b3d3f"
)
folder_button.pack(pady=5)

cancel_button = ctk.CTkButton(
    app,
    text="❌ Cancel",
    command= cancel_download,
    fg_color="#8B0000",      
    hover_color="#a30000"    
)
cancel_button.pack(pady=5)

app.mainloop()
