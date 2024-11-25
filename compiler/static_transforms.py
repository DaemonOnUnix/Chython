import ast

# Modelize before parsing AST trasnformation
# For instance Attribute(value=Name(id='self', ctx=Load()), attr='truc', ctx=Store())
# Becoming Name(id='self->truc', ctx=Store())

class StaticTransform(ast.NodeTransformer):
    def visit_Attribute(self, node):
        # Visit the child nodes first
        self.generic_visit(node)
        
        # Check if the attribute is of the desired pattern
        if isinstance(node.value, ast.Name) and isinstance(node.ctx, ast.Store):
            # Transform Attribute to Name with the desired format
            new_node = ast.Name(
                id=f"{node.value.id}->{node.attr}",
                ctx=node.ctx
            )
            return ast.copy_location(new_node, node)
        
        return node  # If no transformation, return the original node

TRANSFORM_LIST = [
    StaticTransform
]

def apply_transfos(astNode):
    for transform in TRANSFORM_LIST:
        astNode = transform().visit(astNode)
    return astNode