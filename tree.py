import random as r

class Node(object):
    """Узел дерева"""
    def __init__(self,  root):
        self.root = root
        self.children = []

    def __str__(self):
        tmp = str(self.root)
        return tmp

    def countCh(self):
        print("!",len(self.children),self.children)
        return len(self.children)

class Tree(object):
    """Описание дерева
    node - корень
    children - дочернии узлы
    """
    def __init__(self, node, children=None):
        self.node = Node(node)
        if children is not None:
            for child in children:
                self.add_child(child)
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
        print("---"*lv, tmp.root)
        if tmp.children is not []:
            for i in tmp.children:
                i.printTree(i, lv+1)

    def find(self, root):
        tmp = self.node
        if int(str(root),10) == int(str(tmp.root),10):
            return self.node
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
            vertex = self.find(root)
            if vertex is not None:
                return vertex.countCh()
            else:
                return 0

def randTree(n):
    """Случайное дерево
    Аргументы:
    n - количество элементов дерева
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
        right.append(left.pop(left.index(tmp)))
        tr.addChild(ind,Tree(tmp))
        print('left =',left, ' right =',right,'ind =',ind,'\n')
        #tr.printTree (head)
    return head,tr

head, tr = randTree(8)
tr.printTree (head)
print()
print(tr.countChild(3))
