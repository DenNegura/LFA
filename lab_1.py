from common.common import filter_by_formula, RULES, rule, is_terminal, get_next_nt, RULE
from common.grammar import remove_unreachable, remove_non_generating, remove_unit_pair, remove_e
from report import Report
from common.words import create_words, get_the_best_word


def to_chomsky_normal_form(axiom: str, rules: RULES) -> tuple[RULES, str]:
    _report = Report().write('Приведение к нормальной форме Хомского.').nl()
    rules, axiom = remove_e(rules, axiom)
    _report.as_rules(rules, 1)

    rules = remove_unit_pair(rules, axiom)
    _report.as_rules(rules, 2)

    rules = remove_non_generating(rules)
    _report.as_rules(rules, 3)

    rules = remove_unreachable(rules, axiom)
    _report.as_rules(rules, 4)

    nts_in_use = {r[0] for r in rules}

    def create_new_rules(_rule: RULE) -> RULES:

        def _get_new_nt() -> str:
            new_nt = get_next_nt(nts_in_use)
            nts_in_use.add(new_nt)
            return new_nt

        def _new_rules_for_terminals(_rule) -> RULES:
            _next_rules = []
            _nt, _formula = _rule
            if len(_formula) > 1:
                contains_terminals = False
                _new_formula = []
                for _t in _formula:
                    if is_terminal(_t):
                        contains_terminals = True
                        #
                        new_nt = _get_new_nt()
                        _next_rules.append(rule(new_nt, _t))
                        _new_formula.append(new_nt)
                    else:
                        _new_formula.append(_t)
                if contains_terminals:
                    _next_rules.append(rule(_nt, _new_formula))
                else:
                    _next_rules.append(rule(_nt, _formula))
            else:
                _next_rules.append(rule(_nt, _formula))
            return _next_rules

        def _new_rules_for_not_terminals(_rule) -> RULES:

            def _create_rules_recursive(_nt, _formula):
                _next_formula = []
                if len(_formula) > 2:
                    _new_nt = _get_new_nt()
                    _next_rules.append(rule(_new_nt, _formula[-2:]))
                    _next_formula = [*_formula[:-2], _new_nt]
                    _create_rules_recursive(_nt, _next_formula)
                    return
                _next_rules.append(rule(_nt, _formula))

            _nt, _formula = _rule
            _next_rules = []
            _create_rules_recursive(_nt, _formula)
            return _next_rules

        _terminal_rules = _new_rules_for_terminals(_rule)
        # print(_terminal_rules[-1])
        _not_terminal_rules = _new_rules_for_not_terminals(_terminal_rules[-1])
        _create_rules = [*_terminal_rules[:-1], *_not_terminal_rules][::-1]
        return _create_rules

    _new_rules = []
    for _rule in rules:
        _rules = create_new_rules(_rule)
        if _rules:
            for _r in _rules:
                _new_rules.append(_r)
    # _new_rules.sort(key=lambda _rule: _rule[0] != axiom)
    _report.write('(5) Приведение к типу A -> BC, B -> d.').nl()
    _report.as_rules(_new_rules, 5)
    return _new_rules, axiom


def check_chomsky_normal_form(axiom: str, rules: RULES, word: str) -> bool:
    _report = Report().write("Проверка на нормальную форму Хомского.").nl()
    _report.write(f"Слово: {word}").nl()

    table = [[]]
    for letter in word:
        nts = set()
        [nts.add(nt) for nt, formula in filter_by_formula(letter, rules)]
        table[0].append(nts.copy())

    def find_rules(f_nts: set[str], s_nts: set[str], _rules: RULES):
        f_nts = f_nts - {''}
        s_nts = s_nts - {''}
        if not f_nts or not s_nts:
            return ''
        for _nt, _formula in _rules:
            if len(_formula) > 1:
                for f_nt in f_nts:
                    for s_nt in s_nts:
                        if _formula[0] == f_nt and _formula[1] == s_nt:
                            return _nt
        return ''

    for row in range(1, len(word)):
        table.append([set() for _ in range(len(word))])
        for col in range(len(table[row]) - row):
            nts = set()
            for i in range(row):
                _f_nt = find_rules(table[i][col], table[row - i - 1][col + i + 1], rules)
                if _f_nt:
                    nts.add(_f_nt)
            if row:
                table[row][col] = nts

    _report.create_table(20, '|', '-', list(word), [str(x) for x in range(1, len(word) + 1)], table)
    return axiom in table[-1][0]


def lab_1(axiom: str, rules: RULES, word: str = None, len_word: int = 5, file_path: str = None):
    Report().write("=== Начало отчёта ===").nl() \
        .as_rules(rules, 0)
    rules, axiom = to_chomsky_normal_form(axiom, rules)
    if word is None:
        words = create_words(rules, axiom, len_word)
        word = get_the_best_word(words)
    is_good = check_chomsky_normal_form(axiom, rules, word)
    if is_good:
        Report().nl().write("Слово прошло проверку")
    else:
        Report().nl().write("Слово не прошло проверку")
    Report().nl().write("=== Конец отчёта ===").nl()
    if file_path:
        Report().save_to_file(file_path)
    else:
        print(Report().read())

r = [
    rule('C', 'Ti'),
    rule('T', 'fLd'),
    rule('L', 'e'),
    rule('L', 'LcE'),
    rule('E', '1'),
    rule('E', '12'),
]

a = 'C'
w = 'fec1di'
l = 6
f = 'lab_1.txt'
lab_1(a, r, w, l, f)
