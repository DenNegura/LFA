import string

from report import Report

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


def remove_e(rules: RULES, axiom: str) -> RULES:
    _report = Report().write('(1) Удаление е продукций.').nl()
    _report.set_param("n_counter", 1)
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

    for x in m_e_nts:
        _report.write(f'N{_report.concat_param("n_counter", 1)} = {_report.as_set(x)}').nl()

    return _new_rules


def remove_unit_pair(rules: RULES, axiom: str) -> RULES:
    _report = Report().write('(2) Удаление цепных правил.').nl()
    for nt in {x[0] for x in rules}:
        _report.write(f'R_{nt} = ' + '{' + nt + '} ')
    _report.nl()
    unit_rules = []
    nts = set()
    m_nts = {}
    _rules = []
    for nt, formula in rules:
        if is_not_terminal("".join(formula)):
            unit_rules.append((nt, formula[0]))
            nts = nts.union({nt}, formula[0])
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
            _report.write(f'{nt} -> {nt_f}, R_{nt_f} = R_{nt_f} U R_{nt} = ') \
                .write(f'{_report.as_set(last_nt_f)} U {_report.as_set(m_nts[nt])} = ') \
                .write(f'{_report.as_set(m_nts[nt_f])}').nl()
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
    return sorted(_new_rules, key=lambda _rule: _rule[0] == axiom, reverse=True)


def remove_non_generating(rules: RULES) -> RULES:
    _report = Report().write('(3) Удаление непорождающих нетерминалов.').nl()
    _report.set_param('v_counter', 0)

    def is_generate_nt(_formula: FORMULA, _allowed_list: set) -> bool:
        _formula = _formula.copy()
        last_terminals = set()
        for term in _formula:
            if not is_terminal(term) and term not in _allowed_list:
                last_terminals.add(term)
        return len(last_terminals) == 0

    def get_generate_nts(_rules: RULES, _allowed_set: set[str], _gen_set: set[str]) -> set[str]:
        _next_rules = []
        is_new_gen = False
        for _nt, _formula in _rules:
            if is_generate_nt(_formula, _allowed_set):
                if _nt not in _allowed_set:
                    _allowed_set.add(_nt)
                    _gen_set.add(_nt)
                    _report.write(f'V{_report.concat_param("v_counter", 1)} = {_report.as_set(_gen_set)}').nl()
                is_new_gen = True
            else:
                _next_rules.append(rule(_nt, _formula))
        if is_new_gen:
            return get_generate_nts(_next_rules, _allowed_set, _gen_set)
        return _gen_set

    def get_not_generate_nts(_rules: RULES, _gen_list: set[str]) -> list[str]:
        _not_gen_list = []
        for _nt, _formula in _rules:
            if _nt not in _gen_list:
                _not_gen_list.append(_nt)
        return _not_gen_list

    def remove_not_generate_nts(_rules: RULES, _not_gen_list: list[str]) -> RULES:
        _new_rules = []
        for _nt, _formula in _rules:
            if _nt in _not_gen_list:
                continue
            else:
                is_in_not_gen_list = False
                for _f_nt in _formula:
                    if _f_nt in _not_gen_list:
                        is_in_not_gen_list = True
                        break
                if is_in_not_gen_list:
                    continue
            _new_rules.append(rule(_nt, _formula))
        return _new_rules

    gen_set = get_generate_nts(rules, set(), set())
    not_gen_list = get_not_generate_nts(rules, gen_set)
    _report.write(f'Np = Vn / V{_report.get_param("v_counter")} = ') \
        .write(f'{_report.as_set({n[0] for n in rules})} / {_report.as_set(gen_set)} = ') \
        .write(f'{_report.as_set(not_gen_list)}').nl()
    return remove_not_generate_nts(rules, not_gen_list)


def remove_unreachable(rules: RULES, axiom: str) -> RULES:
    _report = Report().write('(4) Удаление недостижимых нетерминалов.').nl()
    _report.set_param("v_counter", 0)

    def find_reachable_nts(_rules: RULES, _reachable_nts: set) -> set[str]:
        _next_rules = []
        _next_reachable_nts = _reachable_nts.copy()
        for _nt, _formula in _rules:
            if _nt in _next_reachable_nts:
                for _f in _formula:
                    if is_not_terminal(_f):
                        _report.write(f'V{_report.concat_param("v_counter", 1)} = '
                                      f'{_report.as_set(_next_reachable_nts)}').nl()
                        _next_reachable_nts.add(_f)
            else:
                _next_rules.append(rule(_nt, _formula))
        if len(_next_reachable_nts) == len(_reachable_nts):
            return _reachable_nts
        else:
            return find_reachable_nts(_next_rules, _next_reachable_nts)

    reachable_nts = find_reachable_nts(rules, {axiom})
    _report.write(f'Nd = Vn \ V{_report.get_param("v_counter") - 1} = '
                  f'{_report.as_set(reachable_nts)} / '
                  f'{_report.as_set({nt[0] for nt in rules}.difference(reachable_nts))}').nl()

    next_rules = []
    for nt, formula in rules:
        if nt in reachable_nts:
            next_rules.append(rule(nt, formula))
    return next_rules


def to_chomsky_normal_form(rules: RULES, axiom: str) -> RULES:
    _report = Report().write('Приведение к нормальной форме Хомского.').nl()
    rules = remove_e(rules, axiom)
    report.as_rules(rules, 1)

    rules = remove_unit_pair(rules, axiom)
    report.as_rules(rules, 2)

    rules = remove_non_generating(rules)
    report.as_rules(rules, 3)

    rules = remove_unreachable(rules, axiom)
    report.as_rules(rules, 4)

    _report.write('(5) Приведение к типу A -> BC, B -> d.').nl()

    nts_in_use = {r[0] for r in rules}
    non_terminals = set(NON_TERMINALS)
    next_rules = []

    def create_rules_for_terminals(_rule: RULE):
        pass

    for nt, formula in rules:
        if len(formula) > 1:
            new_nt = None
            for _f in formula:
                if is_terminal(_f):
                    new_nt = (non_terminals - nts_in_use).pop()
                    nts_in_use.add(new_nt)
                    next_rules.append(rule(new_nt, _f))
            if new_nt is None:
                next_rules.append(rule(nt, formula))
        next_rules.append(rule(nt, formula))
    print(next_rules)


report = Report().write("=== Начало Отчета ===").nl()

rules = [
    rule('R', 'A'),
    rule('A', 'iY'),
    rule('Y', 'X'),
    rule('Y'),
    rule('X', 'OZ'),
    rule('Z', 'X'),
    rule('Z'),
    rule('O', 't'),
    rule('O', 'f'),
]
axiom = 'R'

report.as_rules(rules, 0)

to_chomsky_normal_form(rules, axiom)

report.write("=== Конец Отчета ===")
print(Report().read())
