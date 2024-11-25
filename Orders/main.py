# main.py

import tkinter as tk
from tkinter import messagebox
from orders import OrderManager
from interface import create_main_interface
from advanced_interface import create_advanced_interface

def setup_menubar(root, order_manager):
    """
    Stelt de menubalk in voor de hoofdapplicatie.
    """
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # 'Bestand' Menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Bestand", menu=file_menu)
    file_menu.add_command(label="Importeer Bestellingen", command=lambda: import_orders(order_manager))
    file_menu.add_command(label="Exporteer Bestellingen", command=lambda: export_to_excel(order_manager))
    file_menu.add_separator()
    file_menu.add_command(label="Afsluiten", command=root.quit)

    # 'Meer' Menu
    more_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Meer", menu=more_menu)
    more_menu.add_command(label="Geavanceerde Interface", command=lambda: create_advanced_interface(order_manager))

    # 'Help' Menu
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Over", command=lambda: show_about())

def import_orders(order_manager):
    """
    Importeert bestellingen vanuit een Excel-bestand.
    """
    from export import import_orders_from_excel
    from tkinter import filedialog

    filename = filedialog.askopenfilename(title="Selecteer Excel-bestand", filetypes=[("Excel bestanden", "*.xlsx")])
    if filename:
        import_orders_from_excel(filename, order_manager)
        messagebox.showinfo("Import Succesvol", "Bestellingen zijn succesvol geïmporteerd!")

def export_to_excel(order_manager):
    """
    Exporteert bestellingen en samenvattingen naar een Excel-bestand.
    """
    from export import export_orders_to_excel

    orders = order_manager.get_orders()
    summary = order_manager.get_detailed_summary()
    filename = export_orders_to_excel(orders, summary=summary)
    if filename:
        messagebox.showinfo("Export Succesvol", f"Bestellingen zijn succesvol geëxporteerd naar {filename}!")

def show_about():
    """
    Toont informatie over de applicatie.
    """
    messagebox.showinfo("Over", "Order Management System\nVersie 1.0\nOntwikkeld door [Uw Naam]")

def configure_root_window(root):
    """
    Configureert de hoofdwindow van de applicatie.
    """
    root.title("Order Management System - Kaaswinkel")
    root.geometry("1200x800")
    root.minsize(800, 600)  # Minimale afmetingen
    # root.iconbitmap('icon.ico')  # Voeg een aangepast icoon toe als 'icon.ico' bestaat

def main():
    """
    Hoofdfunctie die de applicatie start.
    """
    root = tk.Tk()

    # Configureer de hoofdwindow
    configure_root_window(root)

    # Initialiseer de OrderManager
    order_manager = OrderManager()

    # Stel de menubalk in
    setup_menubar(root, order_manager)

    # Creëer de hoofdinterface
    create_main_interface(root, order_manager)

    # Start de hoofdloop van de GUI
    root.mainloop()

if __name__ == "__main__":
    main()
