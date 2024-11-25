#!/usr/bin/python3
import ast
import sys
import os
import re
import compiler.translation_unit
import compiler.typeof

def get_ast_tree(file_path):
    with open(file_path, 'r') as f:
        return ast.parse(f.read())

def write_to_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)

def main():
    if len(sys.argv) < 2:
        print('Usage: python3 sys_snake.py <path_to_file>')
        return

    file_path = sys.argv[1]
    ast_tree = get_ast_tree(file_path)
    # print(ast.dump(ast_tree))
    # print(ast.dump(ast.parse("a = b'salut'")))
    # print(ast.dump(ast.parse("b'salut'").body[0]))
    # print(compiler.typeof.typeof(ast.parse("a = b'salut'").body[0].value))
    compiler.translation_unit.TranslationUnit(sys.argv[1][:sys.argv[1].find('.')], ast_tree)
    # sys_snake_code = codegen.codegen(ast_tree, True)
    # write_to_file(file_path.replace('.py', '.py.c') , header.get_builtin_header() + '\n' + header.get_builtin_functions() + '\n' + sys_snake_code)

if __name__ == '__main__':
    main()