import ast
import compiler.parser

OP_LIST = {
    ast.Subscript: '[]',
}

class Subscript:
    def __init__(self, ast_node):
        if ast_node.__class__ != ast.Subscript:
            raise TypeError("Expected Subscript node, got " + ast_node.__class__.__name__)
        self.value = compiler.parser.parse(ast_node.value)
        
        if isinstance(ast_node.slice, tuple) or isinstance(ast_node, slice):
            raise TypeError("Indexing list using tuples or slices are not allowed")
        
        self.slice = compiler.parser.parse(ast_node.slice)
    
    def __repr__(self):
        return f'Subscript({self.value}, {self.slice})'
    
    # XXX Handle integers AND Floats
    def typeof(self, ctx):
        # raise TypeError(f"Not implemented")
        
        # Need to return type of self.value type
        return 'None'