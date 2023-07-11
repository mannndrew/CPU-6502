from instructions.helper import *

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

def store(reg, memory, address, step, inc=False):
    print_registers(f"{step}. Storing value", 50, reg)
    cycle()

    memory[address] = reg["result"]

def check_branch(reg, memory, step, check, inc=False):
    print_registers(f"{step}. Checking branch", 50, reg)
    cycle()

    if check == 1: 
        reg["branch"] = 1
        reg["result"] = memory[get_pc(reg)]

    else: 
        reg["branch"] = 0
        print()

    if inc: inc_pc(reg)

def branch(reg, step):
    if reg["branch"] == 0:
        return

    print_registers(f"{step}. Branching", 50, reg)
    cycle()
    print()

    reg["pcl"] = add(reg["pcl"], reg["result"])

def adc_execute(reg, operand, step, inc=False):
    print_registers(f"{step}. Executing ADC", 50, reg)
    print()
    cycle()

    a = reg["a"]
    b = operand
    c = reg["flags"] & 0b00000001
    result = (a + b + c)
    reg["a"] = result & 0b11111111
    if check_negative(result):
        reg["flags"] |= 0b10000000
    if check_overflow_add(a, b, c):
        reg["flags"] |= 0b01000000
    if check_zero(result):
        reg["flags"] |= 0b00000010
    if check_carry(result):
        reg["flags"] |= 0b00000001
    
    if inc: inc_pc(reg)

def and_execute(reg, operand, step, inc=False):
    print_registers(f"{step}. Executing AND", 50, reg)
    print()
    cycle()

    a = reg["a"]
    b = operand
    result = a & b
    reg["a"] = result
    if check_negative(result):
        reg["flags"] |= 0b10000000
    if check_zero(result):
        reg["flags"] |= 0b00000010
    
    if inc: inc_pc(reg)

def asl_execute(reg, operand, step, mode, inc=False):
    print_registers(f"{step}. Executing ASL", 50, reg)
    print()
    cycle()

    result = operand << 1
    reg[mode] = result & 0b11111111
    if check_negative(result):
        reg["flags"] |= 0b10000000
    if check_zero(result):
        reg["flags"] |= 0b00000010
    if check_carry(operand):
        reg["flags"] |= 0b00000001
    
    if inc: inc_pc(reg)

def bit_execute(reg, operand, step, inc=False):
    print_registers(f"{step}. Executing BIT", 50, reg)
    print()
    cycle()

    a = reg["a"]
    b = operand
    result = a & b
    if get_bit(result, 7) == 1:
        reg["flags"] |= 0b10000000
    if get_bit(result, 6) == 1:
        reg["flags"] |= 0b01000000
    if check_zero(result):
        reg["flags"] |= 0b00000010
    
    if inc: inc_pc(reg)