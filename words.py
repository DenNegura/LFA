from common import filter_by_nt, is_not_terminal, RULES


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
