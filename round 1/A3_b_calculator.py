import math


def calculate(value: int):
    for x in range(math.ceil(value / 3), math.ceil(2 / 3 * value)):
        a = x * value
        b = 3 * x - value
        if a % b == 0:
            yield x, (a//b)


def calculate_count(value: int):
    count = 0
    for x in range(math.ceil(value / 3), math.ceil(2 / 3 * value)):
        a = x * value
        b = 3 * x - value
        if a % b == 0:
            count += 1
    return count



while True:
    n = int(input("n: "))
    pairs = list(calculate(n))
    print(len(pairs), pairs)

# m = 0
# count = int(input("count: "))
#
# for n in range(1, count+1):
#     if n % 3 == 0: continue
#     m = max(m, len(list(calculate(n))))
#     # print(n, len(list(calculate(n))))
#
# print(m)

# n = 1
#
# while True:
#     n += 1
#     if n % 3 == 0:
#         continue
#
#     if n % 1000 == 0:
#         print("not", n)
#
#     if calculate_count(n) == 2021:
#         print(n)


