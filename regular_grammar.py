import string

E = ""

NON_TERMINALS = string.ascii_uppercase

def is_e(x: str):
    return x == E


def is_terminal(x: str):
    return not str.isupper(x)


class Rule:

    def __init__(self, nt: str, f: str | list = E):
        if isinstance(f, str):
            f = list(f)
        self._nt = nt
        self._f = f

    def __str__(self):
        return f'{self._nt} -> {"".join(self._f)}'

    def __repr__(self):
        self.__str__()

    def is_e(self) -> bool:
        return is_e(''.join(self._f))

    def get_nt(self):
        return self._nt

    def get_formula(self):
        return self._f

    def is_only(self, x: str | list):
        return sorted(x) == sorted(self._f)


def remove_e(rules: list[Rule], axiom: str) -> list[Rule]:
    first_e_nts = set()
    _rules = []
    # находим прямые 'е' правила
    for rule in rules:
        if not rule.get_formula():
            first_e_nts.add(rule.get_nt())
        else:
            _rules.append(rule)
    e_nts = first_e_nts.copy()

    # находим косвенные 'e' правила
    def find_e_rules(_rules: list):
        is_new_e_nt = False
        _rem_rules = []
        for _rule in _rules:
            if set(_rule.get_formula()) <= set(e_nts):
                e_nts.add(_rule.get_nt())
                is_new_e_nt = True
            else:
                _rem_rules.append(_rule)
        if is_new_e_nt:
            find_e_rules(_rem_rules)

    find_e_rules(_rules)

    # проверяем аксиому на 'e'
    if axiom in e_nts:
        new_axiom = (set(NON_TERMINALS) - e_nts).pop()


    return e_nts

r = [
    Rule('A', ''),
    Rule('B', 'cd'),
    Rule('C', 'FM'),
    Rule('D', 'FMCM'),
    Rule('F', 'M'),
    Rule('M')
]

for a in r:
    print(a)

print(remove_e(r, 'A'))


