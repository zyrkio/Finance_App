import customtkinter as ctk
import sqlite3
from tkinter import StringVar, Canvas, Frame
from PIL import Image

class HomeScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        # Hauptfenster auf dunkel setzen
        self.configure(fg_color="#1E1E1E")  # Dunkler Hintergrund

        self.profile_var = StringVar(value="Benutzer auswählen")
        self.conn = sqlite3.connect('aktienbuchhaltung.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS profiles (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL)''')
        self.conn.commit()

        self.create_widgets()

    def create_widgets(self):
        # Oberes schmales Feld (Header)
        self.header_frame = ctk.CTkFrame(self, fg_color="#2C3E50", height=100)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)
        self.header_frame.grid_columnconfigure(2, weight=0)

        # Beispiel Widgets
        self.example_label = ctk.CTkLabel(self.header_frame, text="Aktien Buchhaltungsprogramm", font=("Arial", 20), text_color="white")
        self.example_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Profil Dropdown-Menü mit Datenbank-Verbindung
        self.profile_dropdown = ctk.CTkComboBox(self.header_frame, variable=self.profile_var, values=self.get_profiles())
        self.profile_dropdown.grid(row=0, column=2, padx=10, pady=20, sticky="e")

        # Content Frame mit Canvas für Scrollfunktion
        self.canvas = Canvas(self, bg="#333333")
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.scrollable_frame = Frame(self.canvas, bg="#333333")
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Beispielhafte Frames hinzufügen (Mehrere Frames für Scrollen)
        for i in range(10):  # Hier kannst du mehr Frames hinzufügen, um Scrollen zu testen
            frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#444444", height=300, width=1000)
            frame.grid(row=i, column=0, pady=20, padx=20, sticky="ew")
            label = ctk.CTkLabel(frame, text=f"Frame {i+1}", text_color="white")
            label.pack(pady=10)

        # Layout-Konfiguration
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def get_profiles(self):
        """Lädt alle Profile aus der Datenbank und gibt eine Liste zurück."""
        self.cursor.execute('SELECT id, name FROM profiles')
        profiles = self.cursor.fetchall()
        if profiles:
            return [f"{profile[1]} (ID: {profile[0]})" for profile in profiles]
        else:
            return ["Keine Profile gefunden"]


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x800")
    app = HomeScreen(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
