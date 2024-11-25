# orders.py

from collections import defaultdict
from datetime import datetime

class Order:
    """
    Klasse die een individuele bestelling vertegenwoordigt.
    """

    def __init__(self, order_number, date, time,
                 cheese_selection, cheese_people, cheese_comment,
                 meat_selection, meat_people, meat_comment,
                 tapas_selection, tapas_quantity,
                 raclette_selection, raclette_people,
                 bread_orders,
                 general_comment):
        self.order_number = order_number
        self.date = date
        self.time = time

        self.cheese_selection = cheese_selection
        self.cheese_people = cheese_people
        self.cheese_comment = cheese_comment

        self.meat_selection = meat_selection
        self.meat_people = meat_people
        self.meat_comment = meat_comment

        self.tapas_selection = tapas_selection
        self.tapas_quantity = tapas_quantity

        self.raclette_selection = raclette_selection
        self.raclette_people = raclette_people

        self.bread_orders = bread_orders  # Dictionary met broodsoorten en aantallen

        self.general_comment = general_comment

    def to_treeview_tuple(self):
        """
        Converteert de bestelling naar een tuple geschikt voor weergave in een Treeview.
        """
        bread_str = ', '.join([f"{bread} (x{qty})" for bread, qty in self.bread_orders.items() if qty])
        return (
            self.order_number,
            self.date,
            self.time,
            self.cheese_selection,
            self.cheese_people,
            self.cheese_comment,
            self.meat_selection,
            self.meat_people,
            self.meat_comment,
            self.tapas_selection,
            self.tapas_quantity,
            self.raclette_selection,
            self.raclette_people,
            bread_str,
            self.general_comment
        )

    def validate(self):
        """
        Valideert de bestelling en retourneert een lijst met fouten.
        """
        errors = []

        # Controleer verplichte velden
        if not self.order_number:
            errors.append("Bestelnummer is verplicht.")

        if not self.date:
            errors.append("Datum is verplicht.")

        if not self.time:
            errors.append("Tijd is verplicht.")

        # Controleer of aantal personen een positief geheel getal is
        def is_positive_integer(value, field_name):
            if value is not None:
                try:
                    if int(value) <= 0:
                        errors.append(f"{field_name} moet een positief geheel getal zijn.")
                except ValueError:
                    errors.append(f"{field_name} moet een geheel getal zijn.")

        is_positive_integer(self.cheese_people, "Aantal Personen Kaas")
        is_positive_integer(self.meat_people, "Aantal Personen Vlees")
        is_positive_integer(self.tapas_quantity, "Aantal Tapas")
        is_positive_integer(self.raclette_people, "Aantal Personen Raclette")

        # Controleer broodbestellingen
        for bread, qty in self.bread_orders.items():
            try:
                if int(qty) <= 0:
                    errors.append(f"Aantal voor {bread} moet een positief geheel getal zijn.")
            except ValueError:
                errors.append(f"Aantal voor {bread} moet een geheel getal zijn.")

        return errors

    def matches_query(self, query):
        """
        Controleert of de bestelling overeenkomt met de gegeven zoekopdracht.
        """
        query = query.lower()
        fields = [
            str(self.order_number),
            self.date,
            self.time,
            self.cheese_selection,
            str(self.cheese_people),
            self.cheese_comment,
            self.meat_selection,
            str(self.meat_people),
            self.meat_comment,
            self.tapas_selection,
            str(self.tapas_quantity),
            self.raclette_selection,
            str(self.raclette_people),
            ', '.join(self.bread_orders.keys()),
            ', '.join(self.bread_orders.values()),
            self.general_comment
        ]
        return any(query in str(field).lower() for field in fields)

    def get_total_items(self):
        """
        Retourneert het totale aantal items in de bestelling.
        """
        total = 0
        if self.cheese_people:
            total += int(self.cheese_people)
        if self.meat_people:
            total += int(self.meat_people)
        if self.tapas_quantity:
            total += int(self.tapas_quantity)
        if self.raclette_people:
            total += int(self.raclette_people)
        for qty in self.bread_orders.values():
            total += int(qty)
        return total

    def get_datetime(self):
        """
        Retourneert een datetime object op basis van de datum en tijd van de bestelling.
        """
        try:
            return datetime.strptime(f"{self.date} {self.time}", "%d/%m/%y %H:%M")
        except ValueError:
            return None

class OrderManager:
    """
    Beheert een lijst van bestellingen en biedt methoden voor interactie en manipulatie.
    """

    def __init__(self):
        self.orders = []

    def add_order(self, order):
        """
        Voegt een nieuwe bestelling toe.
        """
        self.orders.append(order)

    def update_order(self, index, order):
        """
        Werk een bestaande bestelling bij op basis van de index.
        """
        if 0 <= index < len(self.orders):
            self.orders[index] = order
        else:
            raise IndexError("Bestelling index buiten bereik.")

    def delete_order(self, index):
        """
        Verwijdert een bestelling op basis van de index.
        """
        if 0 <= index < len(self.orders):
            del self.orders[index]
        else:
            raise IndexError("Bestelling index buiten bereik.")

    def get_orders(self):
        """
        Retourneert de lijst met bestellingen.
        """
        return self.orders

    def get_orders_by_dates(self, dates):
        """
        Retourneert bestellingen die overeenkomen met de gegeven datums.
        """
        return [order for order in self.orders if order.date in dates]

    def get_detailed_summary_by_dates(self, dates):
        """
        Retourneert een samenvatting van bestellingen voor de gegeven datums.
        """
        summary = defaultdict(int)
        for order in self.get_orders_by_dates(dates):
            # Kaas
            if order.cheese_selection and order.cheese_people:
                key = f"{order.cheese_selection}"
                summary[key] += int(order.cheese_people)

            # Vlees
            if order.meat_selection and order.meat_people:
                key = f"{order.meat_selection}"
                summary[key] += int(order.meat_people)

            # Tapas
            if order.tapas_selection and order.tapas_quantity:
                key = f"{order.tapas_selection}"
                summary[key] += int(order.tapas_quantity)

            # Raclette
            if order.raclette_selection and order.raclette_people:
                key = f"{order.raclette_selection}"
                summary[key] += int(order.raclette_people)

            # Brood
            for bread, qty in order.bread_orders.items():
                if qty:
                    key = f"{bread}"
                    summary[key] += int(qty)
        return summary

    def get_detailed_summary(self):
        """
        Retourneert een samenvatting van alle bestellingen.
        """
        summary = defaultdict(int)
        for order in self.orders:
            # Zelfde als get_detailed_summary_by_dates maar dan voor alle bestellingen
            if order.cheese_selection and order.cheese_people:
                key = f"{order.cheese_selection}"
                summary[key] += int(order.cheese_people)

            if order.meat_selection and order.meat_people:
                key = f"{order.meat_selection}"
                summary[key] += int(order.meat_people)

            if order.tapas_selection and order.tapas_quantity:
                key = f"{order.tapas_selection}"
                summary[key] += int(order.tapas_quantity)

            if order.raclette_selection and order.raclette_people:
                key = f"{order.raclette_selection}"
                summary[key] += int(order.raclette_people)

            for bread, qty in order.bread_orders.items():
                if qty:
                    key = f"{bread}"
                    summary[key] += int(qty)
        return summary

    def search_orders(self, query):
        """
        Zoekt naar bestellingen die overeenkomen met de zoekopdracht.
        """
        return [order for order in self.orders if order.matches_query(query)]

    def sort_orders(self, reverse=False):
        """
        Sorteert de bestellingen op datum en tijd.
        """
        self.orders.sort(key=lambda order: order.get_datetime() or datetime.max, reverse=reverse)

    def get_order_by_number(self, order_number):
        """
        Zoekt een bestelling op basis van het bestelnummer.
        """
        for order in self.orders:
            if str(order.order_number) == str(order_number):
                return order
        return None

    def get_total_orders(self):
        """
        Retourneert het totale aantal bestellingen.
        """
        return len(self.orders)

    def get_total_items(self):
        """
        Retourneert het totale aantal items in alle bestellingen.
        """
        total = 0
        for order in self.orders:
            total += order.get_total_items()
        return total

    def get_orders_between_dates(self, start_date, end_date):
        """
        Retourneert bestellingen tussen twee datums (inclusief).
        """
        start = datetime.strptime(start_date, "%d/%m/%y")
        end = datetime.strptime(end_date, "%d/%m/%y")
        return [order for order in self.orders if start <= datetime.strptime(order.date, "%d/%m/%y") <= end]
