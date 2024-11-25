import ast
from compiler.importdef import Import
from compiler.functiondef import Function, Return, Pass
from compiler.structdef import Struct
from compiler.variabledef import VariableInstanciation, Variable
from compiler.constants import Constant
from compiler.id import Id
from compiler.binop import BinOp
from compiler.call import Call

from compiler.static_transforms import apply_transfos

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

TYPE_CORRELATION = {
    ast.Import: LiftingElement(ast.Import, Import),
    ast.FunctionDef: LiftingElement(ast.FunctionDef, Function),
    ast.ClassDef: LiftingElement(ast.ClassDef, Struct),
    ast.Assign: LiftingElement(ast.Assign, VariableInstanciation),
    ast.AnnAssign: LiftingElement(ast.AnnAssign, VariableInstanciation),
    ast.Constant: LiftingElement(ast.Constant, Constant),
    ast.Name: LiftingElement(ast.Name, Id),
    ast.Return: LiftingElement(ast.Return, Return),
    ast.BinOp: LiftingElement(ast.BinOp, BinOp),
    ast.Call: LiftingElement(ast.Call, Call),
    ast.Pass: LiftingElement(ast.Pass, Pass)
}

def parse(ast_node):
    ast_node = apply_transfos(ast_node)
    constructed = None
    for k in TYPE_CORRELATION.keys():
        if ast_node.__class__ == k:
            constructed = TYPE_CORRELATION[k](ast_node)
    if not constructed:
        raise TypeError(f"Unexpected ast node: {ast_node.__class__}")
    return constructed