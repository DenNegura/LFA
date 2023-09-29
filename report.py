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
