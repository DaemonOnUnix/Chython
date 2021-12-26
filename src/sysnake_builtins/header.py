builtin_functions = ''
builtin_header = '''
#include <stddef.h>
#include <stdint.h>
'''
def add_builtin_function(function : str):
    global builtin_functions
    builtin_functions += function + '\n'

def get_builtin_header():
    return builtin_header

def get_builtin_functions():
    return builtin_functions