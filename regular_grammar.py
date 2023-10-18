from report import Report

E = ""

ASCII_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ALL_NTS = list(ASCII_UPPERCASE) + list(letter + "'" for letter in ASCII_UPPERCASE)


def get_next_nt(_nts: list[str] | set[str]) -> str:
    for _nt in ALL_NTS:
        if _nt not in _nts:
            return _nt
    raise Exception("All not terminals is in use!")


FORMULA = list[str]
FORMULAS = list[FORMULA]

RULE = tuple[str, FORMULA]
RULES = list[RULE]


def is_e(x: str):
    return x == E


def is_terminal(x: str) -> bool:
    return len(x) == 1 and not str.isupper(x)


def is_not_terminal(x: str) -> bool:
    return (len(x) == 1 and str.isupper(x)) or (len(x) == 2 and str.isupper(x[0]) and x[1] == "'")


def rule(non_terminal: str, formula: str | list = E) -> tuple:
    if isinstance(formula, str):
        formula = list(formula)
    return non_terminal, formula


def filter_by_nt(nt: str, rules: RULES) -> RULES:
    return [*filter(lambda rule: rule[0] == nt, rules)]


def filter_by_formula(formula: str, rules: RULES) -> RULES:
    return [*filter(lambda rule: formula in rule[1], rules)]


def get_rules_from_dict(dict_rules: dict) -> tuple[str, RULES]:
    _rules = []
    _axiom = list(dict_rules.keys())[0]
    for nt in dict_rules.keys():
        for formula in dict_rules[nt]:
            _rules.append(rule(nt, formula))
    return _axiom, _rules


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
    new_axiom = axiom
    if axiom in e_nts:
        is_in_formula = False
        for nt, formula in _rules:
            if axiom in formula:
                new_axiom = get_next_nt(e_nts)
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

    return _new_rules, new_axiom


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
                    if is_not_terminal(_f) and _f not in _next_reachable_nts:
                        _next_reachable_nts.add(_f)
                        _report.write(f'V{_report.concat_param("v_counter", 1)} = '
                                      f'{_report.as_set(_next_reachable_nts)}').nl()
            else:
                _next_rules.append(rule(_nt, _formula))
        if len(_next_reachable_nts) == len(_reachable_nts):
            return _reachable_nts
        else:
            return find_reachable_nts(_next_rules, _next_reachable_nts)

    _report.write(f'V{_report.concat_param("v_counter", 1)} = '
                  f'{_report.as_set({axiom})}').nl()
    reachable_nts = find_reachable_nts(rules, {axiom})
    _report.write(f'Nd = Vn / V{_report.get_param("v_counter") - 1} = '
                  f'{_report.as_set(reachable_nts)} / '
                  f'{_report.as_set({nt[0] for nt in rules}.difference(reachable_nts))}').nl()

    next_rules = []
    for nt, formula in rules:
        if nt in reachable_nts:
            next_rules.append(rule(nt, formula))
    return next_rules


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


def create_words(rules: RULES, axiom: str, length: int) -> set:
    def _replace_first(_nt: str, _word: list, _formula: list):
        _next_word = _word.copy()
        _i = _next_word.index(_nt)
        _next_word[_i: _i + 1] = _formula
        return _next_word

    def contains_non_terminals(_word: list) -> bool:
        for _letter in _word:
            if is_not_terminal(_letter):
                return True
        return False

    def is_necessary_len(_word: list) -> bool:
        return len(_word) >= length

    def is_max_len(_word: list) -> bool:
        return len(_word) >= length + length

    def contains(_nt: str, _word: list) -> bool:
        for _letter in _word:
            if _letter == _nt:
                return True
        return False

    def _create_word_recursive(_word: list, _rules: RULES, is_loop: bool) -> set | str:
        _words = set()
        for _letter in _word:
            if is_not_terminal(_letter):
                for _nt, _formula in filter_by_nt(_letter, _rules):
                    if is_loop is False and contains(_nt, _formula):
                        continue
                    _next_word = _replace_first(_nt, _word, _formula)

                    if is_necessary_len(_next_word):
                        is_loop = False
                        if not contains_non_terminals(_next_word):
                            return "".join(_next_word)
                    if is_max_len(_next_word):
                        return ""

                    _new_word = _create_word_recursive(_next_word, _rules, is_loop)
                    if _new_word:
                        if isinstance(_new_word, set):
                            _words = _words.union([*_new_word])
                        else:
                            _words = _words.union([_new_word])
        if _words:
            return _words
        return set()

    words = set()
    for nt, formula in filter_by_nt(axiom, rules):
        new_words = _create_word_recursive(formula, rules, True)
        if new_words:
            words = words.union([*new_words])
    return words


def get_the_best_word(words: set[str], is_max_len=True, is_max_letters=True) -> str:
    _words = list(words.copy())
    if is_max_len:
        _words = sorted(_words, key=lambda _word: len(_word), reverse=True)
    if is_max_letters:
        _words = sorted(_words, key=lambda _word: len(set(_word)), reverse=True)
    return _words[0]


def check_chomsky_normal_form(rules: RULES, word: str) -> bool:
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

    _report.create_table(8, '|', '-', list(word), [str(x) for x in range(1, len(word) + 1)], table)
    return axiom in table[-1][0]


report = Report().write("=== Начало Отчета ===").nl()

rules = [
    # rule('R', 'A'),
    # rule('A', 'iY'),
    # rule('Y', 'X'),
    # rule('Y'),
    # rule('X', 'OZ'),
    # rule('Z', 'X'),
    # rule('Z'),
    # rule('O', 't'),
    # rule('O', 'f'),

    rule('C', 'Ti'),
    rule('T', 'fLd'),
    rule('L', 'e'),
    rule('L', 'LcE'),
    rule('E', '1'),
    rule('E', '12'),
    #
    # rule('S'),
    # rule('S', 'aUbU'),
    # rule('U', 'S'),
    # rule('U', 'ba'),

    # rule('S', 'aAB'),
    # rule('S', 'BA'),
    # rule('A', 'BBB'),
    # rule('A', 'a'),
    # rule('B', 'AS'),
    # rule('B', 'b'),

    # rule('S', 'aA'),
    # rule('A', 'BBB'),
    # rule('A', 'AB'),
    # rule('B', 'b'),
    # rule('A', 'a'),
    # rule('S'),

    # rule('S', 'KMN'),
    # rule('K', 'ab'),
    # rule('N', 'Ab'),
    # rule('M', 'AB'),
    # rule('A'),
    # rule('B'),

    # rule('S', 'aSbS'),
    # rule('S', 'bSaS'),
    # rule('S'),

    # rule('S', 'KMN'),
    # rule('K', 'ab'),
    # rule('N', 'Ab'),
    # rule('M', 'AB'),
    # rule('A'),
    # rule('A', 'a'),
    # rule('B'),
    # rule('B', 'b'),

    # rule('A', 'B'),
    # rule('A', 'ab'),
    # rule('B', 'a'),
    # rule('B', 'C'),
    # rule('C', 'b'),

]
axiom = rules[0][0]

report.as_rules(rules, 0)

new_rules, new_axiom = to_chomsky_normal_form(axiom, rules)
# words = create_words(new_rules, new_axiom, 4)
# word = get_the_best_word(words)
word = 'fec1di'
print(word)
new_rules = [
    rule('C', 'TP'),
    rule('P', 'i'),
    rule('T', 'DZ'),
    rule('Z', 'LK'),
    rule('D', 'f'),
    rule('K', 'd'),
    rule('L', 'e'),
    rule('L', 'LB'),
    rule('B', 'QE'),
    rule('Q', 'c'),
    rule('E', '1'),
    rule('E', 'NY'),
    rule('N', '1'),
    rule('Y', '2'),
]
print(check_chomsky_normal_form(new_rules, word))
report.write("=== Конец Отчета ===")
print(Report().read())
