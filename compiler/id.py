import ast

class Id:
    def __init__(self, name):
        if name.__class__ != ast.Name:
            raise TypeError(f"Expected Name node, got {name.__class__.__name__}")
        self.name = name.id
    
    def __repr__(self):
        return f'Id({self.name})'
    
    @staticmethod
    def from_str(str):
        return Id(ast.Name(str))