def calculate_total(numbers):
    total = 0

    for number in numbers:
        if number % 2 == 0:
            total += number

    return total


numbers = [10, 15, 20, 25, 30]
result = calculate_total(numbers)

print(result)