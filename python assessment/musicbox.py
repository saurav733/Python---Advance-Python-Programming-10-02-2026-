import os
import tkinter as tk
from tkinter import messagebox

# Create playlists folder if not exists
if not os.path.exists("playlists"):
    os.makedirs("playlists")


# Playlist Class (OOP)
class Playlist:

    def __init__(self, name, songs):
        self.name = name
        self.songs = songs

    def save(self):
        try:
            if not self.name.strip():
                raise ValueError("Playlist name cannot be empty")

            if not self.songs.strip():
                raise ValueError("Song list cannot be empty")

            filename = f"playlists/playlist_{self.name}.txt"

            if os.path.exists(filename):
                raise FileExistsError("Playlist already exists")

            with open(filename, "w") as file:
                file.write(self.songs)

            return True

        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False

    @staticmethod
    def load(name):
        try:
            filename = f"playlists/playlist_{name}.txt"

            with open(filename, "r") as file:
                return file.read()

        except FileNotFoundError:
            messagebox.showerror("Error", "Playlist not found")
            return ""


# Main App Class
class MusicBoxApp:

    def __init__(self, root):
        self.root = root
        self.root.title("MusicBox")
        self.root.geometry("600x400")

        # Playlist Name
        tk.Label(root, text="Playlist Name:").pack()
        self.name_entry = tk.Entry(root, width=40)
        self.name_entry.pack()

        # Songs Text Area
        tk.Label(root, text="Songs (one per line):").pack()
        self.song_text = tk.Text(root, height=10, width=50)
        self.song_text.pack()

        # Save Button
        tk.Button(root, text="Save Playlist", command=self.save_playlist).pack(pady=5)

        # Playlist Listbox
        tk.Label(root, text="Saved Playlists:").pack()

        self.listbox = tk.Listbox(root)
        self.listbox.pack(fill="both", expand=True)

        self.listbox.bind("<<ListboxSelect>>", self.display_playlist)

        # Load existing playlists
        self.load_playlists()

    def save_playlist(self):

        name = self.name_entry.get()
        songs = self.song_text.get("1.0", tk.END).strip()

        playlist = Playlist(name, songs)

        if playlist.save():
            messagebox.showinfo("Success", "Playlist saved successfully")
            self.load_playlists()

    def load_playlists(self):

        self.listbox.delete(0, tk.END)

        try:
            files = os.listdir("playlists")

            for file in files:
                if file.startswith("playlist_") and file.endswith(".txt"):
                    name = file.replace("playlist_", "").replace(".txt", "")
                    self.listbox.insert(tk.END, name)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_playlist(self, event):

        selection = self.listbox.curselection()

        if selection:
            name = self.listbox.get(selection[0])
            songs = Playlist.load(name)

            self.song_text.delete("1.0", tk.END)
            self.song_text.insert(tk.END, songs)


# Run App
root = tk.Tk()
app = MusicBoxApp(root)
root.mainloop()





































































