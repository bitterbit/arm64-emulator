from __future__ import print_function
import frontmatter

from unicorn import *
from unicorn.arm64_const import *
from keystone import *

def get_register_for_key(key):
    return KEY_TO_REG[key]
def get_key_for_reg(reg):
    for key, r in KEY_TO_REG.items():
        if r == reg:
            return key

def get_all_registers():
    return KEY_TO_REG.values()

KEY_TO_REG = {
    "X0": UC_ARM64_REG_X0,
    "X1": UC_ARM64_REG_X1,
    "X2": UC_ARM64_REG_X2,
    "X3": UC_ARM64_REG_X3,
    "X4": UC_ARM64_REG_X4,
    "X5": UC_ARM64_REG_X5,
    "X6": UC_ARM64_REG_X6,
    "X7": UC_ARM64_REG_X7,
    "X8": UC_ARM64_REG_X8,
    "X9": UC_ARM64_REG_X9,
    "X10": UC_ARM64_REG_X10,
    "X11": UC_ARM64_REG_X11,
    "X12": UC_ARM64_REG_X12,
    "X13": UC_ARM64_REG_X13,
    "X14": UC_ARM64_REG_X14,
    "X15": UC_ARM64_REG_X15,
    "X16": UC_ARM64_REG_X16,
    "X17": UC_ARM64_REG_X17,
    "X18": UC_ARM64_REG_X18,
    "X19": UC_ARM64_REG_X19,
    "X20": UC_ARM64_REG_X20,
    "X21": UC_ARM64_REG_X21,
    "X22": UC_ARM64_REG_X22,
    "X23": UC_ARM64_REG_X23,
    "X24": UC_ARM64_REG_X24,
    "X25": UC_ARM64_REG_X25,
    "X26": UC_ARM64_REG_X26,
    "X27": UC_ARM64_REG_X27,
    "X28": UC_ARM64_REG_X28,
}

def hook_block(uc, address, size, user_data):
    print(">>> Tracing basic block at 0x%x, block size = 0x%x" %(address, size))

def hook_code(uc, address, size, user_data):
    print(">>> Tracing instruction at 0x%x, instruction size = 0x%x" %(address, size))



# memory address where emulation starts
ADDRESS    = 0x10000

class Emulator(object):
    def __init__(self):
        self.mu = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
        self.ks = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN) 
        
        self.registers = {} 
        self.asm = "";

    def load_instructions(self, path):
        data = frontmatter.load(path)
        for k,v in data.to_dict().items():
            if k == "content":
                self._set_asm(v)
            else:
                self.registers[k] = v

    def _set_asm(self, asm):
        self.asm = asm
        encoding, count = self.ks.asm(asm)
        self.code = b''.join([chr(x) for x in encoding])
        self.code_len = len(self.code)

    def print_state(self):
        self.print_registers()

    def print_registers(self):
        CELL_WIDTH = 10
        register_rows = [(get_key_for_reg(x), self.mu.reg_read(x)) for x in sorted(get_all_registers())]
        register_rows.append(("SP",self.mu.reg_read(UC_ARM64_REG_SP))) 
        register_rows.append(("PC",self.mu.reg_read(UC_ARM64_REG_PC))) 
        s = ""
        for i in range(len(register_rows)):
            name, val = register_rows[i]
            cell = str(name) + ": " + hex(val)[:-1] 
            cell += (CELL_WIDTH - len(cell)) * ' '
            s += cell + '\t'
            if i % 4  == 3:
                s += '\n'
        print (s)


    def start(self):
        self.mu.mem_map(ADDRESS, 2 * 1024 * 1024)
        self.mu.mem_write(ADDRESS, self.code)
        [self.mu.reg_write(reg, 0) for reg in get_all_registers()] # TODO: is this needed? 
        [self.mu.reg_write(get_register_for_key(reg), val) for reg,val in self.registers.items()]
        
        self.mu.mem_map(ADDRESS + 0x200000, 2 * 1024 * 1024)
        self.mu.reg_write(UC_ARM64_REG_SP, ADDRESS + 0x200000)

        self.mu.hook_add(UC_HOOK_BLOCK, hook_block)
        self.mu.hook_add(UC_HOOK_CODE, hook_code, begin=ADDRESS, end=ADDRESS)
        self.mu.emu_start(ADDRESS, ADDRESS + self.code_len)

        print (">>> Emulation done.")
        self.print_state()


def main():
    e = Emulator()
    e.load_instructions('test.inst')
    print ("asm", e.asm)
    print ("registers", e.registers)
    e.start()

if __name__ == '__main__':
    main()
