import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from yt_dlp import YoutubeDL
import json

CONFIG_FILE = "config.json"

def load_config():
    """
    Load the selected folder path from the configuration file.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config.get("download_folder", "")
    return ""

def save_config(folder_path):
    """
    Save the selected folder path to the configuration file.
    """
    config = {"download_folder": folder_path}
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

def download_mp3():
    url = entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    try:
        # Getter for the selected download folder
        download_folder = folder_path.get()
        if not download_folder:
            messagebox.showerror("Error", "Please select a download folder.")
            return

        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Save to selected folder
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Extract audio
                'preferredcodec': 'mp3',      # Convert to MP3
                'preferredquality': '192',    # Set audio quality
            }],
            'progress_hooks': [update_progress],  #progress hook
        }

        # Disable the download button during download
        button.config(state=tk.DISABLED)

        # Start the download
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", "Downloaded and converted to MP3!")
        os.startfile(download_folder)  # Open the download folder
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        # Re-enable the download button
        button.config(state=tk.NORMAL)
        progress_bar['value'] = 0  # Reset progress bar
        progress_label.config(text="0%")  # Reset progress label

def update_progress(d):
    """
    Callback function to update the progress bar and label.
    """
    if d['status'] == 'downloading':
        # Calculate progress percentage
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        if total_bytes:
            downloaded_bytes = d['downloaded_bytes']
            progress = (downloaded_bytes / total_bytes) * 100
            progress_bar['value'] = progress
            progress_label.config(text=f"{int(progress)}%")  # Update progress label
            root.update_idletasks()  # Update the GUI

def select_folder():
    """
    Open a dialog to select the download folder.
    """
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)
        save_config(folder_selected)  # Save the selected folder to the config file

# main window
root = tk.Tk()
root.title("YouTube to MP3 Downloader")

# Load the previously selected folder (if any)
folder_path = tk.StringVar(value=load_config())

#input field
label = tk.Label(root, text="Enter YouTube URL:")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

#folder selection button and label
folder_label = tk.Label(root, text="Download Folder:")
folder_label.pack(pady=5)

folder_entry = tk.Entry(root, textvariable=folder_path, width=50, state='readonly')
folder_entry.pack(pady=5)

select_folder_button = tk.Button(root, text="Select Folder", command=select_folder)
select_folder_button.pack(pady=5)

#download button
button = tk.Button(root, text="Download MP3", command=download_mp3)
button.pack(pady=10)

#progress bar
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')
progress_bar.pack(pady=10)

#progress percentage label
progress_label = tk.Label(root, text="0%")
progress_label.pack(pady=5)

# Run
root.mainloop()