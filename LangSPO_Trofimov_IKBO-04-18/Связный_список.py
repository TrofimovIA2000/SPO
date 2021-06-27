class Item:
    def __init__(self, value=None):
        self.value = value
        self.nextValue = None


class LinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        current = self.head
        stroka = '[ '
        while current is not None:
            stroka += f'{current.value},'
            current = current.nextValue
        stroka += ']'
        return stroka

    def contains(self, value):
        lastItem = self.head
        while lastItem:
            if value == lastItem.value:
                return True
            else:
                lastItem = lastItem.nextValue
        return False

    def push(self, newValue):
        newItem = Item(newValue)
        if self.head is None:
            self.head = newItem
            return
        lastItem = self.head
        while lastItem.nextValue:
            lastItem = lastItem.nextValue
        lastItem.nextValue = newItem

    def get(self, itemIndex):
        lastItem = self.head
        boxIndex = 0
        while boxIndex <= itemIndex:
            if boxIndex == itemIndex:
                return lastItem.cat
            boxIndex = boxIndex + 1
            lastItem = lastItem.nextValue

    def remove(self, rmValue):
        headItem = self.head

        if headItem is not None:
            if headItem.value == rmValue:
                self.head = headItem.nextValue
                return
        while headItem is not None:
            if headItem.value == rmValue:
                break
            lastItem = headItem
            headItem = headItem.nextValue
        if headItem is None:
            return
        lastItem.nextValue = headItem.nextValue
