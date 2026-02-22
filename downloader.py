import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def get_user_inputs():
    # Initialize a hidden tkinter root window
    root = tk.Tk()
    root.withdraw()

    # 1. Ask for URL via a dialog box
    playlist_url = simpledialog.askstring("Input", "Paste the YouTube Playlist URL:", parent=root)
    if not playlist_url:
        return None, None, None

    # 2. Ask for Folder via a directory picker
    save_path = filedialog.askdirectory(title="Select Folder to Save Files")
    if not save_path:
        return None, None, None

    # 3. Ask for Format
    choice = simpledialog.askstring("Format", "Type '3' for MP3 or '4' for MP4:", parent=root)
    
    return playlist_url.strip(), save_path, choice

def download_media():
    playlist_url, save_path, choice = get_user_inputs()
    
    if not playlist_url or not save_path:
        print("Download cancelled: Missing URL or Path.")
        return

    # Base Configuration
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'noplaylist': False,
        'ffmpeg_location': r'C:\ffmpeg\bin',
        # --- FIX: Skip unavailable/private videos instead of crashing ---
        'ignoreerrors': True, 
        'quiet': False,
        'no_warnings': False,
    }

    # Apply Format Logic
    if choice == '3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        })

    # Execute Download
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\nProcessing playlist. Skipping unavailable videos...\n")
            ydl.download([playlist_url])
            messagebox.showinfo("Success", "Download process completed!")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    download_media()