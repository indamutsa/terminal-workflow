from calculator import add, subtract, multiply, divide


def main():
    print("=== Calculator Demo ===")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
    print(f"5 * 6 = {multiply(5, 6)}")
    print(f"15 / 3 = {divide(15, 3)}")


if __name__ == "__main__":
    main()
