import ast

#deduces the type of a python expression with a binary operator by looking at the AST
#returns the python type of the expression
#returns None if the type cannot be deduced
def get_type_binop(node, vardict={}):
    if node.__class__ == ast.BinOp:
        left =  get_type(node.left, vardict)
        right = get_type(node.right, vardict)
        if left is None or right is None:
            return None
        if node.op.__class__ == ast.Add or node.op.__class__ == ast.Sub or node.op.__class__ == ast.Mult or node.op.__class__ == ast.Div or node.op.__class__ == ast.Pow or node.op.__class__ == ast.Mod or node.op.__class__ == ast.FloorDiv or node.op.__class__ == ast.BitOr or node.op.__class__ == ast.BitAnd or node.op.__class__ == ast.BitXor:
            if left == 'int' and right == 'int':
                return 'int'
            elif left == 'float' and right == 'float':
                return 'float'
            elif left == 'str' and right == 'str':
                return 'str'
            elif left == 'bool' and right == 'bool':
                return 'bool'
            elif left == 'NoneType' and right == 'NoneType':
                return 'NoneType'
            elif left == 'list' and right == 'list':
                return 'list'
            elif left == 'u16' and right == 'u16':
                return 'u16'
            elif left == 'u32' and right == 'u32':
                return 'u32'
            elif left == 'u64' and right == 'u64':
                return 'u64'
            else:
                return None
        elif node.op.__class__ == ast.LShift or node.op.__class__ == ast.RShift or node.op.__class__ == ast.BitOr or node.op.__class__ == ast.BitAnd or node.op.__class__ == ast.BitXor:
            if left == 'int' and right == 'int':
                return 'int'
            elif left == 'u16' and right == 'u16':
                return 'u16'
            elif left == 'u32' and right == 'u32':
                return 'u32'
            elif left == 'u64' and right == 'u64':
                return 'u64'
            else:
                return None
        return None
    return None
    

#deduces the type of a python expression by looking at the AST
#returns the python type of the expression
#returns None if the type cannot be deduced
def get_type(node, vardict={}):
    if isinstance(node, ast.Constant):
        return type(node.value)
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.BinOp):
        return get_type_binop(node, vardict)
    elif isinstance(node, ast.UnaryOp):
        return get_type_unop(node, vardict)
