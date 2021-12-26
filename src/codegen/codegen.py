import ast
import equivalences.equivalences as equivalences
import sysnake_builtins.sysnake_builtins as builtins

def codegen_op_from_node(op):
    if op.__class__ == ast.Add:
        return '+'
    elif op.__class__ == ast.Sub:
        return '-'
    elif op.__class__ == ast.Mult:
        return '*'
    elif op.__class__ == ast.Div:
        return '/'
    elif op.__class__ == ast.Mod:
        return '%'
    elif op.__class__ == ast.Pow:
        raise Exception('Pow not implemented')
    elif op.__class__ == ast.LShift:
        return '<<'
    elif op.__class__ == ast.RShift:
        return '>>'
    elif op.__class__ == ast.BitOr:
        return '|'
    elif op.__class__ == ast.BitXor:
        return '^'
    elif op.__class__ == ast.BitAnd:
        return '&'
    elif op.__class__ == ast.FloorDiv:
        return '/'
    elif op.__class__ == ast.Invert:
        return '~'
    elif op.__class__ == ast.Not:
        return '!'
    raise Exception('Unknown op: ' + str(op))

#descends int the value of slice and returns the type of the slice with the depth
def get_slice_type(slice, depth=0):
    if slice.__class__ == ast.Index:
        return get_slice_type(slice.value, depth+1)
    elif slice.__class__ == ast.Slice:
        return get_slice_type(slice.lower, depth+1)
    elif slice.__class__ == ast.ExtSlice:
        return get_slice_type(slice.dims[0], depth+1)
    elif slice.__class__ == ast.Ellipsis:
        return (depth, 'list')
    elif slice.__class__ == ast.Tuple:
        return (depth, 'tuple')
    elif slice.__class__ == ast.Name:
        return (depth, slice.id)
    elif slice.__class__ == ast.Subscript:
        return get_slice_type(slice.slice, depth)
    raise Exception('Unknown slice type: ' + str(slice))

#checks that all list levels have the same length
#e.g. [1,2,3] -> [3]
#e.g. [[1, 2], [3, 4], [5, 6]] -> [3, 2]
#e.g. [[1, 2], [3]] -> None
def check_list_lengths(a):
    L = a.elts
    if len(L) == 0:
        return []
    if L[0].__class__ != ast.List:
        return [len(L)]
    val = check_list_lengths(L[0])
    for i in range(1, len(L)):
        if val is None:
            return None
        if val != check_list_lengths(L[i]):
            return None
    return [len(L)] + val


def codegen_subscript(node, name="", value=None):
    if node.value.id == 'list':
        depth, ty = get_slice_type(node.slice)
        s =  f"{equivalences.py_type_to_c_type(ty)} {name}"
        sizes = check_list_lengths(value)
        if sizes is None:
            raise Exception('List cannot be indexed by a slice with different lengths')
        temp = ''
        for i in range(depth-1):
            temp = "[" + str(sizes[depth - 1 - i]) + "]" + temp
        temp = '[]' + temp
        return s + temp
    raise Exception('Unknown subscript: ' + str(node))

def codegen_annotation(ann, arg, value=None):
    if ann.__class__ == ast.Name:
        return equivalences.py_type_to_c_type(ann.id) + " " + arg
    elif ann.__class__ == ast.Subscript:
        return codegen_subscript(ann, arg, value)
    raise Exception('Unknown annotation: ' + str(ann))

def codegen_args(args):
    acc = ""
    for arg in args:
        acc += codegen_annotation(arg.annotation, arg.arg)

        if arg != args[-1]:
            acc += ','
    return acc

def codegen_func_def(node):
    acc = ''
    if isinstance(node.returns, ast.Constant) or node.returns is None:
        acc = f"void {node.name}("
    else:
        acc = f"{equivalences.py_type_to_c_type(node.returns.id)} {node.name}("

    acc += codegen_args(node.args.args) + ")\n{\n"

    for i in node.body:
        # print(str(i))
        acc += codegen_node(i) + ';\n'

    acc += "}\n"
    return acc

def codegen_node(node):
    code = ''
    if node.__class__ == ast.FunctionDef:
        code = codegen_func_def(node)
    elif node.__class__ == ast.AnnAssign:
        code = codegen_assign(node)
        # code += ';\n'
    elif node.__class__ == ast.Return:
        code = f'return {codegen_expr(node.value)};\n'
    elif node.__class__ == ast.AugAssign:
        code = f'{codegen_expr(node.target)} {codegen_op_from_node(node.op)}= {codegen_expr(node.value)};\n'
    elif node.__class__ == ast.Assign:
        code = f'{codegen_expr(node.targets[0])} = {codegen_expr(node.value)};\n'
    elif node.__class__ == ast.Expr:
        code = codegen_expr(node.value)
    elif node.__class__ == ast.If:
        code = f'if ({codegen_expr(node.test)}) {{\n'
        for i in node.body:
            code += codegen_node(i)
        code += '}\n'
        for i in node.orelse:
            code += codegen_node(i)
    elif node.__class__ == ast.While:
        code = f'while ({codegen_expr(node.test)}) {{\n'
        for i in node.body:
            code += codegen_node(i)
        code += '}\n'
        for i in node.orelse:
            code += codegen_node(i)
    elif node.__class__ == ast.For:
        code = f'for ({codegen_expr(node.target)} in {codegen_expr(node.iter)}) {{\n'
        for i in node.body:
            code += codegen_node(i)
        code += '}\n'
        for i in node.orelse:
            code += codegen_node(i)
    elif node.__class__ == ast.Pass:
        code = ';\n'
    elif node.__class__ == ast.Break:
        code = 'break;\n'
    elif node.__class__ == ast.Continue:
        code = 'continue;\n'
    return code

def codegen_expr(node):
    if node.__class__ == ast.Constant:
        if node.value == None:
            return 'NULL'
        elif node.value == "True":
            return 'true'
        elif node.value == "False":
            return 'false'
        elif type(node.value) == str:
            val = node.value.replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t').replace('\0', '\\0')
            if len(node.value) > 1:
                return f'"{val}"'
            else:
                return f'\'{val}\''
        return str(node.value)
    elif node.__class__ == ast.Name:
        return node.id
    elif node.__class__ == ast.List:
        s = '{'
        for i in node.elts:
            s += codegen_expr(i)
            if i != node.elts[-1]:
                s += ', '
        s += '}'
        return s
    elif node.__class__ == ast.Subscript:
        return f'{codegen_expr(node.value)}{codegen_subscript(node)}'
    elif node.__class__ == ast.BinOp:
        return f'({codegen_expr(node.left)} {codegen_op_from_node(node.op)} {codegen_expr(node.right)})'
    elif node.__class__ == ast.UnaryOp:
        return f'{codegen_op_from_node(node.op)} {codegen_expr(node.operand)}'
    elif node.__class__ == ast.Call:
        return codegen_func_call(node)
    elif node.__class__ == ast.Attribute:
        print('Attribute: ' + str(node))
        return f'{codegen_expr(node.value)}.{node.attr}'
    elif node.__class__ == ast.Compare:
        return f'({codegen_expr(node.left)} {codegen_op_from_node(node.ops[0])} {codegen_expr(node.comparators[0])})'
    elif node.__class__ == ast.BoolOp:
        return f'({codegen_expr(node.values[0])} {codegen_op_from_node(node.op)} {codegen_expr(node.values[1])})'
    elif node.__class__ == ast.IfExp:
        return f'({codegen_expr(node.test)} ? {codegen_expr(node.body)} : {codegen_expr(node.orelse)})'
    elif node.__class__ == ast.Dict:
        raise Exception('Dict not implemented')
    elif node.__class__ == ast.Set:
        raise Exception('Set not implemented')
    elif node.__class__ == ast.ListComp:
        raise Exception('ListComp not implemented')
    elif node.__class__ == ast.SetComp:
        raise Exception('SetComp not implemented')
    elif node.__class__ == ast.DictComp:
        raise Exception('DictComp not implemented')
    elif node.__class__ == ast.GeneratorExp:
        raise Exception('GeneratorExp not implemented')
    elif node.__class__ == ast.Yield:
        raise Exception('Yield not implemented')
    elif node.__class__ == ast.YieldFrom:
        raise Exception('YieldFrom not implemented')
    elif node.__class__ == ast.Await:
        raise Exception('Await not implemented')
    raise Exception('Unknown node: ' + str(node))

def codegen_func_call(call):
    s = ''
    if call.func.id not in builtins.builtins:
        s += f"{call.func.id}("

        for arg in call.args:
            codegen_expr(arg)

            if arg != call.args[-1]:
                s += ","

        s += ")"
    else:
        function_info = builtins.builtins[call.func.id]
        arity = function_info[0]
        if arity != len(call.args):
            raise Exception(f'Function {call.func.id} expects {arity} arguments, got {len(call.args)}')
        s += f"{call.func.id}("
        for i in range(arity):
            s += codegen_expr(call.args[i])
            if i != arity - 1:
                s += ", "
        s += ")"
        function_info[2]()
    return s

def codegen_assign(node):
    s = ''
    s += codegen_annotation(node.annotation, node.target.id, node.value)
    s += ' = '
    s += codegen_expr(node.value)
    return s

def codegen(parsed, debug=False):
    s = ''
    if debug:
        print(ast.dump(parsed))
    for node in parsed.body:
        s += codegen_node(node)
    return s
