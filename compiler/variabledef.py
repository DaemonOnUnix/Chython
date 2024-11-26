import ast
import compiler.type_system
import compiler.typeof
import compiler.parser
import compiler.id

class Variable:
    def __init__(self, name, value, _type = None):
        #self.name = [compiler.id.Id.from_str(x) for x in name.id.split('->')]
        self.name = compiler.id.Id(name)
        self.value = compiler.parser.parse(value)
        self._type = _type

    def __repr__(self):
        return f"Variable({self.name}, {self.value}, {self._type})"
    
    def typeof(self, ctx):
        in_ctx = ctx.get(self.name)
        type_announced = compiler.type_system.Type([self._type]) if self._type else None
        
        if in_ctx and type_announced:
            raise Exception(f'Redefinition of {self.name} with type {type_announced}, Previously defined as {in_ctx.typeof(ctx)}')
        
        type_value = self.value.typeof(ctx)
        if type_announced and type_value != type_announced:
            raise Exception(f"Type mismatch for {self.name}, expected {type_announced}, got {type_value}")

        type_to_add = type_announced if type_announced else type_value
        ctx.add_element(compiler.context.ContextElement(self.name, type_to_add))

        return type_value

# XXX Modelize a better way to represent packed data, maybe has to do with type system
class VariableInstanciation:
    def __init__(self, astNode):
        if astNode.__class__ != ast.Assign and astNode.__class__ != ast.AnnAssign:
            raise TypeError(f"Expected ast.Assign or ast.AnnAssign, got {astNode.__class__}")
        type_hint, ast_lhs, ast_rhs = '', None, None
        if astNode.__class__ == ast.AnnAssign:
            type_hint = astNode.annotation.id
            ast_lhs = astNode.target
            ast_rhs = astNode.value
            if ast_lhs.__class__ != ast.Name:
                raise TypeError(f"Expected ast.Name, got {ast_lhs.__class__}")
            self.vars = [Variable(ast_lhs, ast_rhs, type_hint)]
            return
        ast_lhs = astNode.targets
        ast_rhs = astNode.value
        self.vars = []
        lhs = []
        # Consider multi assignement
        if ast_rhs.__class__ == ast.Tuple:
            current_rhs = 0
            for target in ast_lhs:
                if target.__class__ == ast.Name:
                    self.vars.append(Variable(target, ast_rhs.elts[current_rhs]))
                    current_rhs += 1
                elif target.__class__ == ast.Tuple:
                    for elt in target.elts:
                        if elt.__class__ != ast.Name:
                            raise TypeError(f"Expected ast.Name, got {ast_lhs.__class__}")
                        self.vars.append(Variable(elt, ast_rhs.elts[current_rhs]))
                        current_rhs += 1
            return
        # Tuple deconstruction
        elif ast_rhs.__class__ == ast.Name and ast_lhs.__class__ == ast.Tuple:
            raise Exception('Tuple deconstruction not implemented')
        # XXX Not strict enough
        elif ast_rhs.__class__ == ast.Name:
            self.vars.append(Variable(ast_lhs[0], ast_rhs))
        elif ast_rhs.__class__ == ast.Constant:
            self.vars.append(Variable(ast_lhs[0], ast_rhs))
        else:
            # Trust me I'm an engineer
            raise TypeError(f"Expected ast.Name or ast.Constant, got {ast_rhs.__class__}")
    
    def get_vars(self):
        return self.vars
    
    def __repr__(self):
        return f"VariableInstanciation({self.vars})"
    
    def typeof(self, ctx):
        for var in self.vars:
            var.typeof(ctx)
        return compiler.type_system.UNIT
