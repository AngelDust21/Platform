# sort_orders.py

from datetime import datetime

def sort_orders_by_date_time(orders, reverse=False):
    """
    Sorteert een lijst van bestellingen op datum en tijd.

    :param orders: Lijst van Order objecten.
    :param reverse: Sorteer in omgekeerde volgorde als True.
    :return: Gesorteerde lijst van Order objecten.
    """
    def parse_datetime(order):
        try:
            return datetime.strptime(f"{order.date} {order.time}", "%d/%m/%y %H:%M")
        except ValueError:
            return datetime.max  # Plaats ongeldige datums achteraan

    return sorted(orders, key=parse_datetime, reverse=reverse)
