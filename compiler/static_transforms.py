import ast

# Modelize before parsing AST trasnformation

# For instance Attribute(value=Name(id='self', ctx=Load()), attr='truc', ctx=Store())
# Becoming Name(id='self->truc', ctx=Store())
class StaticTransform(ast.NodeTransformer):
    def visit_Attribute(self, node):
        self.generic_visit(node)
        
        if isinstance(node.value, ast.Name) and isinstance(node.ctx, ast.Store):
            new_node = ast.Name(
                id=f"{node.value.id}->{node.attr}",
                ctx=node.ctx
            )
            return ast.copy_location(new_node, node)
        return node

# Transforme UnaryOp (- Constant to Constant)
class StaticTransformUnaryOp(ast.NodeTransformer):
    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        
        if isinstance(node.op, ast.USub) and isinstance(node.operand, ast.Constant):
            new_node = ast.Constant(
                value=-node.operand.value
            )
            return ast.copy_location(new_node, node)
        if isinstance(node.op, ast.UAdd) and isinstance(node.operand, ast.Constant):
            new_node = ast.Constant(
                value = node.operand.value
            )
            return ast.copy_location(new_node, node)

TRANSFORM_LIST = [
    StaticTransform,
    StaticTransformUnaryOp
]

def apply_transfos(astNode):
    for transform in TRANSFORM_LIST:
        astNode = transform().visit(astNode)
    return astNode