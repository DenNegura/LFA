from common import filter_by_formula, get_pairs, get_all_not_terminals, get_all_terminals, RULES, is_terminal, \
    is_not_terminal, DICT_RULES, rules_list_to_dict, rule
from report import Report
from words import create_words, get_the_best_word


def create_word_analysis_matrix(axiom: str, rules: RULES) -> dict[str, list[tuple[str, str]]]:
    _report = Report().nl().write("Грамматика простого прошествия.").nl()
    dict_rules = rules_list_to_dict(rules)

    def get_sequence(_nt: str, _rules: DICT_RULES, is_first=True) -> list[str]:
        _dict_rules = _rules.copy()
        _index = 0 if is_first else -1

        def get_seq(_nt: str):
            _symbols = []
            _next_symbols = []
            _formulas = _dict_rules.get(_nt)
            if _formulas:
                for _formula in _formulas:
                    last = _formula[_index]
                    if last in _symbols:
                        continue
                    _symbols.append(last)
                    if is_not_terminal(last):
                        if _dict_rules.get(_nt):
                            _dict_rules.pop(_nt)
                        for _last in get_seq(last):
                            if _last not in _symbols:
                                _next_symbols.append(_last)
            return [*_symbols, *_next_symbols]

        return get_seq(_nt)

    report_prims = []
    report_next = []
    dict_prims = dict()
    dict_next = dict()
    for nt in dict_rules.keys():
        _prims = get_sequence(nt, dict_rules, True)
        report_prims.append([_prims])
        dict_prims[nt] = _prims

        _next = get_sequence(nt, dict_rules, False)
        report_next.append([_next])
        dict_next[nt] = _next

    Report().create_table(30, '|', '-', ['Prim(N_NT)'], list(dict_rules.keys()), report_prims)
    Report().create_table(30, '|', '-', ['Next(N_NT)'], list(dict_rules.keys()), report_next)

    first_rules, second_rules, third_rules, fourth_rules = "", "", "", ""
    dict_table = {'=': [], '<': [], '>': []}
    for index, _rule in enumerate(rules):
        nt, formula = _rule
        pairs = get_pairs(formula)
        for a, b in pairs:
            # Aa || aA
            # if (is_not_terminal(a) and is_terminal(b)) or (is_terminal(a) and is_not_terminal(b)):
            first_rules += f"\n{index + 1}) {Report().as_rule(_rule)} -> {a} = {b}"
            dict_table['='] = [*dict_table['='], (a, b)]

            if is_not_terminal(b):  # Aa
                second_rules += f"\n{index + 1}) {Report().as_rule(_rule)} -> {a} < prim({b})  "
                for symbol in dict_prims[b]:
                    second_rules += f"{a} < {symbol}  "
                    dict_table['<'] = [*dict_table['<'], (a, symbol)]

            if is_not_terminal(a) and is_terminal(b):  # aA
                third_rules += f"\n{index + 1}) {Report().as_rule(_rule)} -> next({a}) > {b}  "
                for symbol in dict_next[a]:
                    third_rules += f"{symbol} > {b}  "
                    dict_table['>'] = [*dict_table['>'], (symbol, b)]

            if is_not_terminal(a) and is_not_terminal(b):  # AA
                fourth_rules += f"\n{index + 1}) {Report().as_rule(_rule)} -> next({a}) > prim({b}) / Vn"
                for last_symbol in dict_next[a]:
                    fourth_rules += f"\n\t{last_symbol}"
                    for prim_symbol in dict_prims[b]:
                        if is_terminal(prim_symbol):
                            fourth_rules += f" > {prim_symbol}"
                            dict_table['>'] = [*dict_table['>'], (last_symbol, prim_symbol)]

    fifth_rules = f"$ < Prim({axiom}) ({axiom} - Аксиома), $ - начало строки."
    fifth_rules += f"\n\t$ < Prim({axiom})"
    for symbol in dict_prims[axiom]:
        fifth_rules += f"\n\t$ < {symbol}"
        dict_table['<'] = [*dict_table['<'], ('$', symbol)]
    sixth_rules = f"Next({axiom}) > $ ({axiom} - Аксиома), $ - конец строки."
    sixth_rules += f"\n\n\tNext({axiom}) > $"
    for symbol in dict_next[axiom]:
        sixth_rules += f"\n\t{symbol} > $"
        dict_table['>'] = [*dict_table['>'], (symbol, '$')]

    _report.nl().write("Пункт 1.").nl().write(first_rules).nl()
    _report.nl().write("Пункт 2.").nl().write(second_rules).nl()
    _report.nl().write("Пункт 3.").nl().write(third_rules).nl()
    _report.nl().write("Пункт 4.").nl().write(fourth_rules).nl()
    _report.nl().write("Пункт 5.").nl().write(fifth_rules).nl()
    _report.nl().write("Пункт 6.").nl().write(sixth_rules).nl()

    headers = [*get_all_not_terminals(rules), *get_all_terminals(rules), '$']
    grid = []
    for i in range(len(headers)):
        grid.append([])
        for _ in headers:
            grid[i].append([])

    for operator in dict_table.keys():
        for pair in dict_table[operator]:
            grid[headers.index(pair[0])][headers.index(pair[1])] = operator

    _report.create_table(8, '|', '-', headers, headers, grid, '')
    return dict_table


# todo view a error
def check_by_word_analysis_matrix(dict_table: dict[str, list[tuple[str, str]]], axiom: str, rules: RULES,
                                  word: str) -> bool:
    _report = Report().nl().write(f"Анализ слова: {word}").nl()
    if word[0] != '$':
        word = '$' + word
    if word[-1] != '$':
        word = word + '$'
    stack_trice = "$"
    end_conditional = f"${axiom}$"
    is_generated_world = True
    counter = 0
    while word != end_conditional and counter < 100:
        counter += 1
        next_word = ""
        is_first = True
        jump_next = False
        for pair_word in get_pairs(list(word)):
            if jump_next:
                jump_next = False
                continue
            is_find_pair = False
            for operator in dict_table:
                for pair in dict_table[operator]:
                    if pair_word[0] == pair[0] and pair_word[1] == pair[1]:
                        is_find_pair = True
                        stack_trice += f" {operator} {pair[1]}"
                        if operator == '=' and is_first:

                            jump_next = True
                            _rules = filter_by_formula(pair, rules)
                            if _rules:
                                is_first = False
                                next_word += _rules[0][0]
                        elif operator == '>' and is_first:
                            is_first = False
                            nt = filter_by_formula(pair[0], rules)[0][0]
                            next_word += nt
                        else:
                            next_word += pair[0]
            if is_find_pair is False:
                _report.nl().write("Слово не прошло проверку.").nl()
                is_generated_world = False

        next_word += '$'
        word = next_word
        stack_trice += "\n$"
    stack_trice += f' < {axiom} > $'

    _report.nl().write(stack_trice).nl()
    return is_generated_world


def lab_3(axiom: str, rules: RULES, word: str, len_word: int = 5, file_path: str = None):
    Report().write("=== Начало отчёта ===").nl() \
        .as_rules(rules, 0)
    data = create_word_analysis_matrix(axiom, rules)
    if word is None:
        words = create_words(rules, axiom, len_word)
        word = get_the_best_word(words)
    is_good = check_by_word_analysis_matrix(data, axiom, rules, word)
    if is_good:
        Report().nl().write("Слово прошло проверку")
    else:
        Report().nl().write("Слово не прошло проверку")
    Report().nl().write("=== Конец отчёта ===").nl()
    if file_path:
        Report().save_to_file(file_path)
    else:
        print(Report().read())

# for test
# r = [
#     rule('R', 'S'),
#     rule('S', 'A'),
#     rule('S', 'aL'),
#     rule('L', 'Sb'),
#     rule('L', 'SL'),
#     rule('A', 'i'),
#     rule('A', 'n'),
# ]
# a = 'R'
# w = 'aiiib'

# r = [
#     rule('S', 'A'),
#     rule('A', 'C'),
#     rule('A', 'AcC'),
#     rule('C', 'a'),
#     rule('C', 'b'),
#     rule('C', 'dD'),
#     rule('D', 'Ae'),
# ]
# a = 'S'
# w = 'ccdce'

# r = [
#     rule('S', 'Cf'),
#     rule('C', 'abB'),
#     rule('B', 'Dc'),
#     rule('D', 'A'),
#     rule('D', 'gA'),
#     rule('A', 'd'),
#     rule('A', 'e'),
# ]
# a = 'S'
#
# lab_3(a, r, None, 4, 'result.txt')
