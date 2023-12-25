import nltk
from nltk import CFG


def lab_6():
    # Определение грамматики
    grammar = CFG.fromstring("""
        E -> T | E '+' T | E '-' T
        T -> F | T '*' F | T '/' F
        F -> '(' E ')' | 'a' | 'b' | 'c' | 'd'
    """)

    expression = input("Expression: ")
    # expression = 'a / b + (c - d) * b - c * d' # for test

    expression = expression.replace(' ', '')

    parser = nltk.ChartParser(grammar)

    # Разбор предложения и получение поддеревьев
    for tree in parser.parse(list(expression)):
        tree.draw()


lab_6()
