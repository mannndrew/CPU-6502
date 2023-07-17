import readchar
import time
cycle_mode = "run"
cycle_speed = 5
print_mode = "yes"

########################################################### Functions #########################################################

def cycle():
    if cycle_mode == "step":
        readchar.readkey()
    elif cycle_mode == "run":
        if cycle_speed == 1: time.sleep(1/1)
        elif cycle_speed == 2: time.sleep(1/10)
        elif cycle_speed == 3: time.sleep(1/1000)
        elif cycle_speed == 4: time.sleep(1/1000000)
        elif cycle_speed == 5: pass

def hex_value(dec):
    conversion_table = ['0', '1', '2', '3',
                        '4', '5', '6', '7',
                        '8', '9','A', 'B',
                        'C', 'D', 'E', 'F']
    
    remainder = 0
    hex = ""

    if dec == 0:
        return "00"

    while 0 < dec:
        remainder = dec % 16
        hex = conversion_table[remainder] + hex
        dec = dec // 16

    if len(hex) == 1:
        hex = "0" + hex
    
    return hex

def instruction_message(message):
    if print_mode == "yes":
        print(message)
    elif print_mode == "no":
        pass

def print_registers(message, offset, reg):
    if print_mode == "yes":
        print(f"{message:<{offset}}"
            f"A: {hex_value(reg['a'])}\t"
            f"X: {hex_value(reg['x'])}\t"
            f"Y: {hex_value(reg['y'])}\t"
            f"SP: {hex_value(reg['sp'])}\t"
            f"PC: {hex_value(reg['pch'])}{hex_value(reg['pcl'])}\t"
            f"Flags: {bin(reg['flags'])}")
    elif print_mode == "no":
        pass
    


def inc_pc(reg):
    if reg["pch"] == 0xFF and reg["pcl"] == 0xFF:
        reg["pch"] = 0x00
        reg["pcl"] = 0x00

    elif reg["pcl"] == 0xFF:
        reg["pch"] += 0x01
        reg["pcl"] = 0x00
    
    else:
        reg["pcl"] += 0x01

    return reg

def add(a, b):
    return (a + b) & 0xFF

def sub(a, b):
    return (a + (~b & 0xFF) + 1) & 0xFF

def get_pc(reg):
    return (reg["pch"] << 8) | reg["pcl"]

def get_dir(reg):
    return (reg["dirh"] << 8) | reg["dirl"]

def get_indir(reg):
    return (reg["indirh"] << 8) | reg["indirl"]

def get_bit(value, bit):
    return (value >> bit) & 0x01

########################################################### Flag Functions ####################################################

# Getters
def get_negative(reg):
    if (reg["flags"] & 0b10000000 != 0): return 1
    else: return 0

def get_overflow(reg):
    if (reg["flags"] & 0b01000000 != 0): return 1
    else: return 0

def get_break(reg):
    if (reg["flags"] & 0b00010000 != 0): return 1
    else: return 0

def get_decimal(reg):
    if (reg["flags"] & 0b00001000 != 0): return 1
    else: return 0

def get_interrupt(reg):
    if (reg["flags"] & 0b00000100 != 0): return 1
    else: return 0

def get_zero(reg):
    if (reg["flags"] & 0b00000010 != 0): return 1
    else: return 0

def get_carry(reg):
    if (reg["flags"] & 0b00000001 != 0): return 1
    else: return 0

# Check for possible flag changes
def check_negative(result):
    if (result & 0b10000000 != 0): return True
    else: return False

def check_overflow_add(a, b, cin):
    c6 = ((a & 0b1111111) + (b & 0b1111111) + cin) >> 7 
    c7 = (a + b + cin) >> 8
    if (c6 ^ c7 == 1): return True
    else: return False
            
def check_zero(result):
    if (result & 0b11111111 == 0): return True
    else: return False
            
def check_carry(result):
    c7 = result >> 8
    if (c7 == 1): return True
    else: return False

# Set flags
def set_negative(reg, result):
    if check_negative(result): 
        reg["flags"] |= 0b10000000
    else: 
        reg["flags"] &= 0b01111111

def set_overflow(reg, a, b, cin):
    if check_overflow_add(a, b, cin): 
        reg["flags"] |= 0b01000000
    else: 
        reg["flags"] &= 0b10111111

def set_zero(reg, result):
    if check_zero(result): 
        reg["flags"] |= 0b00000010
    else: 
        reg["flags"] &= 0b11111101

def set_carry(reg, result):
    if check_carry(result): 
        reg["flags"] |= 0b00000001
    else: 
        reg["flags"] &= 0b11111110