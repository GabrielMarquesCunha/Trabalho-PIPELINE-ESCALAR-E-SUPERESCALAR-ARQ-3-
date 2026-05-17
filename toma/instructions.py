
class Instruction:
    def __init__(self, op, dest, vj, vk, label):
        self.op = op
        self.dest = dest
        self.vj = vj
        self.vk = vk
        self.label = label

    def toString(self):
        if self.dest == '':
            return ''
        
        if self.op == "lw" or self.op == "sw":
            return "{} {}, {}".format(self.op, self.dest, self.vj)

        if self.op == "bne":
            return "{} {}, {}, {}".format(self.op, self.vj, self.vk, self.label)

        return "{} {}, {}, {}".format(self.op, self.dest, self.vj, self.vk)
    # -- T1 -- 
instructions_t1  = [
    Instruction("ld", "f6", "34(r2)", "", ""),
    Instruction("ld", "f2", "45(r3)", "", ""),
    Instruction("multd", "f0", "f2", "f4", ""),
    Instruction("subd", "f8", "f6", "f2", ""),
    Instruction("divd", "f10", "f0", "f6", ""),
    Instruction("addd", "f6", "f8", "f2", "")
]

#-- T2 -- 

instructions_t2 = [
    Instruction("divd", "f0", "f2", "f4", ""),
    Instruction("multd", "f6", "f0", "f8", ""),
    Instruction("addd", "f2", "f6", "f4", ""),
    Instruction("multd", "f8", "f2", "f6", ""),
    Instruction("subd", "f0", "f8", "f6", ""),
    Instruction("addd", "f4", "f0", "f2", "")
]