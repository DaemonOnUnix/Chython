import ast
import compiler.typeof
import compiler.type_system

class Constant:
    def __init__(self, ast_node):
        if ast_node.__class__ != ast.Constant:
            raise TypeError("Expected Constant node, got " + ast_node.__class__.__name__)
        self.value = ast_node.value
        self.type = compiler.type_system.TypeUnit.constant_type(self)
    
    def __repr__(self):
        return f'Constant({self.value}, {self.type})'
    
    def typeof(self, ctx):
        return self.type
