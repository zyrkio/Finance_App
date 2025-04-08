import customtkinter as ctk
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from threading import Thread
import time

class StockPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Master Frame Konfiguration
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.tickers = [
            "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN",
            "NVDA", "META", "NFLX", "AMD", "INTC",
            "BABA", "V", "JPM", "DIS", "KO",
            "PEP", "XOM", "MCD", "NKE", "PFE"
        ]
        
        self.update_interval = 20
        self.header_labels = ["Stock", "Last", "Change", "% Change", "High", "Low", "Volume", "Show Chart"]

        self.chart_frames = {}

        # Canvas mit Scrollbar
        self.canvas = ctk.CTkCanvas(self, borderwidth=0, highlightthickness=0, bg="#2C3E50")
        self.scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_table()

        self.update_thread = Thread(target=self.update_data)
        self.update_thread.daemon = True
        self.update_thread.start()

    def create_table(self):
        for col, header in enumerate(self.header_labels):
            header_label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 12, "bold"), padx=5, pady=5)
            header_label.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        self.data_labels = {}
        for row, ticker in enumerate(self.tickers, start=1):
            self.data_labels[ticker] = {}

            for col, header in enumerate(self.header_labels[:-1]):
                label = ctk.CTkLabel(self.scrollable_frame, text="Loading...", font=("Arial", 10), padx=5, pady=5)
                label.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
                self.data_labels[ticker][header] = label

            show_chart_button = ctk.CTkButton(self.scrollable_frame, text="Toggle Chart", 
                                              command=lambda t=ticker, r=row: self.toggle_chart(t, r))
            show_chart_button.grid(row=row, column=len(self.header_labels)-1, padx=5, pady=5, sticky="ew")
            self.data_labels[ticker]["Show Chart"] = show_chart_button

    def update_data(self):
        while True:
            for ticker in self.tickers:
                try:
                    stock = yf.Ticker(ticker)
                    data = stock.history(period="1d", interval="1m").iloc[-1]
                    
                    last_price = round(data["Close"], 2)
                    high = round(data["High"], 2)
                    low = round(data["Low"], 2)
                    volume = int(data["Volume"])
                    
                    prev_close = stock.history(period="2d").iloc[-2]["Close"]
                    change = round(last_price - prev_close, 2)
                    percent_change = round((change / prev_close) * 100, 2)
                    
                    self.after(0, self.update_labels, ticker, last_price, change, percent_change, high, low, volume)
                    
                except Exception as e:
                    print(f"Fehler beim Abrufen von {ticker}: {e}")

            time.sleep(self.update_interval)

    def update_labels(self, ticker, last_price, change, percent_change, high, low, volume):
        try:
            self.data_labels[ticker]["Stock"].configure(text=ticker)
            self.data_labels[ticker]["Last"].configure(text=f"{last_price} CHF")
            self.data_labels[ticker]["Change"].configure(text=f"{change} CHF")
            self.data_labels[ticker]["% Change"].configure(text=f"{percent_change} %")
            self.data_labels[ticker]["High"].configure(text=f"{high} CHF")
            self.data_labels[ticker]["Low"].configure(text=f"{low} CHF")
            self.data_labels[ticker]["Volume"].configure(text=f"{volume}")
        except KeyError:
            print(f"Fehler beim Aktualisieren der Labels für {ticker}")

    def toggle_chart(self, ticker, row):
        if ticker in self.chart_frames:
            self.chart_frames[ticker].destroy()
            del self.chart_frames[ticker]
        else:
            chart_frame = ctk.CTkFrame(self.scrollable_frame)
            chart_frame.grid(row=row+1, column=0, columnspan=len(self.header_labels), sticky="nsew", padx=5, pady=5)
            self.chart_frames[ticker] = chart_frame

            self.load_chart(ticker, chart_frame)

    def load_chart(self, ticker, frame):
        stock = yf.Ticker(ticker)
        data = stock.history(period="1mo")

        if data.empty:
            print(f"Keine Daten für {ticker}")
            return

        plt.figure(figsize=(6, 4))
        plt.plot(data["Close"], label=f"{ticker} Kursverlauf")
        plt.title(f"{ticker} Kursverlauf über 1 Monat")
        plt.xlabel("Datum")
        plt.ylabel("Preis in CHF")
        plt.legend()
        plt.grid(True)

        chart = FigureCanvasTkAgg(plt.gcf(), master=frame)
        chart.draw()
        chart.get_tk_widget().pack(fill="both", expand=True)
        plt.clf()
