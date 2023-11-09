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


table = [[]]
table[0] = ['A', 'B', 'C', 'D', 'E']
print(table)

# table.append(['' for x in table[0][:-1]])
# table.append(['' for x in table[1][:-1]])
# table.append(['' for x in table[2][:-1]])
# table.append(['' for x in table[3][:-1]])
# table.append(['' for x in table[4][:-1]])
def find_rules(f_nts, s_nts):
    pass

# word = [1, 2, 3, 4, 5]
# for row in range(len(word) - 1):
#     table.append(['' for x in range(len(word))])
#     for col in range(len(table[row]) - row):
#         for i in range(row):
#             print(f'row = {row} | i = {i}, j = {col} i1 = {row - i - 1} j2 = {col + i + 1}')
#             find_rules(table[i][col], table[row - i - 1][col + i + 1])


# r = 1
# for c in range(len(table[r])):
#     for iter in range(r):
#         i, j = iter, c
#         i1, j1 = r - i - 1, j + iter + 1
#         print(f'iter = {iter} | i  = {i}, j  = {j}\niter = {iter} | i1 = {i1}, j1 = {j1}\n')


# print(table)

print(f"\n{''.rjust(10)}g")

f = ['A', 'B', 'C']
d = 'D'

for t, r in enumerate(f):
    print(t, r)