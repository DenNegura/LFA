
# class TreeNode:
#
#     def __init__(self, header, value=None):
#         self._nodes = []
#         self._value = value
#         self._header = header
#
#     def add(self, nodes):
#         if type(nodes) == list or type(nodes) == tuple:
#             self._nodes.extend(nodes)
#         else:
#             self._nodes.append(nodes)
#
#
# def create_tree_knuth(word: str):
#     axiom = "N_NT"
#     list_rules = [
#         rule(axiom, "L_NT"),
#         rule(axiom, "L_NT.L_NT"),
#         rule("L_NT", "LB"),
#         rule("L_NT", "B_NT"),
#         rule("B_NT", "1"),
#         rule("B_NT", "0"),
#     ]
#     tree_rules = rules_list_to_dict(list_rules)
#
#     class TreeNode:
#
#         def __init__(self, header, value=None):
#             self._nodes = []
#             self._value = value
#             self._header = header
#
#         def add(self, nodes):
#             if type(nodes) == list or type(nodes) == tuple:
#                 self._nodes.extend(nodes)
#             else:
#                 self._nodes.append(nodes)
#
#     def create_tree_by_world(_word: str) -> TreeNode:
#         _head = TreeNode("L_NT")
#         _nodes = []
#         for _letter in _word:
#             _nodes.append(TreeNode("B_NT", _letter))
#
#         def create_tree(__head: TreeNode, __nodes, __node) -> TreeNode:
#             if __nodes:
#                 __next_head = TreeNode("L_NT")
#                 __head.add((__next_head, __node))
#                 create_tree(__next_head, __nodes[:-1], __nodes[-1])
#             else:
#                 __head.add(__node)
#                 return __head
#
#         create_tree(_head, _nodes[:-1], _nodes[-1])
#         return _head
#
#     tree = TreeNode("N_NT")
#     inner_words = word.split('.')
#     if len(inner_words) == 2:
#         tree.add(create_tree_by_world(inner_words[0]))
#         tree.add(TreeNode(".", "."))
#         tree.add(create_tree_by_world(inner_words[1]))
#     elif len(inner_words) == 1:
#         tree.add(create_tree_by_world(inner_words[0]))
#     else:
#         raise Exception("points in word more two.")
#
#
# world_g = '101.11001'


# create_tree_knuth(world_g)

class TreeNode:

    def __init__(self, header: str, nodes: list['TreeNode'] = None):
        self.header = header
        if nodes is None:
            self.nodes = []
        else:
            self.nodes = nodes

    def add(self, node: 'TreeNode'):
        self.nodes.append(node)


def create_tree_by_word(axiom: str, rules: RULES, word: str):
    def create_by_recursion(rule, generate_word, header, node):

        if generate_word:
            if len(generate_word) == len(word) and generate_word == word:
                return header
            if is_terminal(generate_word[0]) and generate_word[0] != word[0]:
                return None
            if is_terminal(generate_word[-1]) and generate_word[-1] != word[-1]:
                return None



            for _rule in filter_by_nt(rule[0], rules):
                pass

            return None

    def create_tree(head: TreeNode, node: TreeNode, _word: str):

        def get_branch(_head: TreeNode, _part_word) -> TreeNode | None:
            _map = {}
            for i in range(0, len(_head.nodes)):
                _node = _head.nodes[i]
                if is_terminal(_node.header):
                    if _node.header == _word[0]:
                        _part_word = _part_word[1:]
                    return None
                else:
                    for _rule in filter_by_nt(_node.header, rules):
                        _new_node = TreeNode(_rule[0])
                        for _symbol in _rule[1]:
                            _new_node.add(TreeNode(_symbol))
                        _success_node = get_branch(_new_node, _part_word)
                        if _success_node:
                            _map[i] = _success_node







    axiom_rules = filter_by_nt(axiom, rules)
    for rule in axiom_rules:
        header = TreeNode(rule[0])
        for symbol in rule[1]:
            header.add(TreeNode(symbol))

        create_tree(header, header.nodes[0], word)
        # create_by_recursion(rule, '', TreeNode(rule[0], rule[1]), TreeNode(rule[0], rule[1]))


def generate_assembler_code(math_expression):

    class Operator(Enum):
        OPEN = ("(", 0)
        PLUS = ("+", 1)
        MINUS = ("-", 1)
        MULTIPLY = ("*", 2)
        DIVIDE = ("/", 2)

    def is_operator(s):
        for op in Operator:
            print(op)
            if s == op.value[0]:
                return True
        return False

    class Queue:

        class Node:
            def __init__(self, _val, _next=None, _prev=None):
                self.val = _val
                self.next = _next
                self.prev = _prev

        def __init__(self):
            self._index = 0
            self._root = None
            self._tail = None

        def push_first(self, val):
            if self._index != 0:
                self._root = self.Node(_val=val, _next=self._root)
            else:
                self._root = self.Node(_val=val)
                self._tail = self._root
            self._index += 1

        def push_last(self, val):
            if self._index != 0:
                self._tail = self.Node(_val=val, _prev=self._tail)
            else:
                self._tail = self.Node(_val=val)
                self._root = self._tail
            self._index += 1

        def pop_first(self):
            val = None
            if self._index == 1:
                val = self._root.val
                self._root = self._tail = None
            elif self._index > 1:
                val = self._root.val
                self._root = self._root.next
            else:
                raise Exception("Queue don't have elements.")
            self._index -= 1
            return val

        def pop_last(self):
            val = None
            if self._index == 1:
                val = self._tail.val
                self._root = self._tail = None
            elif self._index > 1:
                val = self._tail.val
                self._tail = self._tail.next
            else:
                raise Exception("Queue don't have elements.")
            self._index -= 1
            return val

        def peek_last(self):
            if self._index != 0:
                return self._tail.val
            else:
                raise Exception("Queue don't have elements.")

        def peek_first(self):
            if self._index != 0:
                return self._root.val
            else:
                raise Exception("Queue don't have elements.")

    q = Queue()
    q.push_first(1)
    q.push_first(2)
    q.push_last(0)
    print(q.pop_first())
    print(q.pop_first())
    print(q.pop_first())

    # def to_postfix_expression(exp: list) -> list:
    #
    #     stack = []
    #     for val in exp:
    #         if is_operator(val):
    #             pass
    #         else:
    #             stack.append()



    # prefix_exp = to_postfix_expression(list(math_expression))

# 2+(5*7)+4 => 57*2+4+
# generate_assembler_code("2+2")


# rules = [
#     rule('S', 'bA'),
#     rule('S', 'aB'),
#     rule('A', 'bAA'),
#     rule('A', 'aS'),
#     rule('A', 'a'),
#     rule('B_NT', 'aBB'),
#     rule('B_NT', 'ab'),
#     rule('B_NT', 'b'),
#
# ]
# create_tree_by_word('S', rules, 'bbaa')

# d = greibach_normal_form('S', rules)
# d = create_word_analysis_matrix('S', rules)
# check_by_word_analysis_matrix(d, 'S', rules, 'dbacbaa')
# r = greibach_normal_form('S', rules)
# r, s = to_chomsky_normal_form('S', rules)
# w = get_the_best_word(create_words(rules, 'S', 3))
# check_chomsky_normal_form(s, r, w)
#
# print(Report().read())
# for i in r:
#     print(Report().as_rule(i))
# m_rules = [
#     rule('R', 'S'),
#     rule('S', 'A'),
#     rule('S', 'aL'),
#     rule('L_NT', 'Sb'),
#     rule('L_NT', 'SL'),
#     rule('A', 'i'),
#     rule('A', 'n'),
# ]
# m_rules = [
#     rule('S', 'dA'),
#     rule('A', 'D'),
#     rule('A', 'DcA'),
#     rule('D', 'bB'),
#     rule('B_NT', 'a'),
#     rule('B_NT', 'aB'),
# ]
#
# Report().as_rules(m_rules, 0).nl()
# m_axiom = 'S'
# # m_word = 'aiiib'
# m_word = 'dbacbaa'
# m_dict_table = create_word_analysis_matrix(m_axiom, m_rules)
#
# check_by_word_analysis_matrix(m_dict_table, m_axiom, m_rules, m_word)
#
# print(Report().read())
# TODO НУЖНО НАПИСАТЬ ФАКТОРИЗАЦИЮ


# rules = [
#     rule('E', 'T'),
#     rule('E', ['T', 'E1']),
#     rule('E1', '+T'),
#     rule('E1', ['+', 'T', 'E1']),
#     rule('T', 'F'),
#     rule('T', ['F', 'T1']),
#     rule('T1', '*F'),
#     rule('T1', ['*', 'F', 'T1']),
#     rule('F', '(E)'),
#     rule('F', 'a'),
# ]
# axiom = 'E'
#
# greibach_normal_form(axiom, rules)


# report = Report().write("=== Начало Отчета ===").nl()

# rules = [
#     # rule('R', 'A'),
#     # rule('A', 'iY'),
#     # rule('Y', 'X'),
#     # rule('Y'),
#     # rule('X', 'OZ'),
#     # rule('Z', 'X'),
#     # rule('Z'),
#     # rule('O', 't'),
#     # rule('O', 'f'),
#
#     rule('C', 'Ti'),
#     rule('T', 'fLd'),
#     rule('L_NT', 'e'),
#     rule('L_NT', 'LcE'),
#     rule('E', '1'),
#     rule('E', '12'),
#     #
#     # rule('S'),
#     # rule('S', 'aUbU'),
#     # rule('U', 'S'),
#     # rule('U', 'ba'),
#
#     # rule('S', 'aAB'),
#     # rule('S', 'BA'),
#     # rule('A', 'BBB'),
#     # rule('A', 'a'),
#     # rule('B_NT', 'AS'),
#     # rule('B_NT', 'b'),
#
#     # rule('S', 'aA'),
#     # rule('A', 'BBB'),
#     # rule('A', 'AB'),
#     # rule('B_NT', 'b'),
#     # rule('A', 'a'),
#     # rule('S'),
#
#     # rule('S', 'KMN'),
#     # rule('K', 'ab'),
#     # rule('N_NT', 'Ab'),
#     # rule('M', 'AB'),
#     # rule('A'),
#     # rule('B_NT'),
#
#     # rule('S', 'aSbS'),
#     # rule('S', 'bSaS'),
#     # rule('S'),
#
#     # rule('S', 'KMN'),
#     # rule('K', 'ab'),
#     # rule('N_NT', 'Ab'),
#     # rule('M', 'AB'),
#     # rule('A'),
#     # rule('A', 'a'),
#     # rule('B_NT'),
#     # rule('B_NT', 'b'),
#
#     # rule('A', 'B_NT'),
#     # rule('A', 'ab'),
#     # rule('B_NT', 'a'),
#     # rule('B_NT', 'C'),
#     # rule('C', 'b'),
#
# ]
# axiom = rules[0][0]
#
# report.as_rules(rules, 0)
#
# new_rules, new_axiom = to_chomsky_normal_form(axiom, rules)
# # words = create_words(new_rules, new_axiom, 4)
# # word = get_the_best_word(words)
# word = 'fec1di'
# print(word)
# new_rules = [
#     rule('C', 'TP'),
#     rule('P', 'i'),
#     rule('T', 'DZ'),
#     rule('Z', 'LK'),
#     rule('D', 'f'),
#     rule('K', 'd'),
#     rule('L_NT', 'e'),
#     rule('L_NT', 'LB'),
#     rule('B_NT', 'QE'),
#     rule('Q', 'c'),
#     rule('E', '1'),
#     rule('E', 'NY'),
#     rule('N_NT', '1'),
#     rule('Y', '2'),
# ]
# print(check_chomsky_normal_form(new_rules, word))
# report.write("=== Конец Отчета ===")
# print(Report().read())


class Queue:
    class Node:
        def __init__(self, _val, _next=None, _prev=None):
            self.val = _val
            self.next = _next
            self.prev = _prev

    def __init__(self):
        self._index = 0
        self._root = None
        self._tail = None

    def push_first(self, val):
        if self._index != 0:
            node = self.Node(_val=val, _next=self._root)
            self._root.prev = node
            self._root = node
        else:
            self._root = self.Node(_val=val)
            self._tail = self._root
        self._index += 1

    def push_last(self, val):
        if self._index != 0:
            node = self.Node(_val=val, _next=self._root)
            self._tail = self.Node(_val=val, _prev=self._tail)
        else:
            self._tail = self.Node(_val=val)
            self._root = self._tail
        self._index += 1

    def pop_first(self):
        val = None
        if self._index == 1:
            val = self._root.val
            self._root = self._tail = None
        elif self._index > 1:
            val = self._root.val
            self._root = self._root.next
        else:
            raise Exception("Queue don't have elements.")
        self._index -= 1
        return val

    def pop_last(self):
        val = None
        if self._index == 1:
            val = self._tail.val
            self._root = self._tail = None
        elif self._index > 1:
            val = self._tail.val
            self._tail = self._tail.next
        else:
            raise Exception("Queue don't have elements.")
        self._index -= 1
        return val

    def peek_last(self):
        if self._index != 0:
            return self._tail.val
        else:
            raise Exception("Queue don't have elements.")

    def peek_first(self):
        if self._index != 0:
            return self._root.val
        else:
            raise Exception("Queue don't have elements.")
