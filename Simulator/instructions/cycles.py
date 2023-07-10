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
        reg["carry"] = check_carry_add(address, reg["x"], 0)
    elif plus == "y":
        reg[mode] = add(address, reg["y"])
        reg["carry"] = check_carry_add(address, reg["y"], 0)

    if inc: inc_pc(reg)

def fetch_absolute_high(reg, address, step, mode, plus="", inc=False):
    print_registers(f"{step}. Fetching absolute page high address", 50, reg)
    cycle()

    if plus == "":
        reg[mode] = address
    elif (plus == "x" or plus == "y") and reg["carry"] == 1:
        reg[mode] = add(address, reg["carry"])
        
    if inc: inc_pc(reg)

def adc_execute(reg, operand, step, inc=False):
    print_registers(f"{step}. Executing ADC", 50, reg)
    print()
    cycle()

    a = reg["a"]
    b = operand
    c = reg["flags"] & 0b00000001
    result = (a + b + c) & 0b11111111
    reg["a"] = result
    if check_negative(result):
        reg["flags"] |= 0b10000000
    if check_overflow_add(a, b, c):
        reg["flags"] |= 0b01000000
    if check_zero(result):
        reg["flags"] |= 0b00000010
    if check_carry_add(a, b, c):
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