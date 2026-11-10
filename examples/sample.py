"""Example file for the code review workbench."""


def calculate_total(prices: list[float]) -> float:
    """Return the sum of a list of prices."""
    total = 0.0
    for price in prices:
        if price >= 0:
            total += price
    return total


def run_example() -> None:
    print(calculate_total([10.0, 15.5, 2.0]))


if __name__ == "__main__":
    run_example()
