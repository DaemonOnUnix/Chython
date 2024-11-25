import ast
from compiler.type_system import *
import compiler.constants
import compiler.id

def do_nothing(ast_tree):
    return True

def do_later(ast_tree):
    return None

class Typer:
    def __init__(self, NodeType, FunctionToType, FunctionToCheckCompat):
        self.NodeType, self.FunctionToType = NodeType, FunctionToType
        self.FunctionToCheckCompat = FunctionToCheckCompat

functions_to_type = [
    Typer(compiler.constants.Constant, TypeUnit.constant_type, do_nothing),
    Typer(compiler.id.Id, do_later, do_nothing)
]

def typeof(ast_node):
    for i in functions_to_type:
        if i.NodeType == ast_node.__class__:
            current_type = i.FunctionToType(ast_node)
            if i.FunctionToCheckCompat(current_type):
                return current_type
            else:
                raise TypeError("Incompatible type")
    raise Exception(f'''No function to type {ast_node.__class__}''')

