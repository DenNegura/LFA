from common import is_terminal, rules_list_to_dict, RULES, is_not_terminal, get_next_nt, E, rules_dict_to_list, rule
from grammar import remove_left_recursion
from report import Report


def greibach_normal_form(axiom: str, rules: RULES):
    _rules = remove_left_recursion(axiom, rules)
    _dict_rules = rules_list_to_dict(_rules)

    def get_order_nts(_rules: RULES):
        _order_nts = []
        _all_nts = set()
        for _nt, _formula in _rules:
            _next_symbol = _formula[0]

            if is_not_terminal(_next_symbol):
                if _nt not in _all_nts:
                    _order_nts[:0] = _nt
                if _next_symbol not in _all_nts:
                    _order_nts.append(_next_symbol)
                    _all_nts.add(_next_symbol)

            _all_nts.add(_nt)
        return _order_nts

    order_nts = get_order_nts(_rules)
    for nt in order_nts[::-1][1:]:
        new_formulas = []
        for formula in _dict_rules[nt]:
            for deep_formula in _dict_rules[formula[0]]:
                new_formulas.append([*deep_formula, *formula[1:]])
        _dict_rules[nt] = new_formulas

    _dict_terminals = dict()
    for nt in _dict_rules.keys():
        new_formulas = []
        for formula in _dict_rules[nt]:
            if formula:
                new_formula = [formula[0]]
                for symbol in formula[1:]:
                    if is_terminal(symbol):
                        new_nt = _dict_terminals.get(symbol)
                        if new_nt is None:
                            new_nt = get_next_nt(order_nts)
                            _dict_terminals[symbol] = new_nt
                        new_formula.append(new_nt)
                    else:
                        new_formula.append(symbol)
                new_formulas.append(new_formula)
            else:
                new_formulas.append([E])
        _dict_rules[nt] = new_formulas
    for terminal in _dict_terminals.keys():
        _dict_rules[_dict_terminals[terminal]] = [[terminal]]

    return rules_dict_to_list(_dict_rules)


def lab_2(axiom: str, rules: RULES, file_path: str = None):
    Report().write("=== Начало отчёта ===").nl() \
        .as_rules(rules, 0)
    rules = greibach_normal_form(axiom, rules)
    Report().as_rules(rules, 0)
    Report().nl().write("=== Конец отчёта ===").nl()
    if file_path:
        Report().save_to_file(file_path)
    else:
        print(Report().read())

# for test
r = [
    rule('R', 'R~T'),
    rule('R', 'RT|'),
    rule('R', 'm'),
    rule('T', 'FT'),
    rule('T', 'Fi'),
    rule('T', 'Fj'),
    rule('T', 'Gk'),
    rule('T', 'K'),
    rule('G', 'KkG'),
    rule('G'),
    rule('K', 'Ki'),
    rule('K'),
]
a = 'R'
lab_2(a, r, 'result.txt')
