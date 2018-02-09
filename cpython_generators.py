#cpython/Lib/test/test_generators.py

class Tree:
    def __init__(self, label, left=None, right=None):
        self.label = label
        self.left = left
        self.right = right

    def __repr__(self, level=0, indent="    "):
        s = level*indent + repr(self.label)
        if self.left:
            s = s + "\\n" + self.left.__repr__(level + 1, indent)
        if self.right:
            s = s + "\\n" + self.right.__repr__(level + 1, indent)
        return s

    def __iter__(self):
        return inorder(self)

def tree(list):
    n = len(list)
    if n == 0:
        return []
    i = n // 2
    return Tree(list[i], tree(list[:i]), tree(list[i+1:]))

def inorder(t):
    if t:
        for x in inorder(t.left):
            yield x
        yield t.label
        for x in inorder(t.right):
            yield x

if __name__ == '__main__':
    t = tree("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    print(t)
