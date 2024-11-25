import ast
import compiler.parser

OP_LIST = {
    ast.Add: '+',
    ast.Sub: '-',
    ast.Div: '/',
    ast.Mod: '%',
    ast.Mult: '*',
    ast.LShift: '<<',
    ast.RShift: '>>',
    ast.BitOr: '|',
    ast.BitXor: '^',
    ast.BitAnd: '&',
    ast.FloorDiv: '/',
}

class BinOp:
    def __init__(self, ast_node):
        if ast_node.__class__ != ast.BinOp:
            raise TypeError("Expected BinOp node, got " + ast_node.__class__.__name__)
        self.left = compiler.parser.parse(ast_node.left)
        self.right = compiler.parser.parse(ast_node.right)
        self.op = OP_LIST[ast_node.op.__class__]
    
    def __repr__(self):
        return f'BinOp({self.left}, {self.op}, {self.right})'
