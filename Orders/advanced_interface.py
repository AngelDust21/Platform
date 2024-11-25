# advanced_interface.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from orders import OrderManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

class AdvancedInterface:
    def __init__(self, master, order_manager):
        self.master = master
        self.order_manager = order_manager

        self.master.title("Geavanceerde Interface")
        self.master.geometry("1000x700")
        self.master.minsize(800, 600)

        # Configureer stijlen
        self.setup_styles()

        # Creëer notebook (tabbladen)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Voeg tabbladen toe
        self.create_statistics_tab()
        self.create_search_tab()
        self.create_settings_tab()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')  # Gebruik een modern thema

        # Pas de stijl van de tabbladen aan
        style.configure("TNotebook.Tab", font=("Arial", 10))
        style.map("TNotebook.Tab", background=[("selected", "#ADD8E6")])

        # Style voor Treeview
        style.configure("Treeview", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

    def create_statistics_tab(self):
        statistics_tab = ttk.Frame(self.notebook)
        self.notebook.add(statistics_tab, text="Statistieken")

        # Frame voor datum selectie
        date_frame = ttk.Frame(statistics_tab)
        date_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Label(date_frame, text="Selecteer Datum:").pack(side=tk.LEFT, padx=5)
        self.stats_date_entry = DateEntry(date_frame, date_pattern='dd/MM/yy')
        self.stats_date_entry.pack(side=tk.LEFT, padx=5)

        refresh_button = ttk.Button(date_frame, text="Vernieuw Grafiek", command=self.plot_daily_data)
        refresh_button.pack(side=tk.LEFT, padx=5)

        # Canvas voor de grafiek
        self.figure = plt.Figure(figsize=(8,6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=statistics_tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initialiseer de grafiek met de huidige datum
        self.plot_daily_data()

    def plot_daily_data(self):
        self.ax.clear()
        selected_date = self.stats_date_entry.get_date().strftime("%d/%m/%y")
        summary = self.order_manager.get_detailed_summary_by_dates([selected_date])

        if not summary:
            self.ax.text(0.5, 0.5, 'Geen data beschikbaar voor deze datum', horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
        else:
            items = list(summary.keys())
            totals = list(summary.values())

            self.ax.barh(items, totals, color="#76B947")
            self.ax.set_xlabel('Aantal')
            self.ax.set_title(f'Samenvatting van Bestellingen op {selected_date}')

        self.canvas.draw()

    def create_search_tab(self):
        search_tab = ttk.Frame(self.notebook)
        self.notebook.add(search_tab, text="Zoek Bestellingen")

        # Zoek frame
        search_frame = ttk.Frame(search_tab)
        search_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Label(search_frame, text="Zoekterm:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Zoek", command=self.search_orders)
        search_button.pack(side=tk.LEFT, padx=5)

        # Resultaten Treeview
        columns = ("Bestelnummer", "Datum", "Tijd", "Kaas", "Aantal Kaas", "Opmerkingen Kaas",
                   "Vlees", "Aantal Vlees", "Opmerkingen Vlees", "Tapas", "Aantal Tapas",
                   "Raclette", "Aantal Raclette", "Brood", "Algemene Opmerkingen")
        self.search_tree = ttk.Treeview(search_tab, columns=columns, show='headings')
        self.search_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, minwidth=100, width=120, anchor='center')

    def search_orders(self):
        query = self.search_entry.get().strip().lower()
        results = self.order_manager.search_orders(query)

        # Verwijder bestaande items
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

        # Voeg nieuwe resultaten toe
        for order in results:
            self.search_tree.insert('', 'end', values=order.to_treeview_tuple())

    def create_settings_tab(self):
        settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(settings_tab, text="Instellingen")

        ttk.Label(settings_tab, text="Instellingen zijn hier nog niet beschikbaar.").pack(pady=20)

def create_advanced_interface(order_manager):
    """
    Creëert en opent de geavanceerde interface in een nieuw venster.
    """
    advanced_window = tk.Toplevel()
    AdvancedInterface(advanced_window, order_manager)
