from instructions.helper import *

def adc_fetch_instruction(reg, step, inc):
    print_registers(f"{step}. Fetching instruction ADC", 50, reg)
    cycle()
    
    if inc: inc_pc(reg)

def adc_fetch_absolute_low(reg, memory, step, inc):
    print_registers(f"{step}. Fetching absolute page low address", 50, reg)
    cycle()
    reg["reg_dirl"] = memory[get_pc(reg)]

    if inc: inc_pc(reg)

def adc_fetch_absolute_high(reg, memory, step, inc):
    print_registers(f"{step}. Fetching absolute page high address", 50, reg)
    cycle()
    reg["reg_dirh"] = memory[get_pc(reg)]

    if inc: inc_pc(reg)

def adc_execute(reg, operand, step, inc):
    print_registers(f"{step}. Executing ADC", 50, reg)
    cycle()

    a = reg["reg_a"]
    b = operand
    c = reg["reg_flags"] & 0b00000001
    result = (a + b + c) & 0b11111111
    reg["reg_a"] = result
    if check_negative(result):
        reg["reg_flags"] |= 0b10000000
    if check_overflow_add(a, b, c):
        reg["reg_flags"] |= 0b01000000
    if check_zero(result):
        reg["reg_flags"] |= 0b00000010
    if check_carry_add(a, b, c):
        reg["reg_flags"] |= 0b00000001
    
    if inc: inc_pc(reg)