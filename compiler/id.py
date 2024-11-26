import ast

class Id:
    def __init__(self, name):
        if name.__class__ != ast.Name:
            raise TypeError(f"Expected Name node, got {name.__class__.__name__}")
        self.name = name.id.split('->')
    
    def __repr__(self):
        return f'Id({self.name})'
    
    @staticmethod
    def from_str(str):
        return Id(ast.Name(str))
    
    def typeof(self, ctx):
        Element = ctx.get(self)
        if Element:
            return Element.typeof(ctx)
        else:
            print(ctx)
            print(self)
            raise NameError(f"Name '{self}' is not defined")
    
    def __eq__(self, o):
        return self.name == o.name
    
    def __ne__(self, o):
        return self.name != o.name