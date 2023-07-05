import sys
import time
import readchar


########################################################### File IO ###########################################################


# Check if the user has provided a file name
if len(sys.argv) != 2:
    print("Usage: python simulator.py <filename>")
    exit(2)

# Get the file name
filename = sys.argv[1]

# Check if the file is hex
if filename[-4:] != ".hex":
    print(f"File ({filename}) is not an hex file")
    exit(2)

# Check if the file exists
try:
    file = open(filename, "r")
except FileNotFoundError:
    print(f"File ({filename}) not found")
    exit(2)

# Print welcome message
print(f"Welcome to the W65C02S simulator!\n")

# Store hex file in memory
memory = []

# Print loading message
print("Loading in hexdump...")

for line in file:
    clean_line = line[6:].strip()
    for i in range(0, len(clean_line), 3):
        memory.append(clean_line[i:i+2])

# Close file
file.close()

# Convert char to int
for i in range(len(memory)):
    memory[i] = int(memory[i], 16)

# Print loading message
print(f"Hexdump loaded successfully!\n")


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
          f"A: {hex_value(reg['reg_a'])}\t"
          f"X: {hex_value(reg['reg_x'])}\t"
          f"Y: {hex_value(reg['reg_y'])}\t"
          f"SP: {hex_value(reg['reg_sp'])}\t"
          f"PC: {hex_value(reg['reg_pch'])}{hex_value(reg['reg_pcl'])}")

def inc_pc(reg):
    if reg["reg_pch"] == 0xFF and reg["reg_pcl"] == 0xFF:
        reg["reg_pch"] = 0x00
        reg["reg_pcl"] = 0x00

    elif reg["reg_pcl"] == 0xFF:
        reg["reg_pch"] += 0x01
        reg["reg_pcl"] = 0x00
    
    else:
        reg["reg_pcl"] += 0x01

    return reg

def add(a, b):
    return (a + b) & 0xFF


########################################################### Simulation ########################################################


# Default addresses
zero_page_begin = 0x0000
zero_page_end = 0x00FF
stack_pointer_end = 0x0100
stack_pointer_begin = 0x01FF
data_begin = 0x0200
data_end = 0x07FF
program_begin = 0x8000
program_end = 0xFFFF

# Default vectors
nonmaskable_interupt_vector_high = 0xFFFA
nonmaskable_interupt_vector_low = 0xFFFB
reset_vector_high = 0xFFFC
reset_vector_low = 0xFFFD
interupt_vector_high = 0xFFFE
interupt_vector_low = 0xFFFF

# Registers
reg = {
    "reg_x": 0x00,
    "reg_y": 0x00,
    "reg_sp": 0xFF,
    "reg_a": 0x00,
    "reg_pch": 0x00,
    "reg_pcl": 0x00,
    "reg_indirh": 0x00,
    "reg_indirl": 0x00,
    "reg_dirh": 0x00,
    "reg_dirl": 0x00,
    "reg_flags": 0x00,
    "reg_inst": 0x00
}

print(f"Beginning simulation...\n")

# Fetch instruction: 1 cycle

reg["reg_pch"] = program_begin >> 8
reg["reg_pcl"] = program_begin & 0xFF
address = 0x00

while True:
    match address:
        case 0x00:
            # BRK: 6 cycles
            print(f"---BRK s Instruction at address {hex(address)}---")

            # Fetch instruction: 1 cycle
            print_registers("1. Fetching instruction BRK", 50, reg)
            cycle()
            reg = inc_pc(reg)

            # Push PCH to stack
            print_registers("2. Pushing PCH to stack", 50, reg)
            cycle()
            memory[reg["reg_sp"]] = reg["reg_pch"]
            reg["reg_sp"] -= 0x01

            # Push PCL to stack
            print_registers("3. Pushing PCL to stack", 50, reg)
            cycle()
            memory[reg["reg_sp"]] = reg["reg_pcl"]
            reg["reg_sp"] -= 0x01

            # Push flags to stack & set break/interupt flag
            print_registers("4. Pushing flags to stack & setting flags", 50, reg)
            cycle()
            memory[reg["reg_sp"]] = reg["reg_flags"]
            reg["reg_sp"] -= 0x01
            reg["reg_flags"] |= 0b00010100

            # Load interrupt vector low byte
            print_registers("5. Loading interrupt vector low byte", 50, reg)
            cycle()
            reg["reg_pcl"] = memory[nonmaskable_interupt_vector_low]

            # Load interrupt vector high byte
            print_registers(f"6. Loading interrupt vector high byte", 50, reg)
            cycle()
            reg["reg_pch"] = memory[nonmaskable_interupt_vector_high]
            print()

        case 0x01:
            # ORA (zp, x): 5 cycles
            print(f"---ORA (zp, x) Instruction at address {hex(address)}---")

            # Fetch instruction: 1 cycle
            print_registers("1. Fetching instruction ORA", 50, reg)
            cycle()
            reg = inc_pc(reg)

            # Fetch operand: 1 cycle
            print_registers("2. Fetching operand", 50, reg)
            cycle()
            reg["reg_indirl"] = memory[add(reg["reg_pcl"], reg["reg_x"])]
            reg = inc_pc(reg)

            # Fetch real address low byte: 1 cycle
            print_registers("3. Fetching real address low byte", 50, reg)
            cycle()
            reg["reg_dirl"] = memory[reg["reg_indirl"]]

            # Fetch real address high byte: 1 cycle
            print_registers("4. Fetching real address high byte", 50, reg)
            cycle()
            reg["reg_dirh"] = memory[add(reg["reg_indirl"], 0x01)]

            # Execute instruction: 1 cycle
            print_registers("5. Executing instruction", 50, reg)
            cycle()
            reg["reg_a"] |= memory[reg["reg_dirh"]] << 8 | memory[reg["reg_dirl"]]



    # Fetch next instruction
    address = reg["reg_pch"] << 8 | reg["reg_pcl"]
