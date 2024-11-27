import ast
import compiler.parser
import compiler.type_system

OP_LIST = {
    ast.Eq: '==',
    ast.NotEq: '!=',
    ast.Lt: '<',
    ast.LtE: '<=',
    ast.Gt: '>',
    ast.GtE: '>=',
    ast.Is: 'is',
    ast.IsNot: 'is not',
    ast.In: 'in',
    ast.NotIn: 'not in',
}

class Compare:
    def __init__(self, ast_node):
        if ast_node.__class__ != ast.Compare:
            raise TypeError("Expected If node, got " + ast_node.__class__.__name__)
        
        self.left = compiler.parser.parse(ast_node.left)
        self.ops = [OP_LIST[x.__class__] for x in ast_node.ops]
        self.comparators = [compiler.parser.parse(x) for x in ast_node.comparators]
    
    def __repr__(self):
        return f'Compare({self.left}, {self.ops}, {self.comparators})'
    
    def typeof(self, ctx):
        tl = self.left.typeof(ctx)    
        tc = [x.typeof(ctx) for x in self.comparators]
                    
        if not (tl.is_num() and (x.is_num() for x in tc)):
            raise TypeError(f"Expected numbers, got {tl} for left operand and {(x for x in tc)}")
        
        return compiler.type_system.Type('u8')
        
