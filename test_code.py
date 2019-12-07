import re


def calculate(text):
    arithmetic_pattern = '\/calc\s?\d+\.?\d?\s*[-+*\/]\s*\d+\.?\d?\s*$'
    if not re.match(arithmetic_pattern, text):
        return('Неверное арифметичесикое выражение')
    else:
        text = re.sub('^/calc', '', text).strip()
        number_regexp = '\d+\.?\d?'
        operation_regexp = '[-+*\/]'
        numbers = list(map(float, re.findall(number_regexp, text)))
        operation = re.findall(operation_regexp, text)[0]
        if operation == '-':
            return numbers[0] - numbers[1]
        if operation == '+':
            return numbers[0] + numbers[1]
        if operation == '*':
            return numbers[0] * numbers[1]
        if operation == '/':
            try:
                return numbers[0] / numbers[1]
            except ZeroDivisionError:
                return 'На ноль нельзя делить!'

print(calculate('/calc 1-3+42'))
