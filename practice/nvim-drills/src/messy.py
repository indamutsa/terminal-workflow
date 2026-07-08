"""Indentation is deliberately inconsistent here — reformat drill target
(Lessons 2, 3, 7: gg=G, :argdo, multi-file operations)."""


def summarize(items):
  total = 0
  for item in items:
      total += item["qty"]
      if item["qty"] > 10:
            total += 1
  return total


def flag_large_orders(orders):
    flagged = []
    for order in orders:
       if order.subtotal() > 100:
                flagged.append(order.order_id)
    return flagged


class Batch:
        def __init__(self, orders):
          self.orders = orders

        def total_items(self):
            return sum(summarize(o.items) for o in self.orders if hasattr(o, "items"))
