# export.py

import pandas as pd
from tkinter import messagebox
from datetime import datetime

def export_orders_to_excel(orders, date_filters=None, summary=None, filename="bestellingen_export.xlsx"):
    """
    Exporteert bestellingen en samenvattingen naar een Excel-bestand.

    :param orders: Lijst van Order objecten.
    :param date_filters: Lijst van datums om te filteren (optioneel).
    :param summary: Samenvatting van bestellingen (optioneel).
    :param filename: Naam van het uitvoerbestand.
    :return: Naam van het geëxporteerde bestand.
    """
    data = []
    for order in orders:
        if date_filters and order.date not in date_filters:
            continue
        bread_orders = ', '.join([f"{bread} (x{qty})" for bread, qty in order.bread_orders.items() if qty])
        data.append({
            "Bestelnummer": order.order_number,
            "Datum": order.date,
            "Tijd": order.time,
            "Kaas Selectie": order.cheese_selection,
            "Aantal Personen Kaas": order.cheese_people,
            "Opmerkingen Kaas": order.cheese_comment,
            "Vlees Selectie": order.meat_selection,
            "Aantal Personen Vlees": order.meat_people,
            "Opmerkingen Vlees": order.meat_comment,
            "Tapas Selectie": order.tapas_selection,
            "Aantal Tapas": order.tapas_quantity,
            "Raclette Selectie": order.raclette_selection,
            "Aantal Personen Raclette": order.raclette_people,
            "Brood Bestelling": bread_orders,
            "Algemene Opmerkingen": order.general_comment
        })

    df_orders = pd.DataFrame(data)

    # Maak een DataFrame van de samenvatting
    if summary:
        summary_data = [{'Item': item, 'Totaal': total} for item, total in summary.items()]
        df_summary = pd.DataFrame(summary_data)
    else:
        df_summary = pd.DataFrame()

    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df_orders.to_excel(writer, sheet_name='Bestellingen', index=False)
            if not df_summary.empty:
                df_summary.to_excel(writer, sheet_name='Samenvatting', index=False)
        return filename
    except Exception as e:
        messagebox.showerror("Export Fout", f"Er is een fout opgetreden tijdens het exporteren: {e}")
        return None

def import_orders_from_excel(filename, order_manager):
    """
    Importeert bestellingen vanuit een Excel-bestand en voegt deze toe aan OrderManager.

    :param filename: Pad naar het Excel-bestand.
    :param order_manager: Instance van OrderManager.
    """
    try:
        df = pd.read_excel(filename, sheet_name='Bestellingen', engine='openpyxl')
        for index, row in df.iterrows():
            order_number = str(row['Bestelnummer'])
            date = str(row['Datum'])
            time = str(row['Tijd'])
            cheese_selection = str(row['Kaas Selectie']) if pd.notna(row['Kaas Selectie']) else ''
            cheese_people = str(row['Aantal Personen Kaas']) if pd.notna(row['Aantal Personen Kaas']) else None
            cheese_comment = str(row['Opmerkingen Kaas']) if pd.notna(row['Opmerkingen Kaas']) else ''
            meat_selection = str(row['Vlees Selectie']) if pd.notna(row['Vlees Selectie']) else ''
            meat_people = str(row['Aantal Personen Vlees']) if pd.notna(row['Aantal Personen Vlees']) else None
            meat_comment = str(row['Opmerkingen Vlees']) if pd.notna(row['Opmerkingen Vlees']) else ''
            tapas_selection = str(row['Tapas Selectie']) if pd.notna(row['Tapas Selectie']) else ''
            tapas_quantity = str(row['Aantal Tapas']) if pd.notna(row['Aantal Tapas']) else None
            raclette_selection = str(row['Raclette Selectie']) if pd.notna(row['Raclette Selectie']) else ''
            raclette_people = str(row['Aantal Personen Raclette']) if pd.notna(row['Aantal Personen Raclette']) else None
            bread_orders_str = str(row['Brood Bestelling']) if pd.notna(row['Brood Bestelling']) else ''
            general_comment = str(row['Algemene Opmerkingen']) if pd.notna(row['Algemene Opmerkingen']) else ''

            # Parse bread orders
            bread_orders = {}
            if bread_orders_str:
                bread_items = bread_orders_str.split(', ')
                for item in bread_items:
                    if '(x' in item:
                        bread_name, qty = item.split(' (x')
                        qty = qty.rstrip(')')
                        bread_orders[bread_name.strip()] = qty

            from orders import Order

            order = Order(
                order_number, date, time,
                cheese_selection, cheese_people if cheese_people != 'nan' else None,
                cheese_comment, meat_selection, meat_people if meat_people != 'nan' else None,
                meat_comment, tapas_selection, tapas_quantity if tapas_quantity != 'nan' else None,
                raclette_selection, raclette_people if raclette_people != 'nan' else None,
                bread_orders, general_comment
            )

            # Valideer de bestelling
            errors = order.validate()
            if errors:
                messagebox.showwarning("Validatie Fouten", f"Bestelling {order_number} bevat de volgende fouten:\n" + "\n".join(errors))
                continue

            # Voeg de bestelling toe aan OrderManager
            order_manager.add_order(order)

        messagebox.showinfo("Import Succesvol", "Bestellingen zijn succesvol geïmporteerd!")
    except FileNotFoundError:
        messagebox.showerror("Bestand Niet Gevonden", f"Het bestand {filename} is niet gevonden.")
    except ValueError as ve:
        messagebox.showerror("Import Fout", f"Er is een waarde fout opgetreden: {ve}")
    except Exception as e:
        messagebox.showerror("Import Fout", f"Er is een fout opgetreden tijdens het importeren: {e}")

def export_summary_to_excel(summary, filename="samenvatting_export.xlsx"):
    """
    Exporteert een samenvatting naar een Excel-bestand.

    :param summary: Dictionary met samenvatting.
    :param filename: Naam van het uitvoerbestand.
    :return: Naam van het geëxporteerde bestand.
    """
    try:
        summary_data = [{'Item': item, 'Totaal': total} for item, total in summary.items()]
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(filename, sheet_name='Samenvatting', index=False)
        return filename
    except Exception as e:
        messagebox.showerror("Export Fout", f"Er is een fout opgetreden tijdens het exporteren van de samenvatting: {e}")
        return None
