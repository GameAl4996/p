import os
import cv2
import shutil
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy import VideoFileClip

def convert_video(video_path, output_zip):
    temp_folder = "temp_extraction"
    os.makedirs(temp_folder, exist_ok=True)
    frames_folder = os.path.join(temp_folder, "frames")
    os.makedirs(frames_folder, exist_ok=True)

    # Extraction des images
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(frames_folder, f"frame_{frame_count:05d}.png")
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    cap.release()

    # Extraction de l'audio
    video = VideoFileClip(video_path)
    audio_path = os.path.join(temp_folder, "audio.mp3")
    video.audio.write_audiofile(audio_path)

    # Création du fichier ZIP
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_folder):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, temp_folder)
                zipf.write(full_path, arcname=relative_path)

    shutil.rmtree(temp_folder)

def browse_video():
    filepath = filedialog.askopenfilename(filetypes=[("Fichiers vidéo", "*.mp4 *.avi *.mov *.mkv")])
    if filepath:
        entry_video.delete(0, tk.END)
        entry_video.insert(0, filepath)

def convert_action():
    video_path = entry_video.get()
    if not os.path.isfile(video_path):
        messagebox.showerror("Erreur", "Fichier vidéo invalide.")
        return

    zip_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Fichier ZIP", "*.zip")])
    if zip_path:
        try:
            convert_video(video_path, zip_path)
            messagebox.showinfo("Succès", f"Conversion terminée.\nZIP : {zip_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")

# Interface graphique
root = tk.Tk()
root.title("Convertisseur vidéo vers ZIP (Images + Audio)")

tk.Label(root, text="Vidéo à convertir :").pack(pady=(10, 0))
frame = tk.Frame(root)
frame.pack(padx=10, pady=5)

entry_video = tk.Entry(frame, width=50)
entry_video.pack(side=tk.LEFT, padx=(0, 5))
btn_browse = tk.Button(frame, text="Parcourir", command=browse_video)
btn_browse.pack(side=tk.LEFT)

btn_convert = tk.Button(root, text="Convertir", command=convert_action, bg="#4CAF50", fg="white")
btn_convert.pack(pady=20)

root.mainloop()
