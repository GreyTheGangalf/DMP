# DMP Downloader 🚀

A modern, hybrid, and multi-threaded Download Manager built with Python and CustomTkinter. 

DMP Downloader is not just a simple URL fetcher; it features an intelligent routing architecture that automatically analyzes network requests and selects the best underlying engine to download the content at maximum speed.

## ✨ Features

* **🧠 Smart Routing Architecture:** Automatically performs an HTTP `HEAD` request to analyze the `Content-Type`. It dynamically routes the traffic to the appropriate download engine without requiring user intervention.
* **⚡ Multi-Threaded Engine (IDM Style):** For direct file links (`.exe`, `.zip`, `.mp4`), the app utilizes a custom-built multi-threaded engine. It calculates byte ranges, opens multiple parallel TCP connections, downloads file chunks simultaneously, and merges them to maximize bandwidth utilization.
* **🎥 Advanced Video Extraction:** For complex platforms (YouTube, Twitter/X, Instagram, Yandex, etc.), it seamlessly integrates with the `yt-dlp` backend, bypassing anti-bot protections and extracting media flawlessly.
* **🛑 Safe Cancellation:** Implements thread-safe `Event` flags allowing users to instantly cancel and clean up temporary `.part` files during an active download without crashing the UI.
* **🎨 Modern GUI:** A sleek, dark-mode ready, and responsive graphical user interface built with `CustomTkinter`.
* **📦 Standalone Executable:** Can be compiled into a single `.exe` file, running seamlessly without requiring a Python environment or exposing the terminal console.

## 🛠️ Tech Stack

* **Language:** Python 3.12+
* **GUI Framework:** CustomTkinter
* **Network/HTTP:** Requests
* **Media Extraction:** yt-dlp
* **Concurrency:** Python native `threading` module

## 🚀 Installation & Usage

### Option 1: Running from source

1.  Clone the repository:
    ```bash
    git clone [https://github.com/GreyTheGangalf/DMP-Downloader.git](https://github.com/GreyTheGangalf/DMP-Downloader.git)
    cd DMP-Downloader
    ```
2.  Install the required dependencies:
    ```bash
    pip install requests yt-dlp customtkinter
    ```
3.  Run the application:
    ```bash
    python main.py
    ```

### Option 2: Building the Standalone Executable

If you want to build the `.exe` file for Windows:
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --collect-all customtkinter main.py


🧠 How the Hybrid Router Works
Whitelist Check: The provided URL is checked against known heavy-media platforms (YouTube, X, Instagram). If matched, it's immediately passed to the yt-dlp engine.

Network Probe: If the domain is unknown, the router sends a lightweight HEAD request using a mock User-Agent.

Content-Type Decision: * If the server returns text/html, it assumes a media player is hidden inside and routes to yt-dlp.

If it returns a file format (e.g., application/octet-stream), it triggers the custom Multi-Threaded Engine to download the file in 4 parallel chunks.

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

📝 License
This project is open-source and available under the MIT License.<img width="737" height="527" alt="Ekran görüntüsü 2026-06-19 005422" src="https://github.com/user-attachments/assets/49f0d90e-38be-4506-bb0f-03b6c1d6683e" />
<img width="740" height="527" alt="image" src="https://github.com/user-attachments/assets/44082058-4217-4c4f-a005-d6caed44d005" />
