import ast
from compiler.parser import parse
from compiler.context import Context

def flatten(xss):
    return [x for xs in xss for x in xs]

class LiftingElement:
    def __init__(self, base_type, target_type):
        self.base_type = base_type
        self.target_type = target_type
    
    def lift(self, obj):
        if obj.__class__ != self.base_type:
            raise TypeError(f"Expected {self.base_type}, got {obj.__class__}")
        return self.target_type(obj)
    
    def __call__(self, obj):
        return self.lift(obj)

class TranslationUnit:
    def __init__(self, name, ast_tree):
        self.name = name

        BODY = []
        TYPES = []
        CTX = Context()
        CTX.push_scope(self.name)

        for i in ast_tree.body:
            parsed = parse(i)
            BODY.append(parsed)
            TYPES.append(parsed.typeof(CTX))
        
        i = 0
        for i in range(len(BODY)):
            print(f'==== EXPR {i} ====')
            print(BODY[i])
            print(f'Type: {TYPES[i]}')
        print(f'==== CTX ====')
        print(CTX)
        