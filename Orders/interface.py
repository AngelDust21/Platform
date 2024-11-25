# interface.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime
from orders import Order, OrderManager
from sort_orders import sort_orders_by_date_time
from export import export_orders_to_excel, import_orders_from_excel

class MainInterface:
    def __init__(self, root, order_manager):
        self.root = root
        self.order_manager = order_manager

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """
        Configureert de stijlen voor de ttk widgets.
        """
        style = ttk.Style()
        style.theme_use('clam')  # Modern thema

        # Definieer aangepaste stijlen indien nodig
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10))
        style.configure("Treeview", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

    def create_widgets(self):
        """
        Creëert alle widgets en plaatst ze in de interface.
        """
        # Hoofdframe binnen de root window
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Stel de rijen en kolommen van main_frame in voor grid
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=0)  # Order Invoer
        main_frame.rowconfigure(1, weight=0)  # Knoppen
        main_frame.rowconfigure(2, weight=1)  # Overzicht
        main_frame.rowconfigure(3, weight=0)  # Filter

        # Frame voor order invoer
        self.create_order_input_frame(main_frame)

        # Knoppen Frame
        self.create_buttons_frame(main_frame)

        # Overzicht Frame
        self.create_overview_frame(main_frame)

        # Filter Frame
        self.create_filter_frame(main_frame)

    def create_order_input_frame(self, parent):
        """
        Creëert de invoersecties voor bestellingen.
        """
        order_input_frame = ttk.LabelFrame(parent, text="Bestelling Invoer")
        order_input_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        # Configureer grid voor order_input_frame
        order_input_frame.columnconfigure(0, weight=1)
        order_input_frame.columnconfigure(1, weight=1)
        order_input_frame.columnconfigure(2, weight=1)
        order_input_frame.columnconfigure(3, weight=1)

        # Bestelnummer, Datum en Tijd
        top_frame = ttk.Frame(order_input_frame)
        top_frame.grid(row=0, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(3, weight=1)
        top_frame.columnconfigure(5, weight=1)
        top_frame.columnconfigure(6, weight=1)

        ttk.Label(top_frame, text="Bestelnummer:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.order_number_entry = ttk.Entry(top_frame)
        self.order_number_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        ttk.Label(top_frame, text="Datum:").grid(row=0, column=2, sticky='e', padx=5, pady=2)
        self.date_entry = DateEntry(top_frame, date_pattern='dd/MM/yy')
        self.date_entry.grid(row=0, column=3, sticky='w', padx=5, pady=2)

        ttk.Button(top_frame, text="Vandaag", command=self.set_current_date).grid(row=0, column=4, padx=5, pady=2)

        ttk.Label(top_frame, text="Tijd (UU:MM):").grid(row=0, column=5, sticky='e', padx=5, pady=2)
        self.time_entry = ttk.Entry(top_frame)
        self.time_entry.grid(row=0, column=6, sticky='ew', padx=5, pady=2)

        # Frame voor selectie van Kaas, Vlees, Tapas, Raclette
        selection_frame = ttk.Frame(order_input_frame)
        selection_frame.grid(row=1, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
        selection_frame.columnconfigure(0, weight=1)
        selection_frame.columnconfigure(1, weight=1)
        selection_frame.columnconfigure(2, weight=1)
        selection_frame.columnconfigure(3, weight=1)

        # Kaas Selectie
        self.create_cheese_selection(selection_frame, 0)

        # Vlees Selectie
        self.create_meat_selection(selection_frame, 1)

        # Tapas Selectie
        self.create_tapas_selection(selection_frame, 2)

        # Raclette Selectie
        self.create_raclette_selection(selection_frame, 3)

        # Brood Selectie
        self.create_bread_selection(order_input_frame)

        # Algemene Opmerkingen
        self.create_general_comments(order_input_frame)

    def create_cheese_selection(self, parent, column):
        """
        Creëert de kaas selectie sectie.
        """
        cheese_frame = ttk.LabelFrame(parent, text="Kaas Selectie")
        cheese_frame.grid(row=0, column=column, sticky='ew', padx=5, pady=5)
        cheese_frame.columnconfigure(1, weight=1)

        ttk.Label(cheese_frame, text="Kaas Type:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.cheese_var = tk.StringVar()
        cheese_options = [
            "", "Kaas Rok4 250", "Kaas Trad Dessert 150",
            "Kaas Tradi 250", "Kaas Alleen Rok4 250",
            "Kaas Alleen Trad 250", "Goudse Kaas 200", "Edammer Kaas 180"
        ]
        cheese_menu = ttk.OptionMenu(cheese_frame, self.cheese_var, cheese_options[0], *cheese_options)
        cheese_menu.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        ttk.Label(cheese_frame, text="Aantal Personen:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.cheese_people_entry = ttk.Entry(cheese_frame)
        self.cheese_people_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=2)

        ttk.Label(cheese_frame, text="Opmerkingen:").grid(row=2, column=0, sticky='e', padx=5, pady=2)
        self.cheese_comment_entry = ttk.Entry(cheese_frame)
        self.cheese_comment_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=2)

    def create_meat_selection(self, parent, column):
        """
        Creëert de vlees selectie sectie.
        """
        meat_frame = ttk.LabelFrame(parent, text="Vlees Selectie")
        meat_frame.grid(row=0, column=column, sticky='ew', padx=5, pady=5)
        meat_frame.columnconfigure(1, weight=1)

        ttk.Label(meat_frame, text="Vlees Type:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.meat_var = tk.StringVar()
        meat_options = ["", "Vlees Rok4 220", "Vlees Trad 200", "Kipfilet 180", "Biefstuk 250"]
        meat_menu = ttk.OptionMenu(meat_frame, self.meat_var, meat_options[0], *meat_options)
        meat_menu.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        ttk.Label(meat_frame, text="Aantal Personen:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.meat_people_entry = ttk.Entry(meat_frame)
        self.meat_people_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=2)

        ttk.Label(meat_frame, text="Opmerkingen:").grid(row=2, column=0, sticky='e', padx=5, pady=2)
        self.meat_comment_entry = ttk.Entry(meat_frame)
        self.meat_comment_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=2)

    def create_tapas_selection(self, parent, column):
        """
        Creëert de tapas selectie sectie.
        """
        tapas_frame = ttk.LabelFrame(parent, text="Tapas Selectie")
        tapas_frame.grid(row=0, column=column, sticky='ew', padx=5, pady=5)
        tapas_frame.columnconfigure(1, weight=1)

        ttk.Label(tapas_frame, text="Tapas Type:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.tapas_var = tk.StringVar()
        tapas_options = ["", "Tapas Rok4", "Tapas Trad", "Tapas Deluxe"]
        tapas_menu = ttk.OptionMenu(tapas_frame, self.tapas_var, tapas_options[0], *tapas_options)
        tapas_menu.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        ttk.Label(tapas_frame, text="Aantal:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.tapas_quantity_entry = ttk.Entry(tapas_frame)
        self.tapas_quantity_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=2)

    def create_raclette_selection(self, parent, column):
        """
        Creëert de raclette selectie sectie.
        """
        raclette_frame = ttk.LabelFrame(parent, text="Raclette Selectie")
        raclette_frame.grid(row=0, column=column, sticky='ew', padx=5, pady=5)
        raclette_frame.columnconfigure(1, weight=1)

        ttk.Label(raclette_frame, text="Raclette Type:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.raclette_var = tk.StringVar()
        raclette_options = ["", "Raclette Rok4", "Raclette Trad", "Raclette Deluxe"]
        raclette_menu = ttk.OptionMenu(raclette_frame, self.raclette_var, raclette_options[0], *raclette_options)
        raclette_menu.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        ttk.Label(raclette_frame, text="Aantal Personen:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.raclette_people_entry = ttk.Entry(raclette_frame)
        self.raclette_people_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=2)

    def create_bread_selection(self, parent):
        """
        Creëert de brood selectie sectie.
        """
        bread_frame = ttk.LabelFrame(parent, text="Brood Selectie")
        bread_frame.grid(row=2, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

        # Configureer grid voor bread_frame
        bread_frame.columnconfigure(tuple(range(10)), weight=1)

        ttk.Label(bread_frame, text="Selecteer Broodsoorten en Aantallen:").grid(row=0, column=0, columnspan=10, padx=5, pady=2)

        bread_types = [
            "Stokbrood", "Ciabatta", "Foret Noir", "Houthakkers", "Margot",
            "Spelt", "Zwitsers Meerzaden", "Notenbrood", "Kletsenbrood", "Krentenmix",
            "Volkoren", "Roggebrood", "Baguette", "Focaccia", "Pita"
        ]

        self.bread_entries = {}
        for idx, bread in enumerate(bread_types):
            ttk.Label(bread_frame, text=bread).grid(row=1, column=idx, sticky='w', padx=2, pady=2)
            entry = ttk.Entry(bread_frame, width=5)
            entry.grid(row=2, column=idx, padx=2, pady=2)
            self.bread_entries[bread] = entry

    def create_general_comments(self, parent):
        """
        Creëert de algemene opmerkingen sectie.
        """
        comments_frame = ttk.LabelFrame(parent, text="Algemene Opmerkingen")
        comments_frame.grid(row=3, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

        self.general_comment_entry = ttk.Entry(comments_frame, width=100)
        self.general_comment_entry.pack(fill=tk.X, padx=5, pady=2)

    def create_buttons_frame(self, parent):
        """
        Creëert de knoppen voor orderbeheer.
        """
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=1, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.columnconfigure(2, weight=1)
        buttons_frame.columnconfigure(3, weight=1)

        self.submit_button = ttk.Button(buttons_frame, text="Voeg Bestelling Toe", command=lambda: self.submit_order(is_update=False))
        self.submit_button.grid(row=0, column=0, sticky='ew', padx=5, pady=2)

        self.update_button = ttk.Button(buttons_frame, text="Update Bestelling", command=lambda: self.submit_order(is_update=True))
        self.update_button.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        self.update_button.state(['disabled'])

        self.delete_button = ttk.Button(buttons_frame, text="Verwijder Bestelling", command=self.delete_order)
        self.delete_button.grid(row=0, column=2, sticky='ew', padx=5, pady=2)

        self.import_button = ttk.Button(buttons_frame, text="Importeer Bestellingen", command=lambda: self.import_orders())
        self.import_button.grid(row=0, column=3, sticky='ew', padx=5, pady=2)

    def create_overview_frame(self, parent):
        """
        Creëert het overzicht van bestellingen in een Treeview.
        """
        overview_frame = ttk.LabelFrame(parent, text="Bestellingen Overzicht")
        overview_frame.grid(row=2, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

        # Configureer grid voor overview_frame
        overview_frame.columnconfigure(0, weight=1)
        overview_frame.rowconfigure(0, weight=1)

        columns = ("Bestelnummer", "Datum", "Tijd", "Kaas", "Aantal Kaas", "Opmerkingen Kaas",
                   "Vlees", "Aantal Vlees", "Opmerkingen Vlees", "Tapas", "Aantal Tapas",
                   "Raclette", "Aantal Raclette", "Brood", "Algemene Opmerkingen")
        self.tree = ttk.Treeview(overview_frame, columns=columns, show='headings')
        self.tree.grid(row=0, column=0, sticky='nsew')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=100, width=120, anchor='center')

        self.tree.bind('<<TreeviewSelect>>', self.on_treeview_select)

        # Scrollbar voor de Treeview
        tree_scrollbar = ttk.Scrollbar(overview_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        tree_scrollbar.grid(row=0, column=1, sticky='ns')

    def create_filter_frame(self, parent):
        """
        Creëert de filter sectie voor het overzicht.
        """
        filter_frame = ttk.LabelFrame(parent, text="Filter Bestellingen")
        filter_frame.grid(row=3, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

        # Configureer grid voor filter_frame
        filter_frame.columnconfigure(1, weight=1)
        filter_frame.columnconfigure(3, weight=1)

        ttk.Label(filter_frame, text="Selecteer Datum:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.filter_date_entry = DateEntry(filter_frame, date_pattern='dd/MM/yy')
        self.filter_date_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        filter_button = ttk.Button(filter_frame, text="Filter", command=self.filter_by_date)
        filter_button.grid(row=0, column=2, sticky='ew', padx=5, pady=2)

        show_all_button = ttk.Button(filter_frame, text="Toon Alles", command=self.show_all_orders)
        show_all_button.grid(row=0, column=3, sticky='ew', padx=5, pady=2)

    def set_current_date(self):
        """
        Stelt de datum in op de huidige datum.
        """
        current_date = datetime.now()
        self.date_entry.set_date(current_date)

    def submit_order(self, is_update=False):
        """
        Voegt een nieuwe bestelling toe of werkt een bestaande bij.
        """
        # Verzamel gegevens uit de invoervelden
        order_number = self.order_number_entry.get().strip()
        date_input = self.date_entry.get_date().strftime("%d/%m/%y")
        time = self.time_entry.get().strip().replace(".", ":")

        cheese_selection = self.cheese_var.get().strip()
        cheese_people = self.cheese_people_entry.get().strip()
        cheese_comment = self.cheese_comment_entry.get().strip()

        meat_selection = self.meat_var.get().strip()
        meat_people = self.meat_people_entry.get().strip()
        meat_comment = self.meat_comment_entry.get().strip()

        tapas_selection = self.tapas_var.get().strip()
        tapas_quantity = self.tapas_quantity_entry.get().strip()

        raclette_selection = self.raclette_var.get().strip()
        raclette_people = self.raclette_people_entry.get().strip()

        # Verzamel brood bestellingen
        bread_orders = {}
        for bread, entry in self.bread_entries.items():
            qty = entry.get().strip()
            if qty:
                bread_orders[bread] = qty

        general_comment = self.general_comment_entry.get().strip()

        # Maak een Order object
        order = Order(
            order_number, date_input, time,
            cheese_selection, cheese_people or None, cheese_comment,
            meat_selection, meat_people or None, meat_comment,
            tapas_selection, tapas_quantity or None,
            raclette_selection, raclette_people or None,
            bread_orders,
            general_comment
        )

        # Valideer de bestelling
        errors = order.validate()
        if errors:
            messagebox.showwarning("Validatie Fouten", "\n".join(errors))
            return

        if is_update:
            selected_item = self.tree.selection()
            if selected_item:
                selected_item = selected_item[0]
                # Hier halen we de index uit de Treeview, die correspondeert met de order in OrderManager
                index = self.tree.index(selected_item)
                self.order_manager.update_order(index, order)
                self.update_button.state(['disabled'])
                self.submit_button.state(['!disabled'])
                messagebox.showinfo("Update Succesvol", "Bestelling is succesvol bijgewerkt.")
        else:
            self.order_manager.add_order(order)
            messagebox.showinfo("Toegevoegd", "Bestelling is succesvol toegevoegd.")

        # Update het overzicht en clear de invoervelden
        self.update_order_treeview()
        self.clear_inputs()

    def clear_inputs(self):
        """
        Leegt alle invoervelden.
        """
        self.order_number_entry.delete(0, tk.END)
        self.date_entry.set_date(datetime.now())
        self.time_entry.delete(0, tk.END)

        self.cheese_var.set("")
        self.cheese_people_entry.delete(0, tk.END)
        self.cheese_comment_entry.delete(0, tk.END)

        self.meat_var.set("")
        self.meat_people_entry.delete(0, tk.END)
        self.meat_comment_entry.delete(0, tk.END)

        self.tapas_var.set("")
        self.tapas_quantity_entry.delete(0, tk.END)

        self.raclette_var.set("")
        self.raclette_people_entry.delete(0, tk.END)

        for entry in self.bread_entries.values():
            entry.delete(0, tk.END)

        self.general_comment_entry.delete(0, tk.END)

    def update_order_treeview(self):
        """
        Werkt de Treeview bij met de huidige bestellingen, gesorteerd op datum en tijd.
        """
        # Verwijder huidige inhoud
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Haal bestellingen op, gefilterd indien nodig
        if hasattr(self, 'filter_date') and self.filter_date.get():
            filtered_orders = self.order_manager.get_orders_by_dates([self.filter_date.get()])
        else:
            filtered_orders = self.order_manager.get_orders()

        # Sorteer bestellingen
        sorted_orders = sort_orders_by_date_time(filtered_orders)

        # Voeg bestellingen toe aan de Treeview
        for order in sorted_orders:
            self.tree.insert('', 'end', values=order.to_treeview_tuple())

    def on_treeview_select(self, event):
        """
        Laadt de geselecteerde bestelling in de invoervelden voor bewerking.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            return
        selected_item = selected_items[0]
        index = self.tree.index(selected_item)
        order = self.order_manager.get_orders()[index]

        # Vul de invoervelden met de gegevens van de bestelling
        self.order_number_entry.delete(0, tk.END)
        self.order_number_entry.insert(0, order.order_number)

        self.date_entry.set_date(datetime.strptime(order.date, "%d/%m/%y"))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, order.time)

        self.cheese_var.set(order.cheese_selection)
        self.cheese_people_entry.delete(0, tk.END)
        self.cheese_people_entry.insert(0, order.cheese_people or "")
        self.cheese_comment_entry.delete(0, tk.END)
        self.cheese_comment_entry.insert(0, order.cheese_comment)

        self.meat_var.set(order.meat_selection)
        self.meat_people_entry.delete(0, tk.END)
        self.meat_people_entry.insert(0, order.meat_people or "")
        self.meat_comment_entry.delete(0, tk.END)
        self.meat_comment_entry.insert(0, order.meat_comment)

        self.tapas_var.set(order.tapas_selection)
        self.tapas_quantity_entry.delete(0, tk.END)
        self.tapas_quantity_entry.insert(0, order.tapas_quantity or "")

        self.raclette_var.set(order.raclette_selection)
        self.raclette_people_entry.delete(0, tk.END)
        self.raclette_people_entry.insert(0, order.raclette_people or "")

        for bread, entry in self.bread_entries.items():
            entry.delete(0, tk.END)
            qty = order.bread_orders.get(bread, "")
            entry.insert(0, qty)

        self.general_comment_entry.delete(0, tk.END)
        self.general_comment_entry.insert(0, order.general_comment)

        # Schakel de knoppen in/uit
        self.update_button.state(['!disabled'])
        self.submit_button.state(['disabled'])

    def delete_order(self):
        """
        Verwijdert de geselecteerde bestelling.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Geen Selectie", "Selecteer een bestelling om te verwijderen.")
            return
        selected_item = selected_items[0]
        index = self.tree.index(selected_item)
        confirm = messagebox.askyesno("Bevestigen", "Weet je zeker dat je deze bestelling wilt verwijderen?")
        if confirm:
            self.order_manager.delete_order(index)
            self.update_order_treeview()
            self.clear_inputs()
            self.update_button.state(['disabled'])
            self.submit_button.state(['!disabled'])
            messagebox.showinfo("Verwijderd", "Bestelling is succesvol verwijderd.")

    def import_orders(self):
        """
        Importeert bestellingen vanuit een Excel-bestand.
        """
        from export import import_orders_from_excel

        filename = filedialog.askopenfilename(title="Selecteer Excel-bestand", filetypes=[("Excel bestanden", "*.xlsx")])
        if filename:
            import_orders_from_excel(filename, self.order_manager)
            self.update_order_treeview()
            messagebox.showinfo("Import Succesvol", "Bestellingen zijn succesvol geïmporteerd!")

    def export_orders(self):
        """
        Exporteert bestellingen naar een Excel-bestand.
        """
        from export import export_orders_to_excel

        date_filters = []
        if hasattr(self, 'filter_date') and self.filter_date.get():
            date_filters = [self.filter_date.get()]

        summary = self.order_manager.get_detailed_summary_by_dates(date_filters) if date_filters else self.order_manager.get_detailed_summary()

        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel bestanden", "*.xlsx")], title="Opslaan als")
        if filename:
            exported_file = export_orders_to_excel(self.order_manager.get_orders(), date_filters=date_filters, summary=summary, filename=filename)
            if exported_file:
                messagebox.showinfo("Export Succesvol", f"Bestellingen zijn succesvol geëxporteerd naar {exported_file}")

    def filter_by_date(self):
        """
        Filtert de bestellingen op basis van de geselecteerde datum.
        """
        selected_date = self.filter_date_entry.get_date().strftime("%d/%m/%y")
        self.filter_date = tk.StringVar(value=selected_date)
        self.update_order_treeview()

    def show_all_orders(self):
        """
        Toont alle bestellingen zonder filtering.
        """
        if hasattr(self, 'filter_date'):
            del self.filter_date
        self.update_order_treeview()

def create_main_interface(root, order_manager):
    """
    Creëert de hoofdinterface van de applicatie.
    """
    app = MainInterface(root, order_manager)
