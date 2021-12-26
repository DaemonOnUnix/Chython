import ast as py_ast

def py_type_to_c_type(py_type):
    if py_type == 'int':
        return 'int'
    elif py_type == 'float':
        return 'float'
    elif py_type == 'str':
        return 'char*'
    elif py_type == 'bool':
        return 'bool'
    elif py_type == 'NoneType':
        return 'void'
    elif py_type == 'list':
        return 'void*'
    elif py_type == "u16":
        return "uint16_t"
    elif py_type == "u32":
        return "uint32_t"
    elif py_type == "u64":
        return "uint64_t"
    raise Exception('Unknown type: ' + py_type)
