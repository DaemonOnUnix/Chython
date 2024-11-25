import ast

class ImportUnit:
    def __init__(self, name, asname = None):
        if not asname:
            asname = name
        self.name = name
        self.asname = asname
    
    def __repr__(self):
        return f'ImportUnit({self.name}, {self.asname})'

class Import:
    def __init__(self, astnode):
        if astnode.__class__ != ast.Import:
            raise TypeError("Expected Import node, got " + astnode.__class__.__name__)
        self.names = []
        for alias in astnode.names:
            if alias.asname:
                self.names.append(ImportUnit(alias.name, alias.asname))
            else:
                self.names.append(ImportUnit(alias.name))

    def __repr__(self):
        return f'Import({self.names})'        