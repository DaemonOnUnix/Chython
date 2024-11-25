import ast
#from compiler.importdef import Import
#from compiler.functiondef import Function
#from compiler.structdef import Struct
#from compiler.variabledef import VariableInstanciation, Variable
from compiler.parser import parse

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

        # CORRELATION = {
        #     ast.Import: [],
        #     ast.FunctionDef: [],
        #     ast.ClassDef: [],
        #     ast.Assign: [],
        #     ast.AnnAssign: []
        # }

        # TYPE_CORRELATION = {
        #     ast.Import: LiftingElement(ast.Import, Import),
        #     ast.FunctionDef: LiftingElement(ast.FunctionDef, Function),
        #     ast.ClassDef: LiftingElement(ast.ClassDef, Struct),
        #     ast.Assign: LiftingElement(ast.Assign, VariableInstanciation),
        #     ast.AnnAssign: LiftingElement(ast.AnnAssign, VariableInstanciation)
        # }

        # COLLECT

        BODY = []

        for i in ast_tree.body:
            BODY.append(parse(i))
            #for k in CORRELATION.keys():
            #    if i.__class__ == k:
            #        CORRELATION[k].append(i)
        
        print('Parsing log:')
        for i in BODY:
            print(i)
        return

        # LIFT

        for k in TYPE_CORRELATION.keys():
            CORRELATION[k] = [TYPE_CORRELATION[k](x) for x in CORRELATION[k]]
        
        # MERGE        
        
        self.rawImports = CORRELATION[ast.Import]
        self.rawFunctions = CORRELATION[ast.FunctionDef]
        self.rawStructs = CORRELATION[ast.ClassDef]
        self.rawAssigns = CORRELATION[ast.Assign] + CORRELATION[ast.AnnAssign]


        # DEBUG
        print('Parsing log:')
        print(self.rawImports)
        print(self.rawFunctions)
        print(self.rawStructs)
        print(self.rawAssigns)
        
        self.rawStaticAssign = []
        # XXX Raww assigns
        #for i in ast_tree.body:
    
    def GetHLR(self):
        self.imports = []
        for i in self.rawImports:
            self.imports.append(Import(i))
        self.functions = []
        for i in self.rawFunctions:
            self.functions.append(Function(i))
        self.structs = []
        # XXX Should add namespace mangling for methods here
        for i in self.rawStructs:
            self.structs.append(Struct(i))