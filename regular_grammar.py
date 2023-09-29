import string

E = ""

NON_TERMINALS = string.ascii_uppercase

FORMULA = list[str]
FORMULAS = list[FORMULA]

RULE = tuple[str, FORMULA]
RULES = list[RULE]


def is_e(x: str):
    return x == E


def is_terminal(x: str) -> bool:
    return len(x) == 1 and not str.isupper(x)


def is_not_terminal(x: str) -> bool:
    return len(x) == 1 and str.isupper(x)


def rule(non_terminal: str, formula: str | list = E) -> tuple:
    if isinstance(formula, str):
        formula = list(formula)
    return non_terminal, formula


def view(_rule: tuple):
    return f'{_rule[0]} -> {"".join(_rule[1])}'


def remove_e(rules: RULES, axiom: str) -> tuple[RULES, FORMULAS]:
    e_nts = set()
    m_e_nts = []
    _rules = []

    ''' находим прямые 'е' правила '''
    for nt, formula in rules:
        if not formula:
            e_nts.add(nt)
        else:
            _rules.append(rule(nt, formula))
    m_e_nts.append(list(e_nts))

    ''' находим косвенные 'e' правила '''

    def find_e_rules(_rules: RULES):
        is_new_e_nt = False
        _rem_rules = []
        for _nt, _formula in _rules:
            if set(_formula) <= set(e_nts):
                e_nts.add(_nt)
                is_new_e_nt = True
            else:
                _rem_rules.append(rule(_nt, _formula))
        if is_new_e_nt:
            m_e_nts.append(list(e_nts))
            find_e_rules(_rem_rules)

    find_e_rules(_rules)

    _new_rules = []
    ''' проверяем аксиому на 'e' '''
    if axiom in e_nts:
        is_in_formula = False
        for nt, formula in _rules:
            if axiom in formula:
                new_axiom = (set(NON_TERMINALS) - e_nts).pop()
                _new_rules.append(rule(new_axiom))
                _new_rules.append(rule(new_axiom, axiom))
                is_in_formula = True
                break
        if not is_in_formula:
            _new_rules.append(rule(axiom))

    def combinations(_formula: FORMULA):
        _formula = _formula.copy()

        def get_combinations_list(_formula: FORMULA) -> list[list[int]]:
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
    for nt, formula in _rules:
        for _formula in combinations(formula):
            _new_rules.append(rule(nt, _formula))

    return _new_rules, m_e_nts


def remove_unit_pair(rules: RULES) -> tuple[RULES, str]:
    unit_rules = []
    nts = set()
    m_nts = {}
    report = ''
    _rules = []
    for nt, formula in rules:
        if is_not_terminal("".join(formula)):
            unit_rules.append((nt, formula[0]))
            nts = nts.union(nt, formula[0])
        else:
            _rules.append(rule(nt, formula))
    for nt in nts:
        m_nts[nt] = {nt}

    _copy_m_nts = dict()
    while _copy_m_nts != m_nts:
        _copy_m_nts = m_nts.copy()
        for nt, nt_f in unit_rules:
            last_nt_f = m_nts[nt_f]
            m_nts[nt_f] = m_nts[nt_f].union(m_nts[nt])
            report += f'{nt} -> {nt_f}, R({nt_f}) = R({nt_f}) U R({nt}) = ' \
                      f'{last_nt_f} U {m_nts[nt]} = {m_nts[nt_f]}\n'.replace("'", '')
    _k_to_remove = []
    for k_nt in m_nts:
        m_nts[k_nt] = m_nts[k_nt].difference(k_nt)
        if not m_nts[k_nt]:
            _k_to_remove.append(k_nt)
    for nt in _k_to_remove:
        m_nts.pop(nt)

    _new_rules = []
    for nt, formula in _rules:
        _new_rules.append(rule(nt, formula))
        if nt in m_nts:
            for unit_nt in m_nts[nt]:
                _new_rules.append(rule(unit_nt, formula))
    return _new_rules, report


def remove_non_generating(rules: RULES) -> RULES:
    def is_generate_nt(_formula: FORMULA, _allowed_list: list) -> bool:
        _formula = _formula.copy()
        last_terminals = set()
        for term in _formula:
            if not is_terminal(term) and term not in _allowed_list:
                last_terminals.add(term)
        return len(last_terminals) == 0

    def get_generate_nts(_rules, _allowed_list, _gen_list):
        _next_rules = []
        is_new_gen = False
        for _nt, _formula in _rules:
            if is_generate_nt(_formula, _allowed_list):
                _allowed_list.append(_nt)
                _gen_list.append(_nt)
                is_new_gen = True
            else:
                _next_rules.append(rule(_nt, _formula))
        if is_new_gen:
            return get_generate_nts(_next_rules, _allowed_list, _gen_list)
        return _gen_list

    gen_list = get_generate_nts(rules, [], [])

    print(gen_list)

# r = [
#     rule('A', 'M'),
#     rule('B', 'cd'),
#     rule('C', 'FM'),
#     rule('D', 'FMCM'),
#     rule('F', 'M'),
#     rule('M')
# ]
r = [
    rule('S', 'ABC'),
    rule('S'),
    rule('A', 'BB'),
    rule('A'),
    rule('B', 'CC'),
    rule('B'),
    rule('C', 'AA'),
    rule('C', 'b')
]

for a in r:
    print(view(a))

print("\n\nremove E prod: ")
n_r = remove_e(r, r[0][0])
print(n_r[1])
for a in n_r[0]:
    print(view(a))

print("\n\nremove unit pair: ")
r_2 = [
    rule('E', 'T'),
    rule('E', 'E+T'),
    rule('T', 'F'),
    rule('T', 'T*F'),
    rule('F', 'a'),
    rule('F', '(E)'),
]
n_n_r = remove_unit_pair(r_2)
print(n_n_r[1])

for t in n_n_r[0]:
    print(view(t))

print("\n\nremove non generating: ")
r_3 = [
    rule('S', 'Ac'),
    rule('A', 'SD'),
    rule('D', 'aD'),
    rule('A', 'a'),
]
n_n_n_r = remove_non_generating(r_3)
