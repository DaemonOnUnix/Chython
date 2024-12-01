import urllib.request

class xFile:
    def __init__(self, path):
        self.path = path
        if path.startswith('http'):
            self.f = urllib.request.urlopen(path)
            self.mode = 'r'       
        else:
            self.f = open(path, 'r')
            self.mode = 'l'

    def read(self):
        if self.mode == 'r':
            return self.f.read().decode('utf-8')
        else:
            return self.f.read()
    
    def write(self, content):
        if self.mode == 'r':
            raise Exception('Cannot write to an HTTP file')
        self.f.write(content)
    
    def readlines(self):
        if self.mode == 'r':
            r = self.f.read().decode('utf-8').split('\n')
            self.f.close()
            self.f = urllib.request.urlopen(path)
        else:
            return self.f.readlines()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.f.close()