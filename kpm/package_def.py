import toml

class PkgInfo:
    def __init__(self, name, pkg_type, version, description, author, license):
        self.name = name
        self.type = pkg_type
        self.version = version
        self.description = description
        self.author = author
        self.license = license

    def __repr__(self):
        return f'PkgInfo(name={self.name!r}, version={self.version!r}, description={self.description!r}, author={self.author!r}, license={self.license!r})'

    def __str__(self):
        return f'Package {self.name} - version {self.version}'

    def __eq__(self, other):
        return self.name == other.name and self.version == other.version

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name) ^ hash(self.version)

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'version': self.version,
            'description': self.description,
            'author': self.author,
            'license': self.license,
        }

    @classmethod
    def from_dict(cls, data):
        try:
            return cls(data['name'], data['type'], data['version'], data['description'], data['author'], data['license'])
        except Exception:
            print(f'Corrupted Project data: {data}')

    @classmethod
    def from_toml(cls, json_str):
        return cls.from_dict(toml.loads(json_str))

    def to_toml(self):
        return toml.dumps(self.to_dict())
