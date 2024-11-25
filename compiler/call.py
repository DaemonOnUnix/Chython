import ast
import compiler.parser

class Call:
    def __init__(self, ast_node):
        if ast_node.__class__ != ast.Call:
            raise TypeError("Expected Call node, got " + ast_node.__class__.__name__)
        self.func = compiler.parser.parse(ast_node.func)
        self.args = []
        for arg in ast_node.args:
            self.args.append(compiler.parser.parse(arg))
        if ast_node.keywords:
            raise NotImplementedError("Keyword arguments are not supported")
        # self.keywords = []
        # for keyword in ast_node.keywords:
        #     self.keywords.append(keyword)
        self.type = None
    
    def __repr__(self):
        return f'Call({self.func}, {self.args})'