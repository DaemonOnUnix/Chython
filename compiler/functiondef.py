import ast
import compiler.id
import compiler.parser
import compiler.type_system
import compiler.context

class FunArg:
    def __init__(self, name, _type):
        self.name = name
        self.type = _type
    
    def __repr__(self):
        return f'FunArg({self.name}, {self.type})'
    
    def get_type(self, ctx):
        return self.type

    def typeof(self, ctx):
        return compiler.type_system.Type([self.type]) if self.type else None

class Return:
    def __init__(self, ast_node):
        if ast_node.__class__ != ast.Return:
            raise TypeError(f"Expected Return node, got {ast_node.__class__.__name__}")
        self.value = compiler.parser.parse(ast_node.value)
    
    def __repr__(self):
        return f'Return({self.value})'
    
    def typeof(self, ctx):
        rt = self.value.typeof(ctx)
        expected = ctx.get_type_to_return()
        if rt != expected:
            raise TypeError(f"Expected to return {ctx.get_type_to_return()}, returns {rt}")
        return compiler.type_system.UNIT

class Pass:
    def __init__(self, ast_node):
        if ast_node.__class__ != ast.Pass:
            raise TypeError(f"Expected Pass node, got {ast_node.__class__.__name__}")
    
    def __repr__(self):
        return 'Pass()'
    
    def typeof(self, ctx):
        return compiler.type_system.UNIT

class Function:
    def __init__(self, astNode):
        print(ast.dump(astNode))
        if astNode.__class__ != ast.FunctionDef:
            raise TypeError(f"Expected FunctionDef node, got {astNode.__class__.__name__}")
        self.name = compiler.id.Id.from_str(astNode.name)
        self.args = [FunArg(arg.arg, arg.annotation.id if arg.annotation else None) for arg in astNode.args.args]
        self.body = [compiler.parser.parse(x) for x in astNode.body]
        if not astNode.returns:
            raise TypeError(f"Function {self.name} has no return type hint")
        self.return_type = astNode.returns.id
    
    def __repr__(self):
        return f'Function({self.name}, {self.args}, {self.body})'
    
    def typeof(self, ctx):
        # Create new context, push all the parameters with type hints in it as variables
        # Check that everyone in bode has UNIT type
        ctx.push_scope(self.name)

        ctx.current_scope.set_return_type(compiler.type_system.Type([self.return_type]))
        for arg in self.args:
            new_element = compiler.id.Id.from_str(arg.name)
            # If no type hint panic
            if not arg.typeof(ctx):
                raise TypeError(f"No type hint for argument {arg.name} in function {self.name.name[0]}")
            ctx.add_element(compiler.context.ContextElement(new_element, arg.typeof(ctx)))
        

        for stmt in self.body:
            print(stmt)
            if stmt.typeof(ctx) != compiler.type_system.UNIT:
                raise TypeError(f"Statement {stmt} in function {self.name} has non-UNIT type")
        
        print(ctx.current_scope)
        ctx.pop_scope()
        # Add the function in the scope

        return compiler.type_system.UNIT
