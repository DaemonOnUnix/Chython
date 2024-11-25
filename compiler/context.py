import ast

class ContextElement:
    def __init__(self, id):
        self.id = id
        self.type = None
    
    def def_type(_type):
        self.type = _type

class Scope:
    def __init__(self):
        self.elements = []
    
    def add_element(self, element):
        self.elements.append(element)
    
    def get_element(self, id):
        for element in self.elements:
            if element.id == id:
                return element
        return None

class Context:
    def __init__(self):
        self.scopes = []
        self.current_scope = Scope()
        self.scopes.append(self.current_scope)
    
    def push_scope(self):
        self.current_scope = Scope()
        self.scopes.append(self.current_scope)
    
    def pop_scope(self):
        self.scopes.pop()
        self.current_scope = self.scopes[-1]
    
    def add_element(self, element):
        self.current_scope.add_element(element)
    
