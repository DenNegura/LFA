from common.TreeNode import *
from report import Report

n_counter = 0

N = 'n'

L = 'l'

REGISTERS = 2

CODE = "code"

CALL = "call"

POS = "pos"

PARAMS = "params"


def input_7():
    operators = {"-", "+", "/", "*"}

    root = TreeNode(val=input("root: "))

    def loop(node: TreeNode):
        left = TreeNode(val=input(f"  ?  \"{node.val}\"  X  : "), parent=node)
        right = TreeNode(val=input(f"  X  \"{node.val}\"  ?  : "), parent=node)
        node.left = left
        node.right = right

        if left.val in operators:
            loop(left)

        if right.val in operators:
            loop(right)

    loop(root)
    return root


def set_n(root: TreeNode):
    def call_n(node: TreeNode):
        global n_counter
        node.props[N] = n_counter
        n_counter += 1

    root.wide(call_n)
    return root


def set_l(root: TreeNode):
    def call_l(node: TreeNode):
        if not node.right and not node.right:
            if node.parent.right == node:
                node.props[L] = 0
            else:
                node.props[L] = 1
        else:
            left_l = node.left.props[L]
            right_l = node.right.props[L]
            if left_l == right_l:
                node.props[L] = left_l + 1
            elif left_l > right_l:
                node.props[L] = left_l
            else:
                node.props[L] = right_l

    root.postorder(call_l)
    return root


def get_assembler_op(op: str):
    if op == "+":
        return "add"
    if op == "-":
        return "sub"
    if op == "*":
        return "mul"
    if op == "/":
        return "div"


class Comm:
    def __init__(self, s: str, node: TreeNode = None):
        self.s = s
        self.node = node

    def is_gc(self) -> bool:
        return self.node is not None

    def set_eq(self, num_gc: str):
        self.s += f' =({num_gc})='

    def __str__(self):
        return self.s

    def __repr__(self):
        return f'"{self.s}"'


def gc1(node: TreeNode, i: int):
    return {
        CODE: (
            Comm(f'move R{i}, {node.val}'),
        )
    }


def gc2(node: TreeNode, i: int):
    return {
        CODE: (
            Comm(f'gc(n{node.left.props[N]}, {i})', node.left),
            Comm(f'{get_assembler_op(node.val)} R{i}, {node.right.val}, R{i}')
        ),
        CALL: (
            (node.left, i),
        )
    }


def gc31(node: TreeNode, i: int):
    return {
        CODE: (
            Comm(f'gc(n{node.right.props[N]}, {i})', node.right),
            Comm(f'gc(n{node.left.props[N]}, {i + 1})', node.left),
            Comm(f'{get_assembler_op(node.val)} R{i}, R{i + 1}, R{i}')
        ),
        CALL: (
            (node.right, i),
            (node.left, i + 1)
        )
    }


def gc32(node: TreeNode, i: int):
    return {
        CODE: (
            Comm(f'gc(n{node.left.props[N]}, {i})', node.left),
            Comm(f'gc(n{node.right.props[N]}, {i + 1})', node.right),
            Comm(f'{get_assembler_op(node.val)} R{i}, R{i + 1}, R{i}')
        ),
        CALL: (
            (node.left, i),
            (node.right, i + 1)
        )
    }


def gc33(node: TreeNode, i: int):
    return {
        CODE: (
            Comm(f'gc(n{node.right.props[N]}, {i})', node.right),
            Comm(f'mov Mem, R{i}'),
            Comm(f'gc(n{node.left.props[N]}, {i})', node.left),
            Comm(f'{get_assembler_op(node.val)} R{i}, Mem, R{i}')
        ),
        CALL: (
            (node.right, i),
            (node.left, i)
        )
    }


def gc(root: TreeNode):
    def get_gc_pos(_assembler: list[Comm], _node: TreeNode) -> int:
        for index, comm in enumerate(_assembler):
            if comm.is_gc():
                if comm.node.props[N] == _node.props[N]:
                    return index
        return -1

    def write(_report: Report, _assembler: list):
        for comm in _assembler:
            _report.write(comm.s).nl()
        _report.nl()

    def change(_assembler: list[Comm], pos: int, num_gc: str):
        _assembler[pos].set_eq(num_gc)

    def worker(_map: dict, _assembler: list, _q: queue.Queue, _replace_position: int):
        _assembler[_replace_position: _replace_position + 1] = _map[CODE]
        calls = _map.get(CALL)
        if calls:
            for call in calls:
                _q.put(call)

    report = Report()
    gq = queue.Queue()
    q = queue.Queue()
    q.put((root, 1))
    assembler = [Comm("gc(n0, 1)", root)]
    gq.put(q)

    while not gq.empty():
        last_assembler = assembler.copy()
        q = gq.get()
        nq = queue.Queue()
        while not q.empty():
            node, i = q.get()
            rp = get_gc_pos(assembler, node)
            ll, lr = None, None
            if node.left:
                ll = node.left.props[L]
            if node.right:
                lr = node.right.props[L]

            if ll is None and lr is None:
                change(assembler, rp, '1')
                worker(gc1(node, i), assembler, nq, rp)
            elif lr == 0:
                change(assembler, rp, '2')
                worker(gc2(node, i), assembler, nq, rp)
            elif 1 <= lr <= ll and lr < REGISTERS:
                change(assembler, rp, '3.2')
                worker(gc32(node, i), assembler, nq, rp)
            elif ll >= REGISTERS and lr >= REGISTERS:
                change(assembler, rp, '3.3')
                worker(gc33(node, i), assembler, nq, rp)
            elif 1 <= ll < lr and ll < REGISTERS:
                change(assembler, rp, '3.1')
                worker(gc31(node, i), assembler, nq, rp)
        if not nq.empty():
            gq.put(nq)
        write(report, last_assembler)
    write(report, assembler)


def infix_to_postfix(expression: str):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    expression = expression.replace(' ', '')
    postfix = []
    stack = []

    for symbol in expression:
        if symbol.isalnum():
            postfix.append(symbol)
        elif symbol == '(':
            stack.append(symbol)
        elif symbol == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()  # Remove '(' from the stack
        else:
            while stack and precedence.get(stack[-1], 0) >= precedence.get(symbol, 0):
                postfix.append(stack.pop())
            stack.append(symbol)

    while stack:
        postfix.append(stack.pop())

    return ''.join(postfix)


def postfix_to_tree(expression: str):
    root = TreeNode()

    def preorder(_root: TreeNode, exp: list) -> list:
        if not exp:
            return []
        _root.val = exp[0]

        if _root.val.isalnum():
            return exp[1:]

        _root.right = TreeNode(parent=_root)
        _root.left = TreeNode(parent=_root)

        exp = preorder(_root.right, exp[1:])
        return preorder(_root.left, exp)

    preorder(root, list(expression[::-1]))
    return root


def lab_7(expression: str, file_path: str = None):
    report = Report()
    report.write(" ======= LAB 7 =======").nl()
    report.write("expression = ").write(expression).nl().nl()
    expression = infix_to_postfix(expression)
    root = postfix_to_tree(expression)
    root = set_n(root)
    root = set_l(root)
    report.as_tree(root, lambda node: f'{node.val} n{node.props[N]} l={node.props[L]}')
    report.nl()
    gc(root)
    if file_path:
        Report().save_to_file(file_path)
    else:
        print(Report().read())


e = "a * (b + c) + a * (d - c)"

f = 'lab_7.txt'

lab_7(e, f)
