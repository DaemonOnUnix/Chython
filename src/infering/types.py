import ast

BUILTIN_TYPES = ['int', 'float', 'str', 'bool', 'NoneType', 'list', 'u16', 'u32', 'u64', 'i16', 'i32', 'i64', 'keyword']
BUILTIN_TOKENS = {
    'None': 'NoneType',

    'True': 'bool',
    'False': 'bool',

    'int': 'keyword',
    'float': 'keyword',
    'str': 'keyword',
    'bool': 'keyword',
    'list': 'keyword',
    'u16': 'keyword',
    'u32': 'keyword',
    'u64': 'keyword',
    'i16': 'keyword',
    'i32': 'keyword',
    'i64': 'keyword',

    'enum': 'keyword',
    'struct': 'keyword',
    'union': 'keyword',
    'class': 'keyword',

    'if': 'keyword',
    'elif': 'keyword',
    'else': 'keyword',
    'for': 'keyword',
    'while': 'keyword',
    'break': 'keyword',
    'continue': 'keyword',
    'return': 'keyword',
    'pass': 'keyword',
    'def': 'keyword',

}

#deduces the type of a python expression with a binary operator by looking at the AST
#returns the python type of the expression
#returns None if the type cannot be deduced
def get_type_binop(node, vardict={}):
    if node.__class__ == ast.BinOp:
        left =  get_type(node.left, vardict)
        right = get_type(node.right, vardict)
        if left is None or right is None:
            return None
        if node.op.__class__ == ast.Add or node.op.__class__ == ast.Sub or node.op.__class__ == ast.Mult or node.op.__class__ == ast.Div or node.op.__class__ == ast.Mod or node.op.__class__ == ast.FloorDiv or node.op.__class__ == ast.BitOr or node.op.__class__ == ast.BitAnd or node.op.__class__ == ast.BitXor:
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
            elif left == 'i16' and right == 'i16':
                return 'i16'
            elif left == 'i32' and right == 'i32':
                return 'i32'
            elif left == 'i64' and right == 'i64':
                return 'i64'
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
        elif node.op.__class__ == ast.Eq or node.op.__class__ == ast.NotEq or node.op.__class__ == ast.Lt or node.op.__class__ == ast.LtE or node.op.__class__ == ast.Gt or node.op.__class__ == ast.GtE:
            if left == 'int' and right == 'int':
                return 'bool'
            elif left == 'float' and right == 'float':
                return 'bool'
            elif left == 'str' and right == 'str':
                return 'bool'
            elif left == 'bool' and right == 'bool':
                return 'bool'
            elif left == 'NoneType' and right == 'NoneType':
                return 'bool'
            elif left == 'list' and right == 'list':
                return 'bool'
            elif left == 'u16' and right == 'u16':
                return 'bool'
            elif left == 'u32' and right == 'u32':
                return 'bool'
            elif left == 'u64' and right == 'u64':
                return 'bool'
            elif left == 'i16' and right == 'i16':
                return 'bool'
            elif left == 'i32' and right == 'i32':
                return 'bool'
            elif left == 'i64' and right == 'i64':
                return 'bool'
            else:
                return None
        return None
    return None
    

#deduces the type of a python expression with a unary operator by looking at the AST
#returns the python type of the expression
#returns None if the type cannot be deduced
def get_type_unop(node, vardict={}):
    if node.__class__ == ast.UnaryOp:
        right = get_type(node.operand, vardict)
        if right is None:
            return None
        if node.op.__class__ == ast.Not or node.op.__class__ == ast.Invert:
            if right == 'bool':
                return 'bool'
            else:
                return None
        elif node.op.__class__ == ast.UAdd or node.op.__class__ == ast.USub:
            if right == 'int':
                return 'int'
            elif right == 'float':
                return 'float'
            elif right == 'u16':
                return 'u16'
            elif right == 'u32':
                return 'u32'
            elif right == 'u64':
                return 'u64'
            elif right == 'i16':
                return 'i16'
            elif right == 'i32':
                return 'i32'
            elif right == 'i64':
                return 'i64'
            else:
                return None
    return None

#converts a python type to a token type
#returns the token type
#returns None if the type cannot be converted
#Example : <class 'int'> -> 'int'
def get_token_type(py_type) -> str:
    if str(py_type) == "<class 'int'>":
        return 'int'
    elif str(py_type) == "<class 'float'>":
        return 'float'
    elif str(py_type) == "<class 'str'>":
        return 'str'
    elif str(py_type) == "<class 'bool'>":
        return 'bool'
    elif str(py_type) == "<class 'NoneType'>":
        return 'NoneType'
    elif str(py_type) == "<class 'list'>":
        return 'list'
    return py_type

#return the type as a string of form 'list of type'
#an empty list has type NoneType
def get_type_list(node, vardict={}):
    if node.__class__ == ast.List:
        if node.elts == []:
            return 'NoneType'
        else:
            expected_type = get_type(node.elts[0], vardict)
            for i in range(1, len(node.elts)):
                if get_type(node.elts[i], vardict) != expected_type:
                    return None
            return 'list of ' + expected_type
    return None

# function types are of the form 'function: type1 -> type2 -> ... -> return_type'
# ambiguous parameter types are noted with '?id'
def get_type_call_helper(node, vardict={}):
    if node.__class__ == ast.Call:
        to_return = ''
        unknown_number = 0
        if node.func.__class__ == ast.Name:
            for parameter in node.args:
                ptype = get_type(parameter, vardict)
                if ptype is None:
                    ptype = f'?{unknown_number}'
                    unknown_number += 1
                if ptype == 'NoneType':
                    return None
                to_return = ptype if to_return == '' else to_return + ' -> ' + ptype
            return to_return + ' -> ' + f'?{unknown_number}'
        return None
    return None

def is_ambiguous(type_string : str):
    return type_string.startswith('?') and len(type_string) > 1

#an ambigous type is of the form '?id'
#current_ambiguous is the id to the current ambiguous type to generate
#if the two types are ambiguous, return the (current, '?current_ambiguous')
#if the two types are not ambiguous, return the (current, expected)
def resolve_ambiguous_conflict(current: str, expected: str, current_ambiguous: int):
    if is_ambiguous(current) and is_ambiguous(expected):
        return (True, current, f'?{current_ambiguous}')
    elif is_ambiguous(current) and not is_ambiguous(expected):
        return (False, current, expected)
    elif not is_ambiguous(current) and is_ambiguous(expected):
        return None, None, None
        # return (False, current, expected)
    else:
        raise Exception('Ambiguous types cannot be resolved' + 'Got ' + current + ' Expected ' + expected)


def get_type_call(node, vardict={}):
    if node.__class__ == ast.Call:
        type_of_call = get_type_call_helper(node, vardict)
        if type_of_call is None:
            return None
        l = type_of_call.split(' -> ')
        type_in_vardict = vardict[node.func.id].split(' -> ') if str(node.func.id) in vardict else None
        # print(vardict)
        #if type_in_vardict is None:
        #    return type_of_call
        if len(l) != len(type_in_vardict):
            return None
        cur = 0
        for i in range(len(l)):
            if l[i] != type_in_vardict[i]:
                if is_ambiguous(l[i]) or is_ambiguous(type_in_vardict[i]):
                    has_changed, change, new = resolve_ambiguous_conflict(l[i], type_in_vardict[i], cur)
                    if has_changed == None:
                        return None
                    if has_changed:
                        cur += 1
                    for j in range(i, len(l)):
                        l[j] = new if l[j] == change else l[j]
                    # for j in range(i, len(type_in_vardict)):
                    #     type_in_vardict[j] = new if type_in_vardict[j] == change else type_in_vardict[j]
                else:
                    return None
        # print(l[-1])
        return l[-1]
        # return ' -> '.join(l)
        # return type_of_call
    return None

#Returns the type of the tuple in the form '(type1, type2, ...)'
#Example : (5, 3) -> '(int, int)'
def get_type_tuple(node, vardict={}):
    if node.__class__ == ast.Tuple:
        if node.elts == []:
            return '()'
        else:
            result = '('
            for i in range(len(node.elts)):
                expected_type = get_type(node.elts[i], vardict)
                if expected_type is None:
                    return None
                result += expected_type
                if i != len(node.elts) - 1:
                    result += ', '
            return result + ')'
    return None

#deduces the type of a python expression by looking at the AST
#returns the python type of the expression
#returns None if the type cannot be deduced
def get_type(node, vardict={}):
    if isinstance(node, ast.Constant):
        if str(node.value) in BUILTIN_TOKENS:
            return BUILTIN_TOKENS[str(node.value)]
        return get_token_type(type(node.value))
    elif isinstance(node, ast.Name):
        return vardict[node.id] if node.id in vardict else None
    elif isinstance(node, ast.BinOp):
        return get_type_binop(node, vardict)
    elif isinstance(node, ast.UnaryOp):
        return get_type_unop(node, vardict)
    elif isinstance(node, ast.Call):
        return get_type_call(node, vardict)
    elif isinstance(node, ast.List):
        return get_type_list(node, vardict)
    elif isinstance(node, ast.Tuple):
        return get_type_tuple(node, vardict)

class wrapper:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

RED = "\033[31m"
GREEN = "\033[32m"
DEFAULT = "\033[39m"

def check_test(test_case :str, expected :str, env : dict, failed_number : wrapper, success_number : wrapper, failed_list):
    try:
        actual = get_type(ast.parse(test_case).body[0].value, env)
        if str(actual) == expected:
            success_number.value += 1
        else:
            failed_number.value += 1
            failed_list.append(f'{RED}[KO]{DEFAULT} {test_case} w. {env} -> got {actual} != {expected}')
    except Exception as e:
        failed_number.value += 1
        failed_list.append(f'{RED}[KO]{DEFAULT} {test_case} w. {env} -> {e}\n{__import__("traceback").format_exc()}')
    return failed_number, success_number, failed_list

def erase():
    print('\033[F\033[K', end='')

def test(cases :list, envs :list, expected :list):
    percentage = 0.
    failed_number = wrapper(0)
    success_number = wrapper(0)
    failed_list = []
    total = len(cases) * len(envs)
    len_expected = 0
    for i in expected:
        len_expected += len(i)
    if len_expected != total:
        print(f'{RED}[KO]{DEFAULT} The number of expected results is different from the number of tests : {len_expected} results vs. {total} tests')
        return
    print("")
    for i in range(len(cases)):
        for j in range(len(envs)):
            failed_number, success_number, failed_list = check_test(cases[i], expected[i][j], envs[j], failed_number, success_number, failed_list)
            percentage = (success_number.value / (success_number.value + failed_number.value)) * 100
        erase()
        print(f'[Success. {GREEN}{success_number.value}{DEFAULT}/{total}] [Failed. {RED if failed_number.value != 0 else ""}{failed_number.value}{DEFAULT if failed_number.value != 0 else ""}/{total}]')
    for i in failed_list:
        print(i)

if __name__=='__main__':
    test_cases = [
        '1 + 2',
        '1 - 2',
        '1 * 2',
        '1 / 2',
        '1 ** 2',
        '1',
        '1.0',
        '"hello"',
        'True',
        'False',
        'None',
        '1 + 2 * 3',
        '1 + 2 * 3 - 4',
        '1 + 2 * 3 - 4 / 5',
        'a',
        'inexistant',
        'a + inexistant',
        'a + 1',
        'a + 1.',
        'a + None',
        'a < 2',
        'a < b',
        'a == b',
        'pika(1, 2, a)',
        'pika(1, 2, a) + 1.',
        'pika(1, 2, 3)',
        '[]',
        '[1, 2, 3]',
        '[1, 2, 3, 4, 5.0]',
        '(1, 2, 3)',
        '(1, 2, 3, 4, 5.0)',
    ]

    envs = [
        {'a': 'int'},
        {'a': 'float'},
        {'a': 'float', 'pika': 'int -> int -> float -> float'},
    ]

    expected = [
        ['int', 'int', 'int'],
        ['int', 'int', 'int'],
        ['int', 'int', 'int'],
        ['int', 'int', 'int'],
        ['None', 'None', 'None'],
        ['int', 'int', 'int'],
        ['float', 'float', 'float'],
        ['str', 'str', 'str'],
        ['bool', 'bool', 'bool'],
        ['bool', 'bool', 'bool'],
        ['NoneType', 'NoneType', 'NoneType'],
        ['int', 'int', 'int'],
        ['int', 'int', 'int'],
        ['int', 'int', 'int'],
        ['int', 'float', 'float'],
        ['None', 'None', 'None'],
        ['None', 'None', 'None'],
        ['int', 'None', 'None'],
        ['None', 'float', 'float'],
        ['None', 'None', 'None'],
        ['bool', 'None', 'None'],
        ['None', 'None', 'None'],
        ['None', 'None', 'None'],
        ['int -> int -> int -> float', 'float', 'float'],
        ['int -> int -> int -> float', 'float', 'float'],
        ['None', 'None', 'None'],
        ['NoneType', 'NoneType', 'NoneType'],
        ['list of int', 'list of int', 'list of int'],
        ['None', 'None', 'None'],
        ['(int, int, int)', '(int, int, int)', '(int, int, int)'],
        ['(int, int, int, int, float)', '(int, int, int, int, float)', '(int, int, int, int, float)']
    ]

    test(test_cases, envs, expected)

    #for test in test_cases:
    #    print('New test : ' + test)
    #    # print(get_type(ast.parse(test).body[0].value))
    #    # print(get_type(ast.parse(test).body[0].value, {'a': 'int'}))
    #    # print(get_type(ast.parse(test).body[0].value, {'a': 'float'}))
    #    print(get_type(ast.parse(test).body[0].value, {'a': 'float', 'pika': 'int -> int -> float -> float'}))
    #    # print(get_type(ast.parse(test).body[0].value, {'a': 'float'}))

