import ast
import compiler.parser

OP_LIST = {
    ast.Invert: '~',
    ast.UAdd: '+',
    ast.USub: '-',
    ast.Not: 'not',
}

class UnOp:
    def __init__(self, ast_node):
        if ast_node.__class__ != ast.UnaryOp:
            raise TypeError("Expected UnOp node, got " + ast_node.__class__.__name__)
        self.operand = compiler.parser.parse(ast_node.operand)
        self.op = OP_LIST[ast_node.op.__class__]
    
    def __repr__(self):
        return f'UnOp({self.op}, {self.operand})'
    
    # XXX Handle integers AND Floats
    def typeof(self, ctx):
        # raise TypeError(f"Not implemented")
        return 'None'