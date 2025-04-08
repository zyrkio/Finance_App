import customtkinter as ctk
from home_screen import HomeScreen
from stock_page import StockPage
from profile_manager import ProfileManager

class Sidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=200)
        self.master = master

        self.grid_rowconfigure(4, weight=1)

        # Buttons für Navigation
        self.home_button = self.create_button("Home", self.load_home)
        self.home_button.grid(row=0, column=0, padx=20, pady=10)

        self.stocks_button = self.create_button("Generelle Aktien", self.load_stocks)
        self.stocks_button.grid(row=1, column=0, padx=20, pady=10)

        self.profile_button = self.create_button("Benutzerkonto", self.load_profile)
        self.profile_button.grid(row=2, column=0, padx=20, pady=10)

    def create_button(self, text, command):
        button = ctk.CTkButton(self, text=text, command=command, width=180, hover_color="#6272a4")
        return button

    def load_home(self):
        self.clear_content_frame()
        HomeScreen(self.master.content_frame).pack(fill="both", expand=True)

    def load_stocks(self):
        self.clear_content_frame()
        StockPage(self.master.content_frame).pack(fill="both", expand=True)

    def load_profile(self):
        self.clear_content_frame()
        ProfileManager(self.master.content_frame).pack(fill="both", expand=True)

    def clear_content_frame(self):
        for widget in self.master.content_frame.winfo_children():
            widget.destroy()
