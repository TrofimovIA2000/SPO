import re
from Лексический_анализатор import Lexer
from Связный_список import LinkedList


class StackMachine:
    pr = {'(': 0, ')': 1, '=': 1, '==': 3, '!=': 3, '>': 4, '>=': 4, '<': 4, '<=': 4, '+': 5, '-': 5, '*': 6, '/': 6,
          'contains': 7, 'remove': 7, 'push': 7, 'get': 7}
    log_op = ['==', '!=', '>', '>=', '<', '<=']
    op = ['+', '-', '*', '/']
    list_com = ['contains', 'remove', 'push', 'get']

    def __init__(self, inp):
        self.stack = []
        self.input = inp
        self.output = []
        self.buf = []
        self.bufel = []
        self.nl = 0
        self.index = -1
        self.variables = {}

    @staticmethod
    def bin_log_op(a, b, op):
        if op == '>':
            return a > b
        elif op == '<':
            return a < b
        elif op == '>=':
            return a >= b
        elif op == '<=':
            return a <= b
        elif op == '==':
            return a == b
        elif op == '!=':
            return a != b

    @staticmethod
    def bin_op(a, b, op):
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            return a / b

    @staticmethod
    def methodList(a, b, op):
        if op == 'push':
            a.push(b)
        elif op == 'remove':
            a.remove(b)
        elif op == 'get':
            a.get(b)
        elif op == 'contains':
            a.contains(b)

    def assign(self, a, b):
        if re.fullmatch(r"0|([1-9][0-9]*)", str(b)):
            self.variables[a] = int(b)
        elif b == 'LinkedList':
            self.variables[a] = LinkedList()
        else:
            self.variables[a] = b

    def abs(self, item):
        if item.name == 'while_expr':
            self.buf.append({self.nl: len(self.output)})

        if item.name not in Lexer.token and not item.name == 'METHOD':
            for i in item.children:
                self.abs(i)

            self.stack.reverse()
            for y in self.stack:
                if not y == '(':
                    self.output.append(y)

            self.stack = []

        else:
            if item.name == 'иначе':
                self.bufel.append(self.nl)
                self.output.append('\t')

            if item.name == 'конец':
                self.nl -= 1
                if '\n' in self.output:
                    self.output.reverse()
                    self.output[self.output.index('\n')] = len(self.output)
                    self.output.reverse()

                if len(self.buf):
                    if self.nl in list(self.buf[-1].keys()):
                        self.output.append('!' + str(self.buf[-1][self.nl]))
                        self.buf.pop(-1)

            if item.name == 'начало':
                self.nl += 1
                if self.nl > 0:
                    self.output.append('\n')

            if len(self.bufel) and not item.name == 'иначе':
                if self.nl == self.bufel[-1]:
                    self.output.reverse()
                    self.output[self.output.index('\t')] =\
                        '!' + str(len(self.output))
                    self.output.reverse()
                    self.bufel.pop(-1)

            if item.name in ['переменная', 'число', 'строка', 'связный_список']:
                self.output.append(str(item.value))

            else:
                if not item.value == '':
                    k = 0
                    for i in range(len(self.stack) - 1, -1, -1):
                        k += 1
                        if item.value == ')':
                            if not self.stack[i] == '(':
                                self.output.append(self.stack[i])
                            else:
                                break
                        elif self.pr[item.value] <= self.pr[self.stack[i]] \
                                and not item.value == '(':
                            self.output.append(self.stack[i])
                        else:
                            break

                    for j in range(1, k):
                        self.stack.pop(-j)

                    if not item.value == ')':
                        self.stack.append(item.value)

    def start(self):
        try:
            for item in self.input:
                self.abs(item)
                self.stack = []
            print(self.output)
            self.compilation()
            print(self.variables)
        except BaseException:
            raise BaseException

    def compilation(self):
        k = 0

        while k < len(self.output):
            if not self.output[k] in list(self.pr.keys()):
                if not (str(type(self.output[k])) == "<class 'int'>" or
                        list(self.output[k])[0] == '!'):
                    self.stack.append(self.output[k])
                    k += 1

                elif len(self.stack):
                    if not self.stack[-1] and\
                            not list(str(self.output[k]))[0] == '!':
                        if not self.stack[-1]:
                            if (self.output[k]) < len(self.output):
                                if isinstance(self.output[self.output[k]],
                                              int):
                                    k = self.output[k] + 1
                                    self.stack.pop(-1)
                                    continue
                                elif list(str(self.output[self.output[k]]))[0]\
                                        == '!':
                                    k = self.output[k] + 1
                                    self.stack.pop(-1)
                                    continue
                                else:
                                    k = self.output[k]
                                    self.stack.pop(-1)
                                    continue
                            else:
                                k = self.output[k] + 1
                                self.stack.pop(-1)
                                continue

                    elif list(str(self.output[k]))[0] == '!':
                        k = self.output[k]
                        continue

                    else:
                        self.stack.pop(-1)

                elif list(str(self.output[k]))[0] == '!':
                    k = int(str(self.output[k])[1:])
                    continue

                else:
                    k += 1

            else:
                b = self.stack.pop(-1)
                a = self.stack.pop(-1)
                op = self.output[k]
                k += 1
                if op == '=':
                    self.assign(a, b)

                elif op in self.log_op:
                    self.stack.append(self.bin_log_op(self.variables[a],
                                                      self.variables[b], op))

                elif op in self.op:
                    if not re.fullmatch(r"0|([1-9][0-9]*)", a):
                        a = self.variables[a]
                    else:
                        a = int(a)
                    if not re.fullmatch(r"0|([1-9][0-9]*)", b):
                        b = int(self.variables[b])
                    else:
                        b = int(b)
                    self.stack.append(self.bin_op(a, b, op))

                elif op in self.list_com:
                    self.stack.append(self.methodList(self.variables[a], b, op))
