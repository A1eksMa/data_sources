import random


class Tree():
    '''
    It's a main class - The Tree.
    '''


    class Node():
        '''
        This abstract node of Tree
        '''
        def __init__(self, node=None, parent=None, children=None):
            self.validate(node, parent, children)
            self.node = node if node is not None else self.Seed()
            self.parent = parent
            self.children = children if children is not None else []

        def validate(self, node, parent, children):
            self.valid_node(node)
            self.valid_parent(parent)
            self.valid_children(children)
            if node is not None and parent is not None and node==parent:
                raise ValueError("Incorrect parent's element")
            if isinstance(children, list) and (node in children or parent in children):
                raise ValueError("Incorrect childrens's element")

        def valid_node(self, node):
            if node is not None and not isinstance(node, self.Seed):
                raise TypeError("Invalid node type. Expected None or Tree.Node.Seed() object.")

        def valid_parent(self, parent):
            if parent is not None and not isinstance(parent, self.Seed):
                raise TypeError("Invalid type of parent's element. Expected None or Tree.Node.Seed() object.")

        def valid_children(self, children):
            if children is not None:
                if not isinstance(children, list):
                    raise TypeError("Invalid children type. Expected None or list.")
                else:
                    for i in children:
                        if not isinstance(i, self.Seed):
                            raise TypeError("Invalid children type. Expected list of Tree.Node.Seed() object.")

        def add_child(self, child):
            if not isinstance(child, self.Seed):
                raise TypeError("Invalid type of children's element. Expected Tree.Node.Seed() object.")
            if child == self.node or child == self.parent:
                raise ValueError("Incorrect childrens's element")

            if not self.children:
                self.children = [child]
            elif child in self.children:
                raise ValueError(f"Child {child} already exist")
            else:
                self.children.append(child)

        def remove_child(self, child):
            try:
                self.children.remove(child)
            except Exception as e:
                print(f'Impossible to remove child {child}:', e)

        def set_parent(self, parent):
            self.valid_parent(parent)
            if parent is None or parent in self.children or parent == self.node:
                raise ValueError("Incorrect parent's element")
            self.parent = parent

        def get_parent(self):
            return self.parent

        def get_children(self):
            return self.children

        def __repr__(self):
            children = []
            if self.children is not None:
                for i in self.children:
                    children.append(i.sid)
            return f"Node: {self.node}\nParent: {self.parent}\nChildren: {children})\n"

        def __str__(self):
            return self.node.sid

        def __eq__(self, other):
            if isinstance(other, Tree.Node):
                return self.node.sid == other.node.sid
            return False

        def __hash__(self):
            return hash(self.node.sid)


        class Seed():
            '''
            Unique system id (sid): random chars
            '''

            # Set default longsize of sid
            __n = 4

            def sid(self, n=__n):
                '''
                Generate random system id
                '''
                string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                id = ''.join(random.choice(string) for i in range(n))
                while hash(id) <= 0:
                    id = ''.join(random.choice(string) for i in range(n))
                return id

            def __init__(self, id=None):
                self.sid = id if id is not None else self.sid()

            def __repr__(self):
                return ('Object type: ' +  str(self.__class__)  + '\n' +
                        'Object ID: ' + str(id(self)) + '\n' +
                        'System Identificator (sid): ' + self.sid)

            def __str__(self):
                return self.sid

            def __eq__(self, other):
                if isinstance(other, Tree.Node.Seed):
                    return self.sid == other.sid
                return False

            def __hash__(self):
                return hash(self.sid)

            def __bool__(self):
                if isinstance(self.sid, str) and len(self.sid) == self.__n and hash(self.sid) > 0:
                    allowed_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                    if all(char in allowed_chars for char in self.sid):
                        return True
                return False


    # And other classes, based on Node() class:

    class Root(Node):
        '''
        It's a Root of Tree, singleton class, that parent is None always
        '''
        pass


    class Branch(Node):
        '''
        It's a Branch of Tree class, that must have a parent
        '''
        pass


    class Leaf(Branch):
        '''
        Leaf class have no children.
        This is endpoint of Tree.
        '''
        pass
