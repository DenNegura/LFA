import sys

from JsonReader import JsonReader
import regular_grammar as rg
from report import Report

read_file_path = sys.argv[1]
write_file_path = sys.argv[2]

json_data = JsonReader.read_file(read_file_path)

axiom, rules = rg.get_rules_from_dict(json_data["rules"])

Report().write("=== Начало отчёта ===").nl()\
    .as_rules(rules, 0)

rules_in_normal_form = rg.to_chomsky_normal_form(axiom, rules)

Report().nl().write("=== Конец отчёта ===").nl()\
    .save_to_file(write_file_path)