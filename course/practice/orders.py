TAX_RATE = 0.08
ORDERS = ["A1", "A2", "A3"]
PRICES = {"A1": 2.50, "A2": 4.00, "A3": 1.25}


def calc_totl(price, qty):
    return price * qty * (1 + TAX_RATE)


def report(codes):
    for code in codes:
        print(code, calc_totl(PRICES[code], 2))


name = "pen"
qty = 3
price = 2.50
note = "rush"
total = calc_totl(price, qty)
print(name, qty, price, note, total)
