import asyncio


def fib(n) -> None:
    if n < 0:
        print("Niepoprawne dane wejściowe")

    elif n == 0:
        print("0")

    elif n == 1 or n == 2:
        print("1")

    else:
        print(fib(n - 1) + fib(n - 2))


if __name__ == "__main__":
    fib(5)