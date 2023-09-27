import string

E = ""

NON_TERMINALS = string.ascii_uppercase


def is_e(x: str):
    return x == E


def is_terminal(x: str):
    return not str.isupper(x)


def rule(non_terminal: str, formula: str | list = E) -> tuple:
    if isinstance(formula, str):
        formula = list(formula)
    return non_terminal, formula


def view(_rule: tuple):
    return f'{_rule[0]} -> {"".join(_rule[1])}'


def remove_e(rules: list, axiom: str):
    e_nts = set()
    _rules = []

    ''' находим прямые 'е' правила '''
    for nt, formula in rules:
        if not formula:
            e_nts.add(nt)
        else:
            _rules.append(rule(nt, formula))

    ''' находим косвенные 'e' правила '''

    def find_e_rules(_rules: list):
        is_new_e_nt = False
        _rem_rules = []
        for _nt, _formula in _rules:
            if set(_formula) <= set(e_nts):
                e_nts.add(_nt)
                is_new_e_nt = True
            else:
                _rem_rules.append(rule(_nt, _formula))
        if is_new_e_nt:
            find_e_rules(_rem_rules)

    find_e_rules(_rules)

    ''' проверяем аксиому на 'e' '''
    if axiom in e_nts:
        new_axiom = (set(NON_TERMINALS) - e_nts).pop()
        # todo нужна логика, когда аксиома равна 'e'

    def combinations(_formula: list):
        _formula = _formula.copy()
        def get_combinations_list(_formula: list) -> list[list[int]]:
            indexes = []
            for _i, _s in enumerate(_formula):
                if _s in e_nts:
                    indexes.append(_i)

            list_e_index = [indexes.copy()]
            for _ in range(len(indexes) - 1):
                indexes.append(indexes.pop(0))
                list_e_index.append(indexes.copy())
            for i in range(len(list_e_index) - 1):
                list_e_index[i].pop()
            return list_e_index

        comb_list = get_combinations_list(_formula)
        _formulas = [_formula.copy()]

        for index_list in comb_list:
            _f = _formula.copy()
            for index in index_list:
                _f[index] = ' '
                _formulas.append(_f.copy())
        _new_formulas = []
        for _f in _formulas:
            for _ in range(_f.count(' ')):
                _f.remove(' ')
            if _f and _f not in _new_formulas:
                _new_formulas.append(_f)
        return _new_formulas

    # перебераем сочетания
    _new_rules = []
    for nt, formula in _rules:
        for _formula in combinations(formula):
            _new_rules.append(rule(nt, _formula))

    return _new_rules


# r = [
#     rule('A', 'M'),
#     rule('B', 'cd'),
#     rule('C', 'FM'),
#     rule('D', 'FMCM'),
#     rule('F', 'M'),
#     rule('M')
# ]
r = [
    rule('S', 'AABCd'),
    rule('A'),
    # rule('B', 'AC'),
    rule('C'),
    rule('B')
]

for a in r:
    print(view(a))

n_r = remove_e(r, 'A')
print("new list: ")
for a in n_r:
    print(view(a))
