class Requirement:
    def __init__(self, name, version=None):
        self.name = name
        self.version = version
    
    def __repr__(self):
        return f'Requirement({self.name}, {self.version})'
    
    def serialize(self):
        return f'{self.name}=={self.version}' if self.version else self.name

class Requirements:
    def __init__(self, string):
        # Same form as pip requirements.txt form
        self.list = []
        for line in string.split('\n'):
            if line and not line.startswith('#'):
                self.list.append(Requirement(*line.split('==')))

    def __repr__(self):
        return f'Requirements({self.list})'
    
    def serialize(self):
        return '\n'.join([req.serialize() for req in self.list]) + '\n'
    
    def add_unique_requirement(self, line):
        req = Requirement(*line.split('=='))
        if req not in self.list:
            self.list.append(req)
