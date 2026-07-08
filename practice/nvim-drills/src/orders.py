"""Order processing practice module — used by Lessons 6 and 7."""
import json
import sys

TAX_RATE = 0.08


class Order:
    def __init__(self, order_id, items, discount=0):
        self.order_id = order_id
        self.items = items
        self.discount = discount

    def subtotal(self):
        return sum(item["price"] * item["qty"] for item in self.items)


class OrderBook:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def find_order(self, order_id):
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def all_totals(self):
        return [calc(o) for o in self.orders]


# TODO: rename this — "calc" doesn't say what it computes (Lesson 6 rename drill)
def calc(o):
    subtotal = o.subtotal()
    taxed = subtotal * (1 + TAX_RATE)
    return taxed - o.discount


# FIXME: off-by-one — skips the last item in the free-shipping check (Lesson 6 DAP drill)
def qualifies_for_free_shipping(order):
    items = order.items
    total_qty = 0
    for i in range(len(items) - 1):
        total_qty += items[i]["qty"]
    return total_qty >= 5


RAW_ORDERS = [
    {"id": "A1", "items": [{"price": 10, "qty": 2}], "discount": 0},
    {"id": "A2", "items": [{"price": 5, "qty": 4}], "discount": 1},
    {"id": "A3", "items": [{"price": 20, "qty": 1}], "discount": 0},
    {"id": "A4", "items": [{"price": 8, "qty": 3}], "discount": 2},
    {"id": "A5", "items": [{"price": 15, "qty": 2}], "discount": 0},
    {"id": "A6", "items": [{"price": 3, "qty": 3}, {"price": 3, "qty": 3}], "discount": 0},
]


def build_order_book():
    book = OrderBook()
    for raw in RAW_ORDERS:
        book.add_order(Order(raw["id"], raw["items"], raw["discount"]))
    return book
