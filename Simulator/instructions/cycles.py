from instructions.helper import *


########################################################### Fetch #############################################################


def fetch_instruction(reg, step, name, inc=False):
    print_registers(f"{step}. Fetching instruction {name}", 50, reg)
    cycle()
    
    if inc: inc_pc(reg)

def fetch_zero(reg, address, step, mode, plus="", inc=False):
    print_registers(f"{step}. Fetching zero page address", 50, reg)
    cycle()

    reg[mode] = address
    if plus == "":
        reg[mode] = address
    elif plus == "x":
        reg[mode] = add(address, reg["x"])
    elif plus == "y":
        reg[mode] = add(address, reg["y"])
    if inc: inc_pc(reg)

def fetch_absolute_low(reg, address, step, mode, plus="", inc=False):
    print_registers(f"{step}. Fetching absolute page low address", 50, reg)
    cycle()
    
    if plus == "":
        reg[mode] = address
    elif plus == "x":
        reg[mode] = add(address, reg["x"])
        reg["carry"] = check_carry(address + reg["x"])
    elif plus == "y":
        reg[mode] = add(address, reg["y"])
        reg["carry"] = check_carry(address + reg["y"])
    if inc: inc_pc(reg)

def fetch_absolute_high(reg, address, step, mode, plus="", inc=False):
    print_registers(f"{step}. Fetching absolute page high address", 50, reg)
    cycle()

    if plus == "":
        reg[mode] = address
    elif (plus == "x" or plus == "y") and reg["carry"] == 1:
        reg[mode] = add(address, reg["carry"])
    if inc: inc_pc(reg)


########################################################### Execute ###########################################################


def adc_execute(reg, operand, step, inc=False):
    print_registers(f"{step}. Executing ADC", 50, reg)
    cycle()

    a = reg["a"]
    b = operand
    c = get_carry(reg)
    result = (a + b + c)
    reg["a"] = result & 0b11111111
    set_negative(reg, result)
    set_overflow(reg, a, b, c)
    set_zero(reg, result)
    set_carry(reg, result)
    if inc: inc_pc(reg)

def and_execute(reg, operand, step, inc=False):
    print_registers(f"{step}. Executing AND", 50, reg)
    cycle()

    a = reg["a"]
    b = operand
    result = a & b
    reg["a"] = result
    set_negative(reg, result)
    set_zero(reg, result)
    if inc: inc_pc(reg)

def asl_execute(reg, operand, step, mode):
    print_registers(f"{step}. Executing ASL", 50, reg)
    cycle()

    result = operand << 1
    reg[mode] = result & 0b11111111
    set_negative(reg, result)
    set_zero(reg, result)
    set_carry(reg, result)

def bit_execute(reg, operand, step, inc=False):
    print_registers(f"{step}. Executing BIT", 50, reg)
    cycle()

    a = reg["a"]
    b = operand
    result = a & b
    set_negative(reg, result)
    set_overflow(reg, result, 0, 0)
    set_zero(reg, result)
    if inc: inc_pc(reg)

def branch_check(reg, memory, step, check, inc=False):
    print_registers(f"{step}. Checking branch", 50, reg)
    cycle()

    if check == 1: 
        reg["branch"] = 1
        reg["result"] = memory[get_pc(reg)]
    else: 
        reg["branch"] = 0
    if inc: inc_pc(reg)

def branch_execute(reg, step):
    if reg["branch"] == 0:
        return
    print_registers(f"{step}. Branching", 50, reg)
    cycle()

    reg["pcl"] = add(reg["pcl"], reg["result"])

def compare_execute(reg, operand, step, mode, inc=False):
    print_registers(f"{step}. Executing compare", 50, reg)
    cycle()

    a = reg[mode]
    b = operand
    result = a + (~b & 0b11111111) + 1
    set_negative(reg, result)
    set_zero(reg, result)
    set_carry(reg, result)
    if inc: inc_pc(reg)

def decrement_execute(reg, operand, step, mode):
    print_registers(f"{step}. Executing decrement", 50, reg)
    cycle()

    result = operand + (0b11111111)
    reg[mode] = result & 0b11111111
    set_negative(reg, result)
    set_zero(reg, result)

def eor_execute(reg, operand, step, inc=False):
    print_registers(f"{step}. Executing EOR", 50, reg)
    cycle()

    a = reg["a"]
    b = operand
    result = a ^ b
    reg["a"] = result
    set_negative(reg, result)
    set_zero(reg, result)
    if inc: inc_pc(reg)

def flags_clear(reg, flags, step):
    print_registers(f"{step}. Clearing flags", 50, reg)
    cycle()

    reg["flags"] &= ~flags

def flags_set(reg, flags, step):
    print_registers(f"{step}. Setting flags", 50, reg)
    cycle()

    reg["flags"] |= flags

def increment_execute(reg, operand, step, mode):
    print_registers(f"{step}. Executing increment", 50, reg)
    cycle()

    result = operand + 1
    reg[mode] = result & 0b11111111
    set_negative(reg, result)
    set_zero(reg, result)

def jump_execute(reg, operand, step):
    print_registers(f"{step}. Executing JMP", 50, reg)
    cycle()

    reg["pcl"] = reg["dirl"]
    reg["pch"] = operand

def load_execute(reg, reg_name, data, step, inc=False):
    print_registers(f"{step}. Storing value in reg", 50, reg)
    cycle()

    reg[reg_name] = data
    set_negative(reg, data)
    set_zero(reg, data)
    if inc: inc_pc(reg)

def lsr_execute(reg, operand, step, mode):
    print_registers(f"{step}. Executing LSR", 50, reg)
    cycle()

    result = operand >> 1
    reg[mode] = result & 0b11111111
    set_negative(reg, result)
    set_zero(reg, result)
    set_carry(reg, result)

def nop_execute(reg, step):
    print_registers(f"{step}. Executing NOP", 50, reg)
    cycle()

def ora_execute(reg, operand, step, inc=False):
    print_registers(f"{step}. Executing ORA", 50, reg)
    cycle()

    a = reg["a"]
    b = operand
    result = a | b
    reg["a"] = result
    set_negative(reg, result)
    set_zero(reg, result)
    if inc: inc_pc(reg)

def push(reg, memory, step, mode):
    print_registers(f"{step}. Pushing {mode} to stack", 50, reg)
    cycle()

    memory[0x0100 + reg["sp"]] = reg[mode]
    if reg["sp"] == 0x00: reg["sp"] = 0x00
    else: reg["sp"] -= 0x01

def pull(reg, memory, step, mode, update_flags=False):
    print_registers(f"{step}. Pulling {mode} from stack", 50, reg)
    cycle()

    if reg["sp"] == 0xFF: reg["sp"] = 0xFF
    else: reg["sp"] += 0x01
    reg[mode] = memory[0x0100 + reg["sp"]]

    if update_flags: 
        set_negative(reg, reg[mode])
        set_zero(reg, reg[mode])

def rmb_execute(reg, operand, bit, step):
    print_registers(f"{step}. Executing reset bit", 50, reg)
    cycle()

    reg["result"] = (operand & ~(1 << bit))

def rol_execute(reg, operand, step, mode):
    print_registers(f"{step}. Executing ROL", 50, reg)
    cycle()

    result = (operand << 1) | get_carry(reg)
    reg[mode] = result & 0b11111111
    set_negative(reg, result)
    set_zero(reg, result)
    set_carry(reg, result)

def ror_execute(reg, operand, step, mode):
    print_registers(f"{step}. Executing ROR", 50, reg)
    cycle()

    result = ((operand & 1) << 8) | (get_carry(reg) << 7) | (operand >> 1)
    reg[mode] = result & 0b11111111
    set_negative(reg, result)
    set_zero(reg, result)
    set_carry(reg, result)

def sbc_execute(reg, operand, step, inc=False):
    print_registers(f"{step}. Executing SBC", 50, reg)
    cycle()

    a = reg["a"]
    b = ((operand ^ 0b11111111) + 1)
    c = get_carry(reg)
    result = (a + b + c)
    reg["a"] = result & 0b11111111
    set_negative(reg, result)
    set_overflow(reg, a, b, c)
    set_zero(reg, result)
    set_carry(reg, result)
    if inc: inc_pc(reg)

def smb_execute(reg, operand, bit, step):
    print_registers(f"{step}. Executing set bit", 50, reg)
    cycle()

    reg["result"] = (operand | (1 << bit))

def stop_execute(reg, step):
    print_registers(f"{step}. Executing STOP", 50, reg)
    cycle()

    exit(0)

def trb_execute(reg, operand, step):
    print_registers(f"{step}. Executing TRB", 50, reg)
    cycle()

    result = operand & reg["a"]
    set_zero(reg, result)
    reg["result"] = (operand & ~reg["a"])

def tsb_execute(reg, operand, step):
    print_registers(f"{step}. Executing TSB", 50, reg)
    cycle()

    result = operand & reg["a"]
    set_zero(reg, result)
    reg["result"] = (operand | reg["a"])

def wai_execute(reg, step):
    print_registers(f"{step}. Executing WAIT", 50, reg)
    cycle()

    exit(0)


########################################################### Store #############################################################


def store_mem(reg, memory, address, data, step):
    print_registers(f"{step}. Storing value in mem", 50, reg)
    cycle()

    memory[address] = data

def store_reg(reg, reg_name, data, step, inc=False):
    print_registers(f"{step}. Storing value in reg", 50, reg)
    cycle()

    reg[reg_name] = data
    if inc: inc_pc(reg)