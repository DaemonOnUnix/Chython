import ast 
import compiler.parser
import compiler.type_system

class If:
    def __init__(self, ast_node):
        if ast_node.__class__ != ast.If:
            raise TypeError("Expected If node, got " + ast_node.__class__.__name__)
        
        self.test = compiler.parser.parse(ast_node.test)
        self.body = [compiler.parser.parse(a) for a in ast_node.body]
        self.orelse = [compiler.parser.parse(x) for x in ast_node.orelse]
    
    def __repr__(self):
        return f'If({self.test}, {self.body}, {self.orelse})'
    
    def typeof(self, ctx):
        
        tt = self.test.typeof(ctx)
        if not tt.is_num():
            raise TypeError(f"If/else test condition has non-integral type")
        for stmt in self.body:
            print(stmt)
            if stmt.typeof(ctx) != compiler.type_system.UNIT:
                raise TypeError(f"If/else Statement {stmt} has non-UNIT type")
            
        return compiler.type_system.UNIT