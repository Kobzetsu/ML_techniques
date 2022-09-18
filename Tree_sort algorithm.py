class tree:
    # Создание структуры дерева
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def insert(self, value):
        if self.value:
            if value < self.value:
                if self.left is None:
                    self.left = tree(value)
                else:
                    self.left.insert(value)
            elif value > self.value:
                if self.right is None:
                    self.right = tree(value)
                else:
                    self.right.insert(value)
        else:
            self.value = value


def recursive_trav(root, res):
    # Рекурсивный обход дерева
    if root:
        recursive_trav(root.left, res)
        res.append(root.value)
        recursive_trav(root.right, res)


def tree_sort(arr):
    if len(arr) == 0:
        return arr
    root = tree(arr[0])
    for i in range(1, len(arr)): # закидываем все в дерево
        root.insert(arr[i])
    res = []
    recursive_trav(root, res) # обходим построенное дерево
    return res
