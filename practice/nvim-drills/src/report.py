"""Reporting module — used by Lesson 7 (project-wide search & replace, quickfix)."""
from src.orders import TAX_RATE, build_order_book, calc


def print_report():
    book = build_order_book()
    print(f"Tax rate applied to every order: {TAX_RATE}")
    for order in book.orders:
        total = calc(order)
        print(f"Order {order.order_id}: total={total:.2f} (tax rate {TAX_RATE})")


if __name__ == "__main__":
    print_report()
