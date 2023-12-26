import nltk

from common.TreeNode import TreeNode
from report import Report

N_NT = "N"

L_NT = "L"

B_NT = "B"

L = 'l'

S = 's'

V = 'v'

V_CALC = 'v_c'


def generate_tree(root: TreeNode, word: str):
    if word:
        node = TreeNode(val=L_NT, parent=root)
        if not root.right:
            root.right = node
        elif not root.left:
            root.left = node

        node.right = TreeNode(val=B_NT, parent=node)
        node.right.right = TreeNode(val=word[0], parent=node.right)
        generate_tree(node, word[1:])
        return root


def word_to_tree(word: str):
    root = TreeNode(N_NT)
    if word.find('.') != -1:
        words = word.split('.')
        for sub_word in words[::-1]:
            generate_tree(root, sub_word[::-1])
    else:
        generate_tree(root, word[::-1])
    return root


def calculate_l(root: TreeNode):
    def call_l(node: TreeNode):
        if node.val == L_NT:
            if node.left:
                node.props[L] = node.left.props[L] + 1
            else:
                node.props[L] = 1

    root.postorder(call_l)


def calculate_tree_s(tree: nltk.Tree):
    pass


def calculate_s(root: TreeNode):
    def call_s(node: TreeNode):
        if node.val == N_NT:
            if node.right and node.left:
                node.right.props[S] = -node.right.props[L]
                node.left.props[S] = 0
            elif node.right:
                node.right.props[S] = 0

        elif node.val == L_NT:
            node.right.props[S] = node.props[S]
            if node.left:
                node.left.props[S] = node.props[S] + 1

    root.preorder(call_s)


def calculate_v(root: TreeNode):
    def call_v(node: TreeNode):
        if node.val == B_NT:
            if node.right.val == '0':
                node.props[V] = '0'
                node.props[V_CALC] = 0
            if node.right.val == '1':
                node.props[V] = f'2^({node.props[S]})'
                node.props[V_CALC] = 2 ** int(node.props[S])
        elif node.val == L_NT or node.val == N_NT:
            if node.left:
                node.props[V] = node.left.props[V] + '+' + node.right.props[V]
                node.props[V_CALC] = node.left.props[V_CALC] + node.right.props[V_CALC]
            else:
                node.props[V] = node.right.props[V]
                node.props[V_CALC] = node.right.props[V_CALC]

    root.postorder(call_v)


def call_print(node: TreeNode):
    s = f'{node.val}'
    l_val = node.props.get(L)
    if l_val is not None:
        s += f'   l = {l_val}'
    s_val = node.props.get(S)
    if s_val is not None:
        s += f'   s = {s_val}'
    v_val = node.props.get(V)
    if v_val is not None:
        s += f'   v = {v_val}'
    return s


def to_bin(num: float):
    # Целая часть
    integer_part = int(num)
    binary_integer_part = bin(integer_part)[2:]

    # Десятичная часть
    decimal_part = num - integer_part
    binary_decimal_part = ''

    while decimal_part > 0:
        decimal_part *= 2
        bit = int(decimal_part)
        binary_decimal_part += str(bit)
        decimal_part -= bit

    return f"{binary_integer_part}.{binary_decimal_part}"


def check(num: float, word):
    return to_bin(num) == word


def lab_5(word: str, file_path: str = None):
    report = Report()
    root = word_to_tree(word)
    calculate_l(root)
    calculate_s(root)
    calculate_v(root)
    report.write(f"{root.val}: v = {root.props[V]} = {root.props[V_CALC]} = {to_bin(root.props[V_CALC])}") \
        .write(f'   {check(root.props[V_CALC], word)} ({word})').nl().nl()
    report.as_tree(root, call_print)
    print(Report().read())
    if file_path:
        Report().save_to_file(file_path)
    else:
        print(Report().read())


w = '11.0101'
f = 'lab_5.txt'

lab_5(w, f)
