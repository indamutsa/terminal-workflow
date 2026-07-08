from src.calculator import Calculator


def test_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5


def test_subtract():
    calc = Calculator()
    assert calc.subtract(5, 2) == 3


def test_multiply():
    calc = Calculator()
    assert calc.multiply(4, 3) == 12


def test_divide():
    calc = Calculator()
    assert calc.divide(10, 2) == 5


def test_divide_by_zero_raises():
    calc = Calculator()
    try:
        calc.divide(1, 0)
        assert False, "expected an exception"
    except Exception:
        pass


def test_history_tracks_results():
    calc = Calculator()
    calc.add(1, 1)
    calc.add(2, 2)
    # Intentionally wrong expectation — Lesson 6 neotest "watch it fail" drill.
    assert calc.history == [2]
