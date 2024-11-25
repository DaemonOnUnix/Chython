import ast
import compiler.id
import compiler.parser

class FunArg:
    def __init__(self, name, _type):
        self.name = name
        self.type = _type
    
    def __repr__(self):
        return f'FunArg({self.name}, {self.type})'

class Return:
    def __init__(self, ast_node):
        if ast_node.__class__ != ast.Return:
            raise TypeError(f"Expected Return node, got {ast_node.__class__.__name__}")
        self.value = compiler.parser.parse(ast_node.value)
    
    def __repr__(self):
        return f'Return({self.value})'

class Pass:
    def __init__(self, ast_node):
        if ast_node.__class__ != ast.Pass:
            raise TypeError(f"Expected Pass node, got {ast_node.__class__.__name__}")
    
    def __repr__(self):
        return 'Pass()'

class Function:
    def __init__(self, astNode):
        if astNode.__class__ != ast.FunctionDef:
            raise TypeError(f"Expected FunctionDef node, got {astNode.__class__.__name__}")
        self.name = compiler.id.Id.from_str(astNode.name)
        self.args = [FunArg(arg.arg, arg.annotation.id if arg.annotation else None) for arg in astNode.args.args]
        self.body = [compiler.parser.parse(x) for x in astNode.body]
    
    def __repr__(self):
        return f'Function({self.name}, {self.args}, {self.body})'