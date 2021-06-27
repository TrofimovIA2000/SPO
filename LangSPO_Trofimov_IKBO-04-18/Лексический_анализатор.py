import re


class Lexer(object):
    token = {"если": "^if$", "иначе": "^else$", "пока": "^while$",
              "операция": "^[-+*/]$", "логическая_операция": r"^==|>|>=|<|<=|!=$",
              "открыть_скобки": "[(]", "закрыть_скобки": "[)]", 'точка': r'\.',
              "окончание_команды": "^;$", "начало": "^[{]$",
             'связный_список': r'LinkedList',
              "конец": "^[}]$", "присвоить": "^=$",
              "окончание": "^;$", "число": r"^0|([1-9][0-9]*)$",
              "строка": r"'[^']*'", "переменная": "^[a-zA-Z0-9_]+$",
              "ошибка": r".*[^.]*"}

    def __init__(self):
        self.list_tokens = []

    def initToken(self, item):
        for key in self.token.keys():
            if re.fullmatch(self.token[key], item):
                return key

    def term(self, file):
        with open(file) as file_handler:
            buffer = ''
            last_token = ''
            for line in file_handler:
                for char in line:
                    if not len(buffer) and char == "'":
                        buffer += char
                        continue
                    elif len(buffer) and not buffer.count("'") == 2:
                        if buffer[0] == "'":
                            buffer += char
                            continue

                    if last_token == 'точка':
                        if not char == '(':
                            buffer += char
                            continue
                        else:
                            self.list_tokens.append({'METHOD': buffer})
                            buffer = ''

                    last_token = self.initToken(buffer)
                    buffer += char
                    token = self.initToken(buffer)

                    if token == "ошибка":
                        if len(buffer) and not last_token == "ошибка":
                            self.list_tokens.append({last_token: buffer[:-1]})
                        if not (buffer[-1] == ' ' or buffer[-1] == '\n'):
                            buffer = buffer[-1]
                        else:
                            buffer = ''

            token = self.initToken(buffer)
            if not token == "ошибка":
                self.list_tokens.append({token: buffer[0]})
