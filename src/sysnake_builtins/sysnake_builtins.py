import sysnake_builtins.header as header

state = {
    'has_written_mem_64' : False,
    'has_read_mem_64' : False,
    'has_written_mem_32' : False,
    'has_read_mem_32' : False,
    'has_written_mem_16' : False,
    'has_read_mem_16' : False,
    'has_written_mem_8' : False,
    'has_read_mem_8' : False
}


builtins_c_code = {
    'write_mem_64' :
    '''
    void write_mem_64(uint64_t address, uint64_t value) {
        volatile uint64_t* mem_ptr = (uint64_t*)address;
        *mem_ptr = value;
    }
    ''',
    'read_mem_64' :
    '''
    uint64_t read_mem_64(uint64_t address) {
        volatile uint64_t* mem_ptr = (uint64_t*)address;
        return *mem_ptr;
    }
    ''',
    'write_mem_32' :
    '''
    void write_mem_32(uint64_t address, uint32_t value) {
        volatile uint32_t* mem_ptr = (uint32_t*)address;
        *mem_ptr = value;
    }
    ''',
    'read_mem_32' :
    '''
    uint32_t read_mem_32(uint64_t address) {
        volatile uint32_t* mem_ptr = (uint32_t*)address;
        return *mem_ptr;
    }
    ''',
    'write_mem_16' :
    '''
    void write_mem_16(uint64_t address, uint16_t value) {
        volatile uint16_t* mem_ptr = (uint16_t*)address;
        *mem_ptr = value;
    }
    ''',
    'read_mem_16' :
    '''
    uint16_t read_mem_16(uint64_t address) {
        volatile uint16_t* mem_ptr = (uint16_t*)address;
        return *mem_ptr;
    }
    ''',
    'write_mem_8' :
    '''
    void write_mem_8(uint64_t address, uint8_t value) {
        volatile uint8_t* mem_ptr = (uint8_t*)address;
        *mem_ptr = value;
    }
    ''',
    'read_mem_8' :
    '''
    uint8_t read_mem_8(uint64_t address) {
        volatile uint8_t* mem_ptr = (uint8_t*)address;
        return *mem_ptr;
    }
    '''
}

def builtin_write_mem_64() -> str:
    header.add_builtin_function(builtins_c_code['write_mem_64'])
    return f'write_mem_64'

def builtin_read_mem_64() -> str:
    header.add_builtin_function(builtins_c_code['read_mem_64'])

def builtin_write_mem_32() -> str:
    header.add_builtin_function(builtins_c_code['write_mem_32'])

def builtin_read_mem_32() -> str:
    header.add_builtin_function(builtins_c_code['read_mem_32'])

def builtin_write_mem_16() -> str:
    header.add_builtin_function(builtins_c_code['write_mem_16'])

def builtin_read_mem_16() -> str:
    header.add_builtin_function(builtins_c_code['read_mem_16'])

def builtin_write_mem_8() -> str:
    header.add_builtin_function(builtins_c_code['write_mem_8'])

def builtin_read_mem_8() -> str:
    header.add_builtin_function(builtins_c_code['read_mem_8'])

builtins = {
    'write_mem_64' : (2, [int, int], builtin_write_mem_64),
    'read_mem_64' : (1, [int], builtin_read_mem_64),
    'write_mem_32' : (2, [int, int], builtin_write_mem_32),
    'read_mem_32' : (1, [int], builtin_read_mem_32),
    'write_mem_16' : (2, [int, int], builtin_write_mem_16),
    'read_mem_16' : (1, [int], builtin_read_mem_16),
    'write_mem_8' : (2, [int, int], builtin_write_mem_8),
    'read_mem_8' : (1, [int], builtin_read_mem_8)
}