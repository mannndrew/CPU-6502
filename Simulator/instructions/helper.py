import readchar

########################################################### Functions #########################################################

def cycle():
    readchar.readkey()

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

def print_registers(message, offset, reg):

    print(f"{message:<{offset}}"
          f"A: {hex_value(reg['a'])}\t"
          f"X: {hex_value(reg['x'])}\t"
          f"Y: {hex_value(reg['y'])}\t"
          f"SP: {hex_value(reg['sp'])}\t"
          f"PC: {hex_value(reg['pch'])}{hex_value(reg['pcl'])}")

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

def get_pc(reg):
    return (reg["pch"] << 8) | reg["pcl"]

def get_dir(reg):
    return (reg["dirh"] << 8) | reg["dirl"]

def get_bit(value, bit):
    return (value >> bit) & 0x01

########################################################### Flag Functions ####################################################

# Getters
def get_negative(flags):
    if (flags & 0b10000000 != 0): return 1
    else: return 0

def get_overflow(flags):
    if (flags & 0b01000000 != 0): return 1
    else: return 0

def get_break(flags):
    if (flags & 0b00010000 != 0): return 1
    else: return 0

def get_decimal(flags):
    if (flags & 0b00001000 != 0): return 1
    else: return 0

def get_interrupt(flags):
    if (flags & 0b00000100 != 0): return 1
    else: return 0

def get_zero(flags):
    if (flags & 0b00000010 != 0): return 1
    else: return 0

def get_carry(flags):
    if (flags & 0b00000001 != 0): return 1
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