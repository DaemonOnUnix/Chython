import ast

class TypeUnit:
    Corr = {
        'u64': 'uint64_t %s',
        'u32': 'uint32_t %s',
        'u16': 'uint16_t %s',
        'u8': 'uint8_t %s',

        'i64': 'int64_t %s',
        'i32': 'int32_t %s',
        'i16': 'int16_t %s',
        'i8': 'int8_t %s',

        'f32': 'float %s',
        'f64': 'double %s',
        
        'char': 'char %s',
        'str': 'char *%s',
        'bytes': 'uint8_t %s[]',

        'unit': 'void'
    }

    Primitives = [
        'u64', 'u32', 'u16', 'u8',
        'i64', 'i32', 'i16', 'i8',
        'f32', 'f64', 'char', 'str',
        'bytes'
    ]

    Integrals = [
        'u64', 'u32', 'u16', 'u8',
        'i64', 'i32', 'i16', 'i8',
        'char'
    ]

    Props = {
        'Integral': Integrals,
        'Primitive': Primitives,
    }

    def __init__(self, name):
        self.name = name
        if name in TypeUnit.Corr:
            self.c = TypeUnit.Corr[name]
        else:
            # To resolve later
            self.c = None
        self.props = []
        for k, v in self.Props.items():
            if name in v:
                self.props.append(k)
    
    def instanciate(self, var_name):
        return self.c % var_name if self.c else None 

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, o):
        return self.name == o.name or ('Integral' in self.props and self.props == o.props)
    
    def __ne__(self, o):
        return not self == o
    
    @staticmethod
    def constant_type(atom):
        if type(atom.value) == int:
            return AtomicType('i64')
        if type(atom.value) == float:
            return AtomicType('f64')
        if type(atom.value) == str:
            return AtomicType('str')
        if type(atom.value) == bytes:
            return AtomicType('bytes')
    
class Type:
    def __init__(self, types_str):
        # Avoid confusion by passing an str
        if type(types_str) == str:
            types_str = [types_str]
        self.elems = []
        for t in types_str:
            self.elems.append(TypeUnit(t))
    
    def __str__(self):
        return '->'.join([str(x) for x in self.elems])
    
    def is_compound(self):
        return len(self.elems) > 1
    
    def is_num(self):
        return not self.is_compound() and 'Integral' in self.elems[0].props
    
    def __len__(self):
        return len(self.elems)

    def __eq__(self, o):
        if len(self) != len(o):
            return False
        for i in range(len(self)):
            if self.elems[i] != o.elems[i]:
                return False
        return True
    
    def __ne__(self, o):
        return not (self == o)

class AtomicType(Type):
    def __init__(self, type_str):
        if not type_str in TypeUnit.Primitives:
            raise ValueError(f"Type {type_str} is not a primitive type")
        super().__init__([type_str])

UNIT = Type(['unit'])