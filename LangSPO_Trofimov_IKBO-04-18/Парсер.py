class Parser:
    def __init__(self, lexer):
        self.height = 0
        self.i = 0
        self.start = lexer
        self.LB = 0

    def S(self):
        S = Node('S')
        while self.i < len(self.start) - 1:
            self.height = 1
            exp = self.exp()
            if exp is not None:
                S.children.append(exp)
            self.i += 1

        return S

    def exp(self):
        try:
            expr = Node('expr', height=self.height)
            self.height += 1

            token = list(self.start[self.i].keys())[0]

            if token == "переменная":
                try:
                    assign_expr = self.assign_expr()
                    expr.children.append(assign_expr)
                    self.height -= 1
                    return expr

                except BaseException:
                    expr.children.append(Leaf(list(self.start[self.i].keys())[0], list(self.start[self.i].values())[0],
                                              self.height))
                    self.check_next('точка')
                    self.i += 1
                    method = self.method()
                    expr.children.append(method)
                    return expr

            elif token == 'пока':
                while_expr = self.while_expr()
                expr.children.append(while_expr)
                self.height -= 1
                return expr

            elif token == 'если':
                if_expr = self.if_expr()
                expr.children.append(if_expr)
                self.height -= 1
                return expr

            else:
                return None
        except BaseException:
            raise BaseException

    def method(self):
        method = Node('method', height=self.height)
        self.height += 1
        self.check_next('METHOD')
        self.i += 1
        method.children.append(Leaf(name=list(self.start[self.i].keys())[0], value=list(self.start[self.i].values())[0],
                               height=self.height))
        self.height += 1
        self.check_next('открыть_скобки')
        self.i += 1
        method.children.append(Leaf(name=list(self.start[self.i].keys())[0], value=list(self.start[self.i].values())[0],
                                    height=self.height))
        math_expr = self.math_expr()
        method.children.append(math_expr)

        if not list(self.start[self.i].keys())[0] == 'окончание_команды':
            raise BaseException

        return method

    def if_expr(self):
        height = self.height
        if_expr = Node('if_expr', height=self.height)
        self.height += 1
        start_height = self.height
        self.check_next('открыть_скобки')
        if_expr.children.append(Leaf('открыть_скобки', '(', height=self.height))
        self.i += 2
        self.height += 1
        token = list(self.start[self.i].keys())[0]

        if token == 'переменная' or token == 'число' or token == 'открыть_скобки':
            math_logic = self.math_logic(ht=[start_height])
            if_expr.children.append(math_logic)

            self.height = start_height
            self.check_next('начало')
            if_expr.children.append(Node('начало', height=start_height))
            self.i += 1
            num_L = 1
            while num_L:
                if list(self.start[self.i].keys())[0] == 'конец':
                    num_L -= 1
                if list(self.start[self.i].keys())[0] == 'начало':
                    num_L += 1
                if num_L:
                    self.i += 1
                    self.height = start_height
                    self.height += 1
                    if list(self.start[self.i].keys())[0] == 'начало':
                        num_L += 1
                    if list(self.start[self.i].keys())[0] == 'конец':
                        num_L -= 1
                        break
                    expr = self.exp()
                    if expr is not None:
                        if_expr.children.append(expr)

            if_expr.children.append(Node('конец', height=start_height))

            if self.i < len(self.start) - 1:
                self.check_next('иначе')
                self.i += 1
                self.check_next('начало')
                self.height = height
                if_expr.children.append(Node('иначе', height=self.height))
                self.height += 1
                start_height = self.height
                if_expr.children.append(Node('начало', height=self.height))
                num_L = 1

                while num_L:

                    if list(self.start[self.i].keys())[0] == 'конец':
                        num_L -= 1
                    if list(self.start[self.i].keys())[0] == 'начало':
                        num_L += 1
                    if num_L:
                        self.i += 1
                        self.height = start_height
                        self.height += 1
                        if list(self.start[self.i].keys())[0] == 'начало':
                            num_L += 1
                        if list(self.start[self.i].keys())[0] == 'конец':
                            num_L -= 1
                            break
                        expr = self.exp()
                        if expr is not None:
                            if_expr.children.append(expr)

                if_expr.children.append(Node('конец', height=start_height))
            return if_expr

    def while_expr(self):
        while_expr = Node('while_expr', height=self.height)
        self.height += 1
        start_height = self.height
        self.check_next('открыть_скобки')
        while_expr.children.append(Leaf('открыть_скобки', '(', height=self.height))
        self.i += 2
        self.height += 1
        token = list(self.start[self.i].keys())[0]
        if token == 'переменная' or token == 'число' or token == 'открыть_скобки':
            math_logic = self.math_logic(ht=[start_height])
            while_expr.children.append(math_logic)

            self.height = start_height
            self.check_next('начало')
            self.i += 1
            while_expr.children.append(Node('начало', height=self.height))
            num_L = 1

            while num_L:
                if list(self.start[self.i].keys())[0] == 'конец':
                    num_L -= 1
                if list(self.start[self.i].keys())[0] == 'начало':
                    num_L += 1

                if num_L:
                    self.i += 1
                    self.height = start_height
                    self.height += 1
                    if list(self.start[self.i].keys())[0] == 'начало':
                        num_L += 1
                    if list(self.start[self.i].keys())[0] == 'конец':
                        num_L -= 1
                        break
                    expr = self.exp()
                    if expr is not None:
                        while_expr.children.append(expr)

            while_expr.children.append(Node('конец', height=start_height))
            return while_expr
        else:
            raise BaseException

    def math_logic(self, ht=[]):
        token = list(self.start[self.i].keys())[0]

        if not token == 'закрыть_скобки' or not token == 'логическая_операция' \
                or not token == 'операция':
            math_logic = Node('math_logic', height=self.height)
        else:
            math_logic = ''
        self.height += 1

        if token == 'открыть_скобки':
            ht.append(self.height)
            LBreaket = self.LBreaket()
            math_logic.children.append(LBreaket)

        elif token == 'закрыть_скобки':
            self.height = ht.pop(-1)
            math_logic = Node('закрыть_скобки',  height=self.height)

        elif token == 'число':
            math_logic.children.append(Leaf(list(self.start[self.i].keys())[0],
                                            list(self.start[self.i].
                                                 values())[0],
                                            self.height))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'логическая_операция':
                    self.i += 1
                    math_logic.children.append(Leaf(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.height))

                elif list(self.start[self.i + 1].keys())[0] == 'операция':
                    self.i += 1
                    math_logic.children.append(Leaf(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.height))

        elif token == 'переменная':
            math_logic.children.append(Leaf(list(self.start[self.i].keys())[0],
                                            list(self.start[self.i].
                                                 values())[0],
                                            self.height))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'логическая_операция':
                    self.i += 1
                    math_logic.children.append(Leaf(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.height))

                elif list(self.start[self.i + 1].keys())[0] == 'операция':
                    self.i += 1
                    math_logic.children.append(Leaf(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.height))

        elif token == 'логическая_операция':
            self.height -= 1
            math_logic = Node('логическая_операция' +
                              list(self.start[self.i].values())[0],
                              height=self.height)

        elif token == 'операция':
            self.height -= 1
            math_logic = Node('операция' + list(self.start[self.i].values())[0],
                              height=self.height)

        elif not token == 'окончание_команды':
            raise BaseException

        if len(ht):
            self.i += 1
            me = self.math_logic(ht)
            math_logic.children.append(me)

        return math_logic

    def check_next(self, values):
        token = list(self.start[self.i + 1].keys())[0]
        if not token == values:
            raise BaseException

    def assign_expr(self):
        assign_expr = Node('assign_expr', '=', self.height)
        self.check_next("присвоить")
        self.height += 1
        assign_expr.children.append(Leaf(list(self.start[self.i].keys())[0],
                                         list(self.start[self.i].
                                              values())[0], self.height))
        self.i += 1
        assign_expr.children.append(Leaf(list(self.start[self.i].keys())[0],
                                         list(self.start[self.i].
                                              values())[0], self.height))
        self.height -= 1
        self.i += 1
        token = list(self.start[self.i].keys())[0]
        if token == 'строка':
            self.height += 1
            assign_expr.children.append(Leaf('строка', list(self.start[self.i].
                                                         values())[0],
                                             self.height))
            self.check_next('окончание_команды')
            self.i += 1

        elif token == 'число' or token == 'открыть_скобки' or token == 'переменная':
            self.height += 1
            math_expr = self.math_expr()
            assign_expr.children.append(math_expr)

        elif token == 'связный_список':
            self.height += 1
            assign_expr.children.append(Leaf('связный_список', list(self.start[self.i].values())[0], self.height))

        return assign_expr

    def math_expr(self, ht=[]):
        token = list(self.start[self.i].keys())[0]
        if not token == 'закрыть_скобки' or not token == 'операция' or not token == 'точка':
            math_expr = Node('math_expr', height=self.height)
        else:
            math_expr = ''
        self.height += 1

        if token == 'открыть_скобки':
            ht.append(self.height)
            LBreaket = self.LBreaket()
            math_expr.children.append(LBreaket)

        elif token == 'закрыть_скобки':
            self.LB -= 1
            self.height = ht.pop(-1)
            if self.LB < 0:
                raise BaseException
            math_expr = Node('закрыть_скобки', value=')', height=self.height)

        elif token == 'число':
            math_expr.children.append(Leaf(list(self.start[self.i].keys())[0],
                                           list(self.start[self.i].
                                                values())[0],
                                           self.height))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'операция':
                    self.i += 1
                    math_expr.children.append(Leaf(list(self.start[self.i].
                                                        keys())[0],
                                                   list(self.start[self.i].
                                                        values())[0],
                                                   self.height))

        elif token == 'операция':
            self.height -= 1
            math_expr = Node('операция' + list(self.start[self.i].values())[0],
                             height=self.height)

        elif token == 'переменная':
            math_expr.children.append(Leaf(list(self.start[self.i].keys())[0],
                                           list(self.start[self.i].
                                                values())[0],
                                           self.height))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'операция':
                    self.i += 1
                    math_expr.children.append(Leaf(list(self.start[self.i].
                                                        keys())[0],
                                                   list(self.start[self.i].
                                                        values())[0],
                                                   self.height))

        elif token == 'точка':
            math_expr = self.method()
            self.i -= 1
        elif not token == 'окончание_команды':
            raise BaseException

        self.i += 1
        if not list(self.start[self.i].keys())[0] == 'окончание_команды':
            me = self.math_expr(ht)
            math_expr.children.append(me)

        return math_expr

    def LBreaket(self):
        self.LB += 1
        LBreaket = Leaf('открыть_скобки', '(', height=self.height)

        return LBreaket


class Node:
    def __init__(self, name='', value='', height=0):
        self.children = []
        self.name = name
        self.value = value
        self.height = height
        self.buffer = []

    def __repr__(self):
        str_end = ''
        for child in self.children:
            str_end += "\t" * child.height + f'{child}'
        return f'{self.name}\n{str_end}'


class Leaf:
    def __init__(self, name='', value='', height=0):
        self.name = name
        self.value = value
        self.height = height

    def __repr__(self):
        return f'{self.name} {self.value}\n'
