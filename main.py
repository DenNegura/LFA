# import sys

# from JsonReader import JsonReader
# import regular_grammar as rg
# from report import Report
#
# read_file_path = sys.argv[1]
# write_file_path = sys.argv[2]
#
# json_data = JsonReader.read_file(read_file_path)
#
# axiom, rules = rg.get_rules_from_dict(json_data["rules"])
#
# Report().write("=== Начало отчёта ===").nl()\
#     .as_rules(rules, 0)
#
# rules_in_normal_form = rg.to_chomsky_normal_form(axiom, rules)
#
# Report().nl().write("=== Конец отчёта ===").nl()\
#     .save_to_file(write_file_path)


from regular_grammar import *
from report import *

# rules = [
#     rule('S', '{R'),
#     rule('S', '[R'),
#     rule('R', 'Ra}'),
#     rule('R', 'Ra]'),
#     rule('R', 'a'),
#     rule('R', 'T'),
#     rule('R', 'F'),
#     rule('R', 'E'),
#     rule('F', '{F}'),
#     rule('F', 'bb'),
#     rule('F', E),
#     rule('T', '[T]'),
#     rule('E', 'k#'),
# ]
# axiom = 'S'
# try:
#     greibach_normal_form(axiom, rules)
# except:
#     pass
# print(Report().read())

# rules = [
#     rule('R', 'A'),
#     rule('A', 'iY'),
#     rule('Y', 'X'),
#     rule('Y'),
#     rule('X', 'OZ'),
#     rule('Z', 'X'),
#     rule('Z'),
#     rule('O', 't'),
#     rule('O', 'f'),
# ]
# axiom = 'R'
#
# rules, axiom = to_chomsky_normal_form(axiom, rules)
#
# word = get_the_best_word(create_words(rules, axiom, 6))
#
# is_correct = check_chomsky_normal_form(axiom, rules, word)
# print(is_correct)

rules = [
    rule('S', 'Cf'),
    rule('C', 'abB'),
    rule('B', 'Dc'),
    rule('D', 'A'),
    rule('D', 'LgA'),
    rule('A', 'd'),
    rule('A', 'e'),
]
axiom = 'S'

word = 'abdgegdgdcf'
is_correct = False
try:
    # rules = remove_unreachable(rules, axiom)
    # Report().as_rules(rules, 0)
    # rules = remove_non_generating(rules)
    # Report().as_rules(rules, 0)
    mtx = create_word_analysis_matrix(axiom, rules)
    is_correct = check_by_word_analysis_matrix(mtx, axiom, rules, word)
except:
    print(Report().read())


if is_correct:
    print(Report().read())
