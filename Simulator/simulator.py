import sys
import time



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

# Print loading message
print(f"Hexdump loaded successfully!\n")


########################################################### Simulator ###########################################################


def inc_pc(reg_pch, reg_pcl):
    if reg_pch == 0xFF and reg_pcl == 0xFF:
        reg_pch = 0x00
        reg_pcl = 0x00

    elif reg_pcl == 0xFF:
        reg_pch += 0x01
        reg_pcl = 0x00
    
    else:
        reg_pcl += 0x01

    return reg_pch, reg_pcl

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
reg_x = 0x00
reg_y = 0x00
reg_sp = 0xFF
reg_a = 0x00
reg_pch  = 0x00
reg_pcl = 0x00
reg_flags = 0x00
reg_inst = 0x00

# Fetch instruction: 1 cycle
time.sleep(1)
reg_inst = memory[0]
reg_pch, reg_pcl = inc_pc(reg_pch, reg_pcl)

while reg_inst != None:
    match reg_inst:
        case "00":
            # BRK: 6 cycles

            # Push PCH to stack
            time.sleep(1)
            memory[reg_sp] = reg_pch
            reg_sp -= 0x01

            # Push PCL to stack
            time.sleep(1)
            memory[reg_sp] = reg_pcl
            reg_sp -= 0x01

            # Push flags to stack & set break/interupt flag
            time.sleep(1)
            memory[reg_sp] = reg_flags
            reg_sp -= 0x01
            reg_flags |= 0b00010100

            # Load interrupt vector low byte
            time.sleep(1)
            reg_pcl = memory[nonmaskable_interupt_vector_low]

            # Load interrupt vector high byte
            time.sleep(1)
            reg_pch = memory[nonmaskable_interupt_vector_high]


# print(memory)