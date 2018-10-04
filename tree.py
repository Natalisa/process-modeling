import random as r

class Node(object):
    """Узел дерева"""
    def __init__(self,  root, level):
        self.root = root
        self.level = level
        self.children = []

    def __str__(self):
        tmp = str(self.root)
        return tmp

    def countCh(self):
        return len(self.children)

class Tree(object):
    """Описание дерева
    node - корень
    children - дочернии узлы
    """
    def __init__(self, node, children = None):
        self.node = Node(node, 0)

    def __repr__(self):
        return str(self.node.root)
    def __str__(self):
        return str(self.node.root)

    def addChild(self, root, node):
    #    assert isinstance(node, Tree)
        tmp = self.node
        if int(str(root),10) == int(str(tmp.root),10):
            tmp.children.append(node)
        else:
            for i in tmp.children:
                i.addChild(root,node)

    def printTree(self, root, lv = 0):
        tmp = self.node
        print("---"*lv, tmp.root, "lv", tmp.level)
        if tmp.children is not []:
            for i in tmp.children:
                i.printTree(i, lv+1)

    def find(self, root):
        tmp = self.node
        if int(str(root),10) == int(str(tmp.root),10):
            return tmp
        else:
            for i in tmp.children:
                i.find(root)

    def countChild(self, root=None):
        tmp = self.node

        if root is None:
            print("Vertex",str(tmp.root),"have",tmp.countCh(),"child")
            if tmp.children is not []:
                for i in tmp.children:
                    i.countChild()

        if root is not None:
            if str(tmp.root) == str(root):
                return tmp.countCh()
            else:
                if tmp.children is not []:
                    res = 0
                    for i in tmp.children:
                        res += i.countChild(root)
                    return res

def randTree(n, countNode = None, countLevel = None):
    """Случайное дерево
    Аргументы:
    n - количество элементов дерева
    countNode - ограничение на количество дочерних
    countLevel - ограничение на количество уровней
    Возвращает:
    head - голова дерева
    tr - случайное дерево
    """
    left = list(range(1,n+1))
    right = []

    head = r.choice(left)
    tr = Tree(head)
    right.append(left.pop(left.index(head)))

    print('left =',left, ' right =',right,'\n')
    while left:
        tmp = r.choice(left)
        ind = r.choice(right)
        if countNode is None or tr.countChild(ind) < countNode:
            right.append(left.pop(left.index(tmp)))
        else:
            right.pop(right.index(ind))
            continue
        tr.addChild(ind,Tree(tmp))
        print('left =',left, ' right =',right,'ind =',ind,'\n')
        #tr.printTree (head)
    return head,tr

head, tr = randTree(10, countLevel = 6)
tr.printTree (head)
print()
#print('количество:', tr.find(3).level)

