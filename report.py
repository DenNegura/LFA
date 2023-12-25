from TreeNode import TreeNode


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs) -> 'class_':
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Report:

    def __init__(self):
        self._report = ''
        self._params = {}

    def set_param(self, key, value):
        if self._params.get(key):
            old_value = self._params[key]
            self._params[key] = value
            return old_value
        else:
            self._params[key] = value
            return None

    def get_param(self, key):
        return self._params[key]

    def concat_param(self, key, value):
        old_value = self._params[key]
        self._params[key] += value
        return old_value

    def clean(self) -> 'Report':
        self._report = ''
        self._params = {}
        return self

    def write(self, line: str) -> 'Report':
        self._report += line
        return self

    @staticmethod
    def as_set(collection: set | list):
        if isinstance(collection, set):
            return str(collection).replace("'", '')
        if isinstance(collection, list):
            return '{' + ", ".join(collection) + '}'

    @staticmethod
    def as_rule(rule):
        return f'{rule[0]} -> {"".join(rule[1])}'

    def as_rules(self, rules, counter: int) -> 'Report':
        self.write(f'P{counter} = ').write("{").nl()
        for rule in rules:
            self.write('\t').write(self.as_rule(rule)).nl()
        self.write('}').nl()
        return self

    def nl(self) -> 'Report':
        self._report += '\n'
        return self

    def read(self) -> str:
        return self._report

    def create_table(self, space_cell: int, v_sep: str,  h_sep: str,
                     col_headers: list[str], row_headers: list[str],
                     table: list[list[set | list | str]], default_value='-') -> 'Report':
        def h_line():
            return h_sep * (space_cell + 1) * (len(col_headers) + 1) + '\n'

        self._report += f"\n{''.rjust(space_cell)}{v_sep}"
        for col in col_headers:
            self._report += f" {col.ljust(space_cell - 1)}{v_sep}"
        self._report += '\n' + h_line()

        row_index = 0
        for row in row_headers:
            self._report += f" {row.ljust(space_cell - 1)}{v_sep}"
            for cell in table[row_index]:
                str_cell = default_value
                if cell:
                    if type(cell) is set:
                        str_cell = str(cell).replace("{", "").replace("}", "").replace("'", "")
                    if type(cell) is list:
                        str_cell = str(cell).replace("[", "").replace("]", "").replace("'", "")
                    if type(cell) is str:
                        str_cell = cell
                self._report += f" {str_cell.ljust(space_cell - 1)}{v_sep}"
            self._report += '\n' + h_line()
            row_index += 1
        return self

    def save_to_file(self, file_path: str) -> 'Report':
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self._report)
        return self

    def as_tree(self, root: TreeNode, str_fun=str, level=0, prefix="Root: "):
        if root is not None:
            self.write(" " * (level * 4) + prefix + str_fun(root)).nl()
            if root.left is not None or root.right is not None:
                self.as_tree(root.left, str_fun, level + 1, "L--- ")
                self.as_tree(root.right, str_fun, level + 1, "R--- ")
