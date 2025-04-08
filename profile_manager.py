import customtkinter as ctk
import sqlite3

class ProfileManager(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.conn = sqlite3.connect('aktienbuchhaltung.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS profiles (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL)''')
        self.conn.commit()
        
        self.current_profile_id = None

        # Hauptlayout einrichten
        self.grid_rowconfigure(0, weight=5)  # Großes Info-Feld
        self.grid_rowconfigure(1, weight=0)  # Schmales Button-Feld
        self.grid_columnconfigure(0, weight=1)

        # Großes Informationsfeld (oben)
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        self.profile_info_label = ctk.CTkLabel(self.info_frame, text="Benutzerinformationen", font=("Arial", 18))
        self.profile_info_label.pack(pady=10)

        self.profile_data_label = ctk.CTkLabel(self.info_frame, text="Keine Daten geladen", font=("Arial", 14))
        self.profile_data_label.pack(pady=10)

        # Schmales Button-Feld (unten)
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        self.entry_name = ctk.CTkEntry(self.button_frame, placeholder_text="Neuer Benutzername")
        self.entry_name.grid(row=0, column=0, padx=10, pady=10)

        self.button_create = ctk.CTkButton(self.button_frame, text="Neuen Benutzer erstellen", command=self.create_profile)
        self.button_create.grid(row=0, column=1, padx=10, pady=10)

        self.profile_toggle = ctk.CTkOptionMenu(self.button_frame, values=self.get_profile_names(), command=self.load_profile)
        self.profile_toggle.grid(row=0, column=2, padx=10, pady=10)

    def create_profile(self):
        name = self.entry_name.get()
        if name:
            self.cursor.execute('INSERT INTO profiles (name) VALUES (?)', (name,))
            self.conn.commit()
            self.entry_name.delete(0, ctk.END)
            self.profile_toggle.configure(values=self.get_profile_names())
            print(f'Profil "{name}" wurde erstellt.')
        else:
            print("Bitte einen Profilnamen eingeben.")

    def get_profile_names(self):
        self.cursor.execute('SELECT id, name FROM profiles')
        profiles = self.cursor.fetchall()
        return [f"{profile[1]} (ID: {profile[0]})" for profile in profiles]

    def load_profile(self, selected_profile):
        profile_id = int(selected_profile.split("ID: ")[1].strip(")"))
        self.cursor.execute('SELECT * FROM profiles WHERE id = ?', (profile_id,))
        profile = self.cursor.fetchone()

        if profile:
            self.current_profile_id = profile[0]
            self.profile_data_label.configure(text=f"Profil: {profile[1]}")
            print(f'Profil "{profile[1]}" wurde geladen.')
        else:
            self.profile_data_label.configure(text="Keine Daten gefunden")
