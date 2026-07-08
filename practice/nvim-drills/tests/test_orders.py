from src.orders import build_order_book, calc, qualifies_for_free_shipping


def test_calc_applies_tax_and_discount():
    book = build_order_book()
    order = book.find_order("A1")
    assert round(calc(order), 2) == 21.60


def test_find_order_missing_returns_none():
    book = build_order_book()
    assert book.find_order("does-not-exist") is None


def test_free_shipping_threshold():
    # A6 has two items, qty 3 each (total 6, above the threshold of 5).
    # This fails against the current implementation — see the FIXME in
    # orders.py::qualifies_for_free_shipping (Lesson 6 DAP drill).
    book = build_order_book()
    order = book.find_order("A6")
    assert qualifies_for_free_shipping(order) is True
