import dis

def similarity(name1, name2):
    return 0.95

class FuzzyGlobals(dict):
    def __init__(self, fallback_globals):
        self.fallback = fallback_globals
        self.variables = {}

    def __getitem__(self, key):
        for k, v in self.variables.items():
            if similarity(key, k) >= 0.9:
                print("Matched %r to %r" % (key, k))
                return v

        for k, v in self.fallback.items():
            if similarity(key, k) >= 0.9:
                print("Matched %r to %r" % (key, k))
                return v

        for k, v in self.fallback["__builtins__"].items():
            if similarity(key, k) >= 0.9:
                print("Matched %r to %r" % (key, k))
                return v

        raise NameError(key)

    def __setitem__(self, key, value):
        assert 0, (key, value)

def fuzzyNames(f):
    code = f.__code__
    codestr = code.co_code

    new_codestr = []

    bytecode_map = {
        "LOAD_FAST": "LOAD_NAME",
        "STORE_FAST": "STORE_NAME",
    }
    for instr in dis.Bytecode(code):
        opname = instr.opname
        opcode = dis.opmap[bytecode_map.get(opname, opname)]
        new_codestr.append(opcode.to_bytes(1, "little"))
        new_codestr.append((instr.arg or 0).to_bytes(1, "little"))

    new_code = code.replace(co_code=b''.join(new_codestr))
    # new_code = code

    return type(f)(new_code, FuzzyGlobals(f.__globals__))

if __name__ == "__main__":
    @fuzzyNames
    def test():
        strength = 1.0
        return power

    dis.dis(test)

    print(test())
