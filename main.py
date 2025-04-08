import customtkinter as ctk
from sidebar import Sidebar
from home_screen import HomeScreen

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AktienBuchhaltungsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Aktien Buchhaltungsprogramm")
        self.geometry("1200x800")

        # Sidebar hinzufügen
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        # Frame für Seiteninhalte (HIER ist dein Fehler!)
        self.content_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # HomeScreen wird direkt geladen
        self.show_home_screen()

    def show_home_screen(self):
        # Vorherige Inhalte löschen
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # HomeScreen anzeigen
        home_screen = HomeScreen(self.content_frame)
        home_screen.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)


if __name__ == "__main__":
    app = AktienBuchhaltungsApp()
    app.mainloop()
