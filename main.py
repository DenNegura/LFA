import sys

import regular_grammar as rg
from JsonReader import JsonReader
from report import Report


def main():
    is_chomsky = sys.argv[1] == '-h'
    is_greibach = sys.argv[1] == '-g'
    read_file_path = sys.argv[2]
    write_file_path = sys.argv[3]

    json_data = JsonReader.read_file(read_file_path)

    axiom, rules = rg.get_rules_from_dict(json_data["rules"])

    Report().write("=== Начало отчёта ===").nl() \
        .as_rules(rules, 0)
    
    if is_chomsky:
        rules_in_normal_form, new_axiom = rg.to_chomsky_normal_form(axiom, rules)
        best_word = json_data.get("word")
        if best_word is None:
            words = rg.create_words(rules_in_normal_form, new_axiom, json_data["len-word"])
            best_word = rg.get_the_best_word(words)
        is_good = rg.check_chomsky_normal_form(new_axiom, rules_in_normal_form, best_word)
        if is_good:
            Report().nl().write("Слово прошло проверку")
        else:
            Report().nl().write("Слово не прошло проверку")

    if is_greibach:
        dict_table = rg.create_word_analysis_matrix(axiom, rules)
        best_word = json_data.get("word")
        if best_word is None:
            words = rg.create_words(rules, axiom, json_data["len-word"])
            best_word = rg.get_the_best_word(words)
        is_good = rg.check_by_word_analysis_matrix(dict_table, axiom, rules, best_word)
        if is_good:
            Report().nl().write("Слово прошло проверку")
        else:
            Report().nl().write("Слово не прошло проверку")

    Report().nl().write("=== Конец отчёта ===").nl() \
        .save_to_file(write_file_path)


if __name__ == "__main__":
    main()
