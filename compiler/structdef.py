import ast
import compiler.parser

class Struct:
    def __init__(self, astNode):
        if astNode.__class__ != ast.ClassDef:
            raise TypeError(f"Expected ClassDef node, got {astNode.__class__.__name__}")
        print(ast.dump(astNode))
        self.name = compiler.id.Id.from_str(astNode.name)
        print(self.name)
        self.fields = [compiler.parser.parse(x) for x in astNode.body]
    
    def __repr__(self):
        return f'Struct({self.name}, {self.fields})'