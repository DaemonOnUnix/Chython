import ast
import compiler.id

class ContextElement:
    def __init__(self, id, type=None):
        self.id = id
        self.type = type
    
    def def_type(_type):
        self.type = _type
    
    def __repr__(self):
        return f'({self.id}, {self.type})'
    
    def typeof(self, ctx):
        return self.type

class Scope:
    def __init__(self, name):
        self.elements = []
        self.name = name
    
    def add_element(self, element):
        self.elements.append(element)
    
    def get_element(self, id):
        for element in self.elements:
            if element.id == id:
                return element
        return None
    
    def __repr__(self):
        return f'Scope({self.name}, {self.elements})'

class Context:
    def __init__(self):
        self.scopes = []
        self.current_scope = Scope('.')
        self.scopes.append(self.current_scope)
    
    def push_scope(self, name):
        self.current_scope = Scope(name)
        self.scopes.append(self.current_scope)
    
    def pop_scope(self):
        self.scopes.pop()
        self.current_scope = self.scopes[-1]
    
    def add_element(self, element):
        self.current_scope.add_element(element)
    
    def get(self, id):
        if id.__class__ != compiler.id.Id:
            raise TypeError(f"Expected compiler.id.Id, got {id.__class__}")
        for scope in reversed(self.scopes):
            element = scope.get_element(id)
            if element:
                return element
        return None
    
    def __repr__(self):
        return f'Context({self.scopes})'

