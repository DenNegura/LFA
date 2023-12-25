FORMULA = list[str]
FORMULAS = list[FORMULA]

RULE = tuple[str, FORMULA]
RULES = list[RULE]

LIST_RULES = RULES
DICT_RULES = dict[str, FORMULAS]

E = ""

ASCII_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ALL_NTS = list(ASCII_UPPERCASE) + list(letter + "'" for letter in ASCII_UPPERCASE)


def is_terminal(x: str) -> bool:
    return len(x) == 1 and not str.isupper(x)


def is_not_terminal(x: str) -> bool:
    return (len(x) == 1 and str.isupper(x)) or (len(x) == 2 and str.isupper(x[0]) and x[1] == "'")


def rule(non_terminal: str, formula: str | list = E) -> tuple:
    if isinstance(formula, str):
        formula = list(formula)
    return non_terminal, formula


def filter_by_nt(nt: str, rules: RULES) -> RULES:
    return [*filter(lambda _rule: _rule[0] == nt, rules)]


def filter_by_formula(formula: str | list | tuple, rules: RULES) -> RULES:
    if type(formula) is str:
        return [*filter(lambda _rule: formula in _rule[1], rules)]
    return [*filter(lambda _rule: list(formula) == _rule[1], rules)]


def get_pairs(_formula: FORMULA) -> list[tuple[str, str]]:
    _pairs = []
    if len(_formula) > 1:
        for _i in range(1, len(_formula)):
            _pairs.append((_formula[_i - 1], _formula[_i]))
    return _pairs


def get_all_not_terminals(rules: RULES) -> list[str]:
    all_not_terminals = []
    for nt, formula in rules:
        if nt not in all_not_terminals:
            all_not_terminals.append(nt)
        for symbol in formula:
            if is_not_terminal(symbol) and symbol not in all_not_terminals:
                all_not_terminals.append(symbol)
    return all_not_terminals


def get_all_terminals(rules: RULES) -> list[str]:
    all_terminals = []
    for _, formula in rules:
        for symbol in formula:
            if is_terminal(symbol) and symbol not in all_terminals:
                all_terminals.append(symbol)
    return all_terminals


def rules_list_to_dict(list_rules: list) -> dict[str, FORMULAS]:
    dict_rules = {}
    for nt, formula in list_rules:
        if dict_rules.get(nt):
            dict_rules[nt].append(formula)
        else:
            dict_rules[nt] = [formula]
    return dict_rules


def get_next_nt(_nts: list[str] | set[str]) -> str:
    for _nt in ALL_NTS:
        if _nt not in _nts:
            return _nt
    raise Exception("All not terminals is in use!")


def rules_dict_to_list(dict_rules: dict) -> RULES:
    list_rules = []
    for nt in dict_rules.keys():
        for formula in dict_rules[nt]:
            list_rules.append(rule(nt, formula))
    return list_rules
