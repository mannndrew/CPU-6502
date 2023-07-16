import sys
import pygame
from instructions.cycles import *
from instructions.helper import *


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


########################################################### Simulation ########################################################


# Default addresses
zero_page_begin = 0x0000
zero_page_end = 0x00FF
stack_pointer_end = 0x0100
stack_pointer_begin = 0x01FF
screen_begin = 0x0200
screen_end = 0x05FF
data_begin = 0x0600
data_end = 0x7FFF
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
    "x": 0x00,
    "y": 0x00,
    "sp": 0xFF,
    "a": 0x00,
    "pch": 0x00,
    "pcl": 0x00,
    "indirh": 0x00,
    "indirl": 0x00,
    "dirh": 0x00,
    "dirl": 0x00,
    "flags": 0x00,
    "inst": 0x00,
    "carry": 0x00,
    "result": 0x00,
    "branch": 0x00
}

print(f"Beginning simulation...\n")


# Fetch instruction: 1 cycle

reg["pch"] = program_begin >> 8
reg["pcl"] = program_begin & 0xFF
address = get_pc(reg)

# Screen dimensions
width = 32
height = 32
pixel_size = 10  # Size of each pixel


# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((width * pixel_size, height * pixel_size))


while True:
    pos = screen_begin


    print(hex(address), hex(memory[address]))
    match memory[address]:
        case 0x00:
            # BRK: 7 cycles
            print(f"---BRK s Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BRK", inc=True)
            push(reg, memory, step=2, mode="pch")
            push(reg, memory, step=3, mode="pcl")
            push(reg, memory, step=4, mode="flags")
            flags_set(reg, flags=0b00010100, step=5)
            store_reg(reg, "pcl", memory[nonmaskable_interupt_vector_low], step=6)
            store_reg(reg, "pch", memory[nonmaskable_interupt_vector_low], step=7)
            print()

        case 0x01:
            # ORA (zp, x): 5 cycles
            print(f"---ORA (zp, x) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ORA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", plus="x", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            ora_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0x04:
            # TSB zp: 4 cycles
            print(f"---TSB zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="TSB", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            tsb_execute(reg, memory[reg["dirl"]], step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x05:
            # ORA zp: 3 cycles
            print(f"---ORA zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ORA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            ora_execute(reg, memory[reg["dirl"]], step=3)
            print()

        case 0x06:
            # ASL zp: 4 cycles
            print(f"---ASL zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ASL", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            asl_execute(reg, memory[reg["dirl"]], step=3, mode="result")
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x07:
            # RMB0 zp: 4 cycles
            print(f"---RMB0 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="RMB0", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            rmb_execute(reg, memory[reg["dirl"]], bit=0, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x08:
            # PHP s: 2 cycles
            print(f"---PHP s Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="PHP", inc=True)
            push(reg, memory, step=2, mode="flags")
            print()

        case 0x09:
            # ORA #: 2 cycles
            print(f"---ORA # Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ORA", inc=True)
            ora_execute(reg, memory[get_pc(reg)], step=2, inc=True)
            print()

        case 0x0A:
            # ASL A: 2 cycles
            print(f"---ASL A Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ASL", inc=True)
            asl_execute(reg, reg["a"], step=2, mode="a")
            print()

        case 0x0C:
            # TSB a: 5 cycles
            print(f"---TSB a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="TSB", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            tsb_execute(reg, memory[get_dir(reg)], step=4)
            store_mem(reg, memory, get_dir(reg), reg["result"], step=5)
            print()

        case 0x0D:
            # ORA a: 4 cycles
            print(f"---ORA a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ORA", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            ora_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x0E:
            # ASL a: 5 cycles
            print(f"---ASL a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ASL", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            asl_execute(reg, memory[get_dir(reg)], step=4, mode="result")
            store_mem(reg, memory, get_dir(reg), reg["result"], step=5)
            print()

        case 0x0F:
            # BBR0 r: 2/3 cycles
            print(f"---BBR0 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBR0", inc=True)
            branch_check(reg, memory, step=2, check=(not get_bit(memory[get_pc(reg)], 0)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x10:
            # BPL r: 2/3 cycles
            print(f"---BPL r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BPL", inc=True)
            branch_check(reg, memory, step=2, check=(not get_negative(reg)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x11:
            # ORA (zp), y: 5 cycles
            print(f"---ORA (zp), y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ORA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl", plus="y")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh", plus="y")
            ora_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0x12:
            # ORA (zp): 5 cycles
            print(f"---ORA (zp) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ORA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            ora_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0x14:
            # TRB zp: 4 cycles
            print(f"---TRB zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="TRB", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            trb_execute(reg, memory[reg["dirl"]], step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x15:
            # ORA zp, x: 3 cycles
            print(f"---ORA zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ORA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            ora_execute(reg, memory[reg["dirl"]], step=3)
            print()

        case 0x16:
            # ASL zp, x: 4 cycles
            print(f"---ASL zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ASL", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            asl_execute(reg, memory[reg["dirl"]], step=3, mode="result")
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x17:
            # RMB1 zp: 4 cycles
            print(f"---RMB1 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="RMB1", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            rmb_execute(reg, memory[reg["dirl"]], bit=1, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x18:
            # CLC i: 2 cycles
            print(f"---CLC i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CLC", inc=True)
            flags_clear(reg, flags=0b00000001, step=2)
            print()

        case 0x19:
            # ORA a, y: 4 cycles
            print(f"---ORA a, y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ORA", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="y", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="y", inc=True)
            ora_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x1A:
            # INC A: 2 cycles
            print(f"---INC A Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="INC", inc=True)
            increment_execute(reg, reg["a"], step=2, mode="a")
            print()

        case 0x1C:
            # TRB a: 5 cycles
            print(f"---TRB a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="TRB", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            trb_execute(reg, memory[get_dir(reg)], step=4)
            store_mem(reg, memory, get_dir(reg), reg["result"], step=5)
            print()

        case 0x1D:
            # ORA a, x: 4 cycles
            print(f"---ORA a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ORA", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            ora_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x1E:
            # ASL a, x: 5 cycles
            print(f"---ASL a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ASL", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="y", inc=True)
            asl_execute(reg, memory[get_dir(reg)], step=4, mode="result")
            store_mem(reg, memory, get_dir(reg), reg["result"], step=5)
            print()

        case 0x1F:
            # BBR1 r: 2/3 cycles
            print(f"---BBR1 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBR1", inc=True)
            branch_check(reg, memory, step=2, check=(not get_bit(memory[get_pc(reg)], 1)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x20:
            # JSR a: 6 cycles
            print(f"---JSR a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="JMP", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            push(reg, memory, step=4, mode="pch")
            push(reg, memory, step=5, mode="pcl")
            jump_execute(reg, reg["dirh"], step=6)
            print()

        case 0x21:
            # AND (zp, x): 5 cycles
            print(f"---AND (zp, x) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="AND", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", plus="x", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            and_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0x24:
            # BIT zp: 3 cycles
            print(f"---BIT zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BIT", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            bit_execute(reg, memory[reg["dirl"]], step=3)
            print()

        case 0x25:
            # AND zp: 3 cycles
            print(f"---AND zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="AND", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            and_execute(reg, memory[reg["dirl"]], step=3)
            print()

        case 0x26:
            # ROL zp: 4 cycles
            print(f"---ROL zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ROL", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            rol_execute(reg, memory[reg["dirl"]], step=3, mode="result")
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x27:
            # RMB2 zp: 4 cycles
            print(f"---RMB2 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="RMB2", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            rmb_execute(reg, memory[reg["dirl"]], bit=2, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x28:
            # PLP s: 2 cycles
            print(f"---PLP s Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="PLP", inc=True)
            pull(reg, memory, step=2, mode="flags")
            print()

        case 0x29:
            # AND #: 2 cycles
            print(f"---AND # Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="AND", inc=True)
            and_execute(reg, memory[get_pc(reg)], step=2, inc=True)
            print()

        case 0x2A:
            # ROL A: 2 cycles
            print(f"---ROL A Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ROL", inc=True)
            rol_execute(reg, reg["a"], step=2, mode="a")
            print()

        case 0x2C:
            # BIT a: 4 cycles
            print(f"---BIT a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BIT", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            bit_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x2D:
            # AND a: 4 cycles
            print(f"---AND a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="AND", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            and_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x2E:
            # ROL a: 5 cycles
            print(f"---ROL a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ROL", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            rol_execute(reg, memory[get_dir(reg)], step=3, mode="result")
            store_mem(reg, memory, get_dir(reg), reg["result"], step=4)
            print()

        case 0x2F:
            # BBR2 r: 2/3 cycles
            print(f"---BBR2 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBR2", inc=True)
            branch_check(reg, memory, step=2, check=(not get_bit(memory[get_pc(reg)], 2)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x30:
            # BMI r: 2/3 cycles
            print(f"---BMI r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BMI", inc=True)
            branch_check(reg, memory, step=2, check=(get_negative(reg)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x31:
            # AND (zp), y: 5 cycles
            print(f"---AND (zp), y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="AND", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, plus="y", mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, plus="y", mode="dirh")
            and_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0x32:
            # AND (zp): 5 cycles
            print(f"---AND (zp) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="AND", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            and_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0x34:
            # BIT zp, x: 3 cycles
            print(f"---BIT zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BIT", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            bit_execute(reg, memory[reg["dirl"]], step=3)
            print()

        case 0x35:
            # AND zp, x: 3 cycles
            print(f"---AND zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="AND", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            and_execute(reg, memory[reg["dirl"]], step=3)
            print()

        case 0x36:
            # ROL zp, x: 4 cycles
            print(f"---ROL zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ROL", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            rol_execute(reg, memory[reg["dirl"]], step=3, mode="result")
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x37:
            # RMB3 zp: 4 cycles
            print(f"---RMB3 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="RMB3", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            rmb_execute(reg, memory[reg["dirl"]], bit=3, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x38:
            # SEC i: 2 cycles
            print(f"---SEC i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SEC", inc=True)
            flags_set(reg, 0b00000001, step=2)
            print()

        case 0x39:
            # AND a, y: 4 cycles
            print(f"---AND a, y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="AND", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="y", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="y", inc=True)
            and_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x3A:
            # DEC A: 2 cycles
            print(f"---DEC A Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="DEC", inc=True)
            decrement_execute(reg, reg["a"], step=2, mode="a")
            print()

        case 0x3C:
            # BIT a, x: 4 cycles
            print(f"---BIT a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BIT", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            bit_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x3D:
            # AND a, x: 4 cycles
            print(f"---AND a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="AND", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            and_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x3E:
            # ROL a, x: 5 cycles
            print(f"---ROL a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ROL", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            rol_execute(reg, memory[get_dir(reg)], step=3, mode="result")
            store_mem(reg, memory, get_dir(reg), reg["result"], step=4)
            print()

        case 0x3F:
            # BBR3 r: 2/3 cycles
            print(f"---BBR3 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBR3", inc=True)
            branch_check(reg, memory, step=2, check=(not get_bit(memory[get_pc(reg)], 3)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x40:
            # RTI s: 4 cycles
            print(f"---RTI s Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="RTI")
            pull(reg, memory, step=2, mode="flags")
            pull(reg, memory, step=3, mode="pcl")
            pull(reg, memory, step=4, mode="pch")
            print()

        case 0x41:
            # EOR (zp, x): 5 cycles
            print(f"---EOR (zp, x) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="EOR", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", plus="x", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            eor_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0x45:
            # EOR zp: 3 cycles
            print(f"---EOR zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="EOR", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            eor_execute(reg, memory[reg["dirl"]], step=3)
            print()

        case 0x46:
            # LSR zp: 4 cycles
            print(f"---LSR zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LSR", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            lsr_execute(reg, memory[reg["dirl"]], step=3, mode="result")
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x47:
            # RMB4 zp: 4 cycles
            print(f"---RMB4 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="RMB4", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            rmb_execute(reg, memory[reg["dirl"]], bit=4, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x48:
            # PHA s: 2 cycles
            print(f"---PHA s Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="PHA", inc=True)
            push(reg, memory, step=2, mode="a")
            print()

        case 0x49:
            # EOR #: 2 cycles
            print(f"---EOR # Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="EOR", inc=True)
            eor_execute(reg, memory[get_pc(reg)], step=2, inc=True)
            print()

        case 0x4A:
            # LSR A: 2 cycles
            print(f"---LSR A Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LSR", inc=True)
            lsr_execute(reg, reg["a"], step=2, mode="a")
            print()

        case 0x4C:
            # JMP a: 3 cycles
            print(f"---JMP a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="JMP", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            jump_execute(reg, memory[get_pc(reg)], step=3)
            print()

        case 0x4D:
            # EOR a: 4 cycles
            print(f"---EOR a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="EOR", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            eor_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x4E:
            # LSR a: 5 cycles
            print(f"---LSR a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LSR", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            lsr_execute(reg, memory[get_dir(reg)], step=4, mode="result")
            store_mem(reg, memory, get_dir(reg), reg["result"], step=5)
            print()

        case 0x4F:
            # BBR4 r: 2/3 cycles
            print(f"---BBR4 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBR4", inc=True)
            branch_check(reg, memory, step=2, check=(not get_bit(memory[get_pc(reg)], 4)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x50:
            # BVC r: 2/3 cycles
            print(f"---BVC r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BVC", inc=True)
            branch_check(reg, memory, step=2, check=(not get_overflow(reg)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x51:
            # EOR (zp), y: 5 cycles
            print(f"---EOR (zp), y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="EOR", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, plus="y", mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, plus="y", mode="dirh")
            eor_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0x52:
            # EOR (zp): 5 cycles
            print(f"---EOR (zp) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="EOR", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            eor_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0x55:
            # EOR zp, x: 3 cycles
            print(f"---EOR zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="EOR", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            eor_execute(reg, memory[reg["dirl"]], step=3)
            print()

        case 0x56:
            # LSR zp, x: 4 cycles
            print(f"---LSR zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LSR", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            lsr_execute(reg, memory[reg["dirl"]], step=3, mode="result")
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x57:
            # RMB5 zp: 4 cycles
            print(f"---RMB5 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="RMB5", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            rmb_execute(reg, memory[reg["dirl"]], bit=5, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x58:
            # CLI i: 2 cycles
            print(f"---CLI i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CLI", inc=True)
            flags_clear(reg, flags=0b00000100, step=2)
            print()

        case 0x59:
            # EOR a, y: 4 cycles
            print(f"---EOR a, y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="EOR", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="y", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="y", inc=True)
            eor_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x5A:
            # PHY s: 2 cycles
            print(f"---PHY s Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="PHY", inc=True)
            push(reg, memory, step=2, mode="y")
            print()

        case 0x5D:
            # EOR a, x: 4 cycles
            print(f"---EOR a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="EOR", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            eor_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x5E:
            # LSR a, x: 5 cycles
            print(f"---LSR a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LSR", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            lsr_execute(reg, memory[get_dir(reg)], step=4, mode="result")
            store_mem(reg, memory, get_dir(reg), reg["result"], step=5)
            print()

        case 0x5F:
            # BBR5 r: 2/3 cycles
            print(f"---BBR5 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBR5", inc=True)
            branch_check(reg, memory, step=2, check=(not get_bit(memory[get_pc(reg)], 5)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x60:
            # RTS s: 3 cycles
            print(f"---RTS s Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="RTS", inc=True)
            pull(reg, memory, step=2, mode="pcl")
            pull(reg, memory, step=3, mode="pch")
            print()

        case 0x61:
            # ADC (zp, x): 5 cycles
            print(f"---ADC (zp, x) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ADC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", plus="x", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            adc_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0x64:
            # STZ zp: 3 cycles
            print(f"---STZ zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STZ", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            store_mem(reg, memory, reg["dirl"], reg["z"], step=3)
            print()

        case 0x65:
            # ADC zp: 3 cycles
            print(f"---ADC zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ADC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            adc_execute(reg, memory[reg["dirl"]], step=3)
            print()

        case 0x66:
            # ROR zp: 4 cycles
            print(f"---ROR zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ROR", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            ror_execute(reg, memory[reg["dirl"]], step=3, mode="result")
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x67:
            # RMB6 zp: 4 cycles
            print(f"---RMB6 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="RMB6", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            rmb_execute(reg, memory[reg["dirl"]], bit=6, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x68:
            # PLA s: 2 cycles
            print(f"---PLA s Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="PLA", inc=True)
            pull(reg, memory, step=2, mode="a", update_flags=True)
            print()

        case 0x69:
            # ADC #: 2 cycles
            print(f"---ADC # Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ADC", inc=True)
            adc_execute(reg, memory[get_pc(reg)], step=2, inc=True)
            print()
            
        case 0x6A:
            # ROR A: 2 cycles
            print(f"---ROR A Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ROR", inc=True)
            ror_execute(reg, reg["a"], step=2, mode="a")
            print()

        case 0x6C:
            # JMP (a): 5 cycles
            print(f"---JMP (a) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="JMP", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="indirh")
            fetch_absolute_low(reg, memory[get_indir(reg)], step=4, mode="dirl")
            jump_execute(reg, memory[(get_indir(reg) + 1) & 0xFFFF], step=5)
            print()

        case 0x6D:
            # ADC a: 4 cycles
            print(f"---ADC a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ADC", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            adc_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x6E:
            # ROR a: 5 cycles
            print(f"---ROR a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ROR", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            ror_execute(reg, memory[get_dir(reg)], step=3, mode="result")
            store_mem(reg, memory, get_dir(reg), reg["result"], step=4)
            print()

        case 0x6F:
            # BBR6 r: 2/3 cycles
            print(f"---BBR6 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBR6", inc=True)
            branch_check(reg, memory, step=2, check=(not get_bit(memory[get_pc(reg)], 6)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x70:
            # BVS r: 2/3 cycles
            print(f"---BVS r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BVS", inc=True)
            branch_check(reg, memory, step=2, check=(get_overflow(reg)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x71:
            # ADC (zp), y: 5 cycles
            print(f"---ADC (zp), y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ADC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, plus="y", mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, plus="y", mode="dirh")
            adc_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0x72:
            # ADC (zp): 5 cycles
            print(f"---ADC (zp) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ADC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            adc_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0x74:
            # STZ zp, x: 3 cycles
            print(f"---STZ zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STZ", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            store_mem(reg, memory, reg["dirl"], reg["z"], step=3)
            print()

        case 0x75:
            # ADC zp, x: 3 cycles
            print(f"---ADC zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ADC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            adc_execute(reg, memory[reg["dirl"]], step=3)
            print()

        case 0x76:
            # ROR zp, x: 4 cycles
            print(f"---ROR zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ROR", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            ror_execute(reg, memory[reg["dirl"]], step=3, mode="result")
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x77:
            # RMB7 zp: 4 cycles
            print(f"---RMB7 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="RMB7", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            rmb_execute(reg, memory[reg["dirl"]], bit=7, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x78:
            # SEI i: 2 cycles
            print(f"---SEI i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SEI", inc=True)
            flags_set(reg, 0b00000100, step=2)
            print()
            
        case 0x79:
            # ADC a, y: 4 cycles
            print(f"---ADC a, y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ADC", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="y", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="y", inc=True)
            adc_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x7A:
            # PLY s: 2 cycles
            print(f"---PLY s Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="PLY", inc=True)
            pull(reg, memory, step=2, mode="y", update_flags=True)
            print()

        case 0x7C:
            # JMP (a, x): ? cycles
            print(f"---JMP (a, x) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="JMP", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="indirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="indirh", plus="x")
            fetch_absolute_low(reg, memory[get_indir(reg)], step=4, mode="dirl")
            jump_execute(reg, memory[(get_indir(reg) + 1) & 0xFFFF], step=5)
            print()

        case 0x7D:
            # ADC a, x: 4 cycles
            print(f"---ADC a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ADC", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            adc_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0x7E:
            # ROR a, x: 5 cycles
            print(f"---ROR a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="ROR", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            ror_execute(reg, memory[get_dir(reg)], step=3, mode="result")
            store_mem(reg, memory, get_dir(reg), reg["result"], step=4)
            print()

        case 0x7F:
            # BBR7 r: 2/3 cycles
            print(f"---BBR7 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBR7", inc=True)
            branch_check(reg, memory, step=2, check=(not get_bit(memory[get_pc(reg)], 7)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x80:
            # BRA r: 3 cycles
            print(f"---BRA r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BRA", inc=True)
            branch_check(reg, memory, step=2, check=1, inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x81:
            # STA (zp, x): 5 cycles
            print(f"---STA (zp, x) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", plus="x", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            store_mem(reg, memory, get_dir(reg), reg["a"], step=5)
            print()

        case 0x84:
            # STY zp: 3 cycles
            print(f"---STY zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STY", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            store_mem(reg, memory, reg["dirl"], reg["y"], step=3)
            print()

        case 0x85:
            # STA zp: 3 cycles
            print(f"---STA zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            store_mem(reg, memory, reg["dirl"], reg["a"], step=3)
            print()

        case 0x86:
            # STX zp: 3 cycles
            print(f"---STX zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STX", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            store_mem(reg, memory, reg["dirl"], reg["x"], step=3)
            print()

        case 0x87:
            # SMB0 zp: 4 cycles
            print(f"---SMB0 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SMB0", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            smb_execute(reg, memory[reg["dirl"]], bit=0, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x88:
            # DEY i: 2 cycles
            print(f"---DEY i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="DEY", inc=True)
            decrement_execute(reg, reg["y"], step=2, mode="y")
            print()

        case 0x89:
            # BIT #: 2 cycles
            print(f"---BIT # Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BIT", inc=True)
            bit_execute(reg, memory[get_pc(reg)], step=2, inc=True)
            print()

        case 0x8A:
            # TXA i: 2 cycles
            print(f"---TXA i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="TXA", inc=True)
            store_reg(reg, "a", reg["x"], step=2)

        case 0x8C:
            # STY a: 4 cycles
            print(f"---STY a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STY", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            store_mem(reg, memory, get_dir(reg), reg["y"], step=4)
            print()

        case 0x8D:
            # STA a: 4 cycles
            print(f"---STA a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STA", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            store_mem(reg, memory, get_dir(reg), reg["a"], step=4)
            print()

        case 0x8E:
            # STX a: 4 cycles
            print(f"---STX a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STX", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            store_mem(reg, memory, get_dir(reg), reg["x"], step=4)
            print()

        case 0x8F:
            # BBS0 r: 2/3 cycles
            print(f"---BBS0 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBS0", inc=True)
            branch_check(reg, memory, step=2, check=(get_bit(memory[get_pc(reg)], 0)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x90:
            # BCC r: 2/3 cycles
            print(f"---BCC r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BCC", inc=True)
            branch_check(reg, memory, step=2, check=(not get_carry(reg)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0x91:
            # STA (zp), y: 5 cycles
            print(f"---STA (zp), y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl", plus="y")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh", plus="y")
            store_mem(reg, memory, get_dir(reg), reg["a"], step=5)
            print()

        case 0x92:
            # STA (zp): 5 cycles
            print(f"---STA (zp) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            store_mem(reg, memory, get_dir(reg), reg["a"], step=5)
            print()

        case 0x94:
            # STY zp, x: 3 cycles
            print(f"---STY zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STY", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            store_mem(reg, memory, reg["dirl"], reg["y"], step=3)
            print()

        case 0x95:
            # STA zp, x: 3 cycles
            print(f"---STA zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            store_mem(reg, memory, reg["dirl"], reg["a"], step=3)
            print()

        case 0x96:
            # STX zp, y: 3 cycles
            print(f"---STX zp, y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STX", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="y", inc=True)
            store_mem(reg, memory, reg["dirl"], reg["x"], step=3)
            print()

        case 0x97:
            # SMB1 zp: 4 cycles
            print(f"---SMB1 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SMB1", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            smb_execute(reg, memory[reg["dirl"]], bit=1, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0x98:
            # TYA i: 2 cycles
            print(f"---TYA i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="TYA", inc=True)
            store_reg(reg, "a", reg["y"], step=2)

        case 0x99:
            # STA a, y: 4 cycles
            print(f"---STA a, y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STA", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="y", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="y", inc=True)
            store_mem(reg, memory, get_dir(reg), reg["a"], step=4)
            print()

        case 0x9A:
            # TXS i: 2 cycles
            print(f"---TXS i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="TXS", inc=True)
            store_reg(reg, "sp", reg["x"], step=2)

        case 0x9C:
            # STZ a: 4 cycles
            print(f"---STZ a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STZ", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            store_mem(reg, memory, get_dir(reg), reg["z"], step=4)
            print()

        case 0x9D:
            # STA a, x: 4 cycles
            print(f"---STA a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STA", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            store_mem(reg, memory, get_dir(reg), reg["a"], step=4)
            print()

        case 0x9E:
            # STZ a, x: 4 cycles
            print(f"---STZ a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STZ", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            store_mem(reg, memory, get_dir(reg), reg["z"], step=4)
            print()

        case 0x9F:
            # BBS1 r: 2/3 cycles
            print(f"---BBS1 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBS1", inc=True)
            branch_check(reg, memory, step=2, check=(get_bit(memory[get_pc(reg)], 1)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0xA0:
            # LDY #: 2 cycles
            print(f"---LDY # Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDY", inc=True)
            load_execute(reg, "y", memory[get_pc(reg)], step=2, inc=True)
            print()

        case 0xA1:
            # LDA (zp, x): 5 cycles
            print(f"---LDA (zp, x) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", plus="x", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            load_execute(reg, "a", memory[get_dir(reg)], step=5)
            print()

        case 0xA2:
            # LDX #: 2 cycles
            print(f"---LDX # Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDX", inc=True)
            load_execute(reg, "x", memory[get_pc(reg)], step=2, inc=True)
            print()

        case 0xA4:
            # LDY zp: 3 cycles
            print(f"---LDY zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDY", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            load_execute(reg, "y", memory[reg["dirl"]], step=3)
            print()

        case 0xA5:
            # LDA zp: 3 cycles
            print(f"---LDA zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            load_execute(reg, "a", memory[reg["dirl"]], step=3)
            print()

        case 0xA6:
            # LDX zp: 3 cycles
            print(f"---LDX zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDX", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            load_execute(reg, "x", memory[reg["dirl"]], step=3)
            print()

        case 0xA7:
            # SMB2 zp: 4 cycles
            print(f"---SMB2 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SMB2", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            smb_execute(reg, memory[reg["dirl"]], bit=2, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0xA8:
            # TAY i: 2 cycles
            print(f"---TAY i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="TAY", inc=True)
            store_reg(reg, "y", reg["a"], step=2)

        case 0xA9:
            # LDA #: 2 cycles
            print(f"---LDA # Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDA", inc=True)
            load_execute(reg, "a", memory[get_pc(reg)], step=2, inc=True)
            print()

        case 0xAA:
            # TAX i: 2 cycles
            print(f"---TAX i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="TAX", inc=True)
            store_reg(reg, "x", reg["a"], step=2)

        case 0xAC:
            # LDY a: 4 cycles
            print(f"---LDY a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDY", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            load_execute(reg, "y", memory[get_dir(reg)], step=4)
            print()

        case 0xAD:
            # LDA a: 4 cycles
            print(f"---LDA a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDA", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            load_execute(reg, "a", memory[get_dir(reg)], step=4)
            print()

        case 0xAE:
            # LDX a: 4 cycles
            print(f"---LDX a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDX", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            load_execute(reg, "x", memory[get_dir(reg)], step=4)
            print()

        case 0xAF:
            # BBS2 r: 2/3 cycles
            print(f"---BBS2 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBS2", inc=True)
            branch_check(reg, memory, step=2, check=(get_bit(memory[get_pc(reg)], 2)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0xB0:
            # BCS r: 2/3 cycles
            print(f"---BCS r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BCS", inc=True)
            branch_check(reg, memory, step=2, check=(get_carry(reg)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0xB1:
            # LDA (zp), y: 5 cycles
            print(f"---LDA (zp), y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl", plus="y")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh", plus="y")
            load_execute(reg, "a", memory[get_dir(reg)], step=5)
            print()

        case 0xB2:
            # LDA (zp): 5 cycles
            print(f"---LDA (zp) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            load_execute(reg, "a", memory[get_dir(reg)], step=5)
            print()

        case 0xB4:
            # LDY zp, x: 3 cycles
            print(f"---LDY zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDY", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            load_execute(reg, "y", memory[reg["dirl"]], step=3)
            print()

        case 0xB5:
            # LDA zp, x: 3 cycles
            print(f"---LDA zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDA", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            load_execute(reg, "a", memory[reg["dirl"]], step=3)
            print()

        case 0xB6:
            # LDX zp, y: 3 cycles
            print(f"---LDX zp, y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDX", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="y", inc=True)
            load_execute(reg, "x", memory[reg["dirl"]], step=3)
            print()

        case 0xB7:
            # SMB3 zp: 4 cycles
            print(f"---SMB3 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SMB3", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            smb_execute(reg, memory[reg["dirl"]], bit=3, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0xB8:
            # CLV i: 2 cycles
            print(f"---CLV i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CLV", inc=True)
            flags_clear(reg, flags=0b01000000, step=2)
            print()

        case 0xB9:
            # LDA a, y: 4 cycles
            print(f"---LDA a, y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDA", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="y", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="y", inc=True)
            load_execute(reg, "a", memory[get_dir(reg)], step=4)
            print()

        case 0xBA:
            # TSX i: 2 cycles
            print(f"---TSX i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="TSX", inc=True)
            store_reg(reg, "x", reg["sp"], step=2)

        case 0xBC:
            # LDY a, x: 4 cycles
            print(f"---LDY a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDY", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            load_execute(reg, "y", memory[get_dir(reg)], step=4)
            print()
        
        case 0xBD:
            # LDA a, x: 4 cycles
            print(f"---LDA a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDA", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            load_execute(reg, "a", memory[get_dir(reg)], step=4)
            print()

        case 0xBE:
            # LDX a, y: 4 cycles
            print(f"---LDX a, y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="LDX", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="y", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="y", inc=True)
            load_execute(reg, "x", memory[get_dir(reg)], step=4)
            print()

        case 0xBF:
            # BBS3 r: 2/3 cycles
            print(f"---BBS3 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBS3", inc=True)
            branch_check(reg, memory, step=2, check=(get_bit(memory[get_pc(reg)], 3)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0xC0:
            # CPY #: 2 cycles
            print(f"---CPY # Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CPY", inc=True)
            compare_execute(reg, memory[get_pc(reg)], step=2, mode="y", inc=True)
            print()

        case 0xC1:
            # CMP (zp, x): 5 cycles
            print(f"---CMP (zp, x) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CMP", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", plus="x", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            compare_execute(reg, memory[get_dir(reg)], step=5, mode="a")
            print()

        case 0xC4:
            # CPY zp: 3 cycles
            print(f"---CPY zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CPY", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            compare_execute(reg, memory[reg["dirl"]], step=3, mode="y")
            print()

        case 0xC5:
            # CMP zp: 3 cycles
            print(f"---CMP zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CMP", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            compare_execute(reg, memory[reg["dirl"]], step=3, mode="a")
            print()

        case 0xC6:
            # DEC zp: 4 cycles
            print(f"---DEC zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="DEC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            decrement_execute(reg, memory[reg["dirl"]], step=3, mode="result")
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0xC7:
            # SMB4 zp: 4 cycles
            print(f"---SMB4 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SMB4", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            smb_execute(reg, memory[reg["dirl"]], bit=4, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0xC8:
            # INY i: 2 cycles
            print(f"---INY i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="INY", inc=True)
            increment_execute(reg, reg["y"], step=2, mode="y")
            print()

        case 0xC9:
            # CMP #: 2 cycles
            print(f"---CMP # Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CMP", inc=True)
            compare_execute(reg, memory[get_pc(reg)], step=2, mode="a", inc=True)
            print()

        case 0xCA:
            # DEX i: 2 cycles
            print(f"---DEX i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="DEX", inc=True)
            decrement_execute(reg, reg["x"], step=2, mode="x")
            print()
        
        case 0xCB:
            # WAI i: 2 cycles
            print(f"---WAI i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="WAI", inc=True)
            wai_execute(reg, step=2)

        case 0xCC:
            # CPY a: 4 cycles
            print(f"---CPY a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CPY", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            compare_execute(reg, memory[get_dir(reg)], step=4, mode="y")
            print()

        case 0xCD:
            # CMP a: 4 cycles
            print(f"---CMP a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CMP", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            compare_execute(reg, memory[get_dir(reg)], step=4, mode="a")
            print()

        case 0xCE:
            # DEC a: 5 cycles
            print(f"---DEC a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="DEC", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            decrement_execute(reg, memory[get_dir(reg)], step=4, mode="result")
            store_mem(reg, memory, get_dir(reg), reg["result"], step=5)
            print()

        case 0xCF:
            # BBS4 r: 2/3 cycles
            print(f"---BBS4 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBS4", inc=True)
            branch_check(reg, memory, step=2, check=(get_bit(memory[get_pc(reg)], 4)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0xD0:
            # BNE r: 2/3 cycles
            print(f"---BNE r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BNE", inc=True)
            branch_check(reg, memory, step=2, check=(not get_zero(reg)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0xD1:
            # CMP (zp), y: 5 cycles
            print(f"---CMP (zp), y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CMP", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl", plus="y")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh", plus="y")
            compare_execute(reg, memory[get_dir(reg)], step=5, mode="a")
            print()
        
        case 0xD2:
            # CMP (zp): 5 cycles
            print(f"---CMP (zp) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CMP", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            compare_execute(reg, memory[get_dir(reg)], step=5, mode="a")
            print()

        case 0xD5:
            # CMP zp, x: 3 cycles
            print(f"---CMP zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CMP", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            compare_execute(reg, memory[reg["dirl"]], step=3, mode="a")
            print()

        case 0xD6:
            # DEC zp, x: 4 cycles
            print(f"---DEC zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="DEC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            decrement_execute(reg, memory[reg["dirl"]], step=3, mode="result")
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0xD7:
            # SMB5 zp: 4 cycles
            print(f"---SMB5 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SMB5", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            smb_execute(reg, memory[reg["dirl"]], bit=5, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0xD8:
            # CLD i: 2 cycles
            print(f"---CLD i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CLD", inc=True)
            flags_clear(reg, flags=0b00001000, step=2)
            print()

        case 0xD9:
            # CMP a, y: 4 cycles
            print(f"---CMP a, y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CMP", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="y", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="y", inc=True)
            compare_execute(reg, memory[get_dir(reg)], step=4, mode="a")
            print()

        case 0xDA:
            # PHX s: 2 cycles
            print(f"---PHX s Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="PHX", inc=True)
            push(reg, memory, step=2, mode="x")
            print()

        case 0xDB:
            # STP i: 2 cycles
            print(f"---STP i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="STP", inc=True)
            stop_execute(reg, step=2)

        case 0xDD:
            # CMP a, x: 4 cycles
            print(f"---CMP a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CMP", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            compare_execute(reg, memory[get_dir(reg)], step=4, mode="a")
            print()

        case 0xDE:
            # DEC a, x: 5 cycles
            print(f"---DEC a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="DEC", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            decrement_execute(reg, memory[get_dir(reg)], step=4, mode="result")
            store_mem(reg, memory, get_dir(reg), reg["result"], step=5)
            print()

        case 0xDF:
            # BBS5 r: 2/3 cycles
            print(f"---BBS5 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBS5", inc=True)
            branch_check(reg, memory, step=2, check=(get_bit(memory[get_pc(reg)], 5)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0xE0:
            # CPX #: 2 cycles
            print(f"---CPX # Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CPX", inc=True)
            compare_execute(reg, memory[get_pc(reg)], step=2, mode="x", inc=True)
            print()

        case 0xE1:
            # SBC (zp, x): 5 cycles
            print(f"---SBC (zp, x) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SBC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", plus="x", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            sbc_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0xE4:
            # CPX zp: 3 cycles
            print(f"---CPX zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CPX", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            compare_execute(reg, memory[reg["dirl"]], step=3, mode="x")
            print()

        case 0xE5:
            # SBC zp: 3 cycles
            print(f"---SBC zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SBC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            sbc_execute(reg, memory[reg["dirl"]], step=3)
            print()

        case 0xE6:
            # INC zp: 4 cycles
            print(f"---INC zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="INC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            increment_execute(reg, memory[reg["dirl"]], step=3, mode="result")
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0xE7:
            # SMB6 zp: 4 cycles
            print(f"---SMB6 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SMB6", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            smb_execute(reg, memory[reg["dirl"]], bit=6, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0xE8:
            # INX i: 2 cycles
            print(f"---INX i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="INX", inc=True)
            increment_execute(reg, reg["x"], step=2, mode="x")
            print()

        case 0xE9:
            # SBC #: 2 cycles
            print(f"---SBC # Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SBC", inc=True)
            sbc_execute(reg, memory[get_pc(reg)], step=2, inc=True)
            print()

        case 0xEA:
            # NOP i: 2 cycles
            print(f"---NOP i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="NOP", inc=True)
            nop_execute(reg, step=2)
            print()

        case 0xEC:
            # CPX a: 4 cycles
            print(f"---CPX a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="CPX", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            compare_execute(reg, memory[get_dir(reg)], step=4, mode="x")
            print()

        case 0xED:
            # SBC a: 4 cycles
            print(f"---SBC a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SBC", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            sbc_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0xEE:
            # INC a: 5 cycles
            print(f"---INC a Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="INC", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", inc=True)
            increment_execute(reg, memory[get_dir(reg)], step=4, mode="result")
            store_mem(reg, memory, get_dir(reg), reg["result"], step=5)
            print()

        case 0xEF:
            # BBS6 r: 2/3 cycles
            print(f"---BBS6 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBS6", inc=True)
            branch_check(reg, memory, step=2, check=(get_bit(memory[get_pc(reg)], 6)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0xF0:
            # BEQ r: 2/3 cycles
            print(f"---BEQ r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BCS", inc=True)
            branch_check(reg, memory, step=2, check=(get_zero(reg)), inc=True)
            branch_execute(reg, step=3)
            print()

        case 0xF1:
            # SBC (zp), y: 5 cycles
            print(f"---SBC (zp), y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SBC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, plus="y", mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, plus="y", mode="dirh")
            sbc_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0xF2:
            # SBC (zp): 5 cycles
            print(f"---SBC (zp) Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SBC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="indirl", inc=True)
            fetch_absolute_low(reg, memory[reg["indirl"]], step=3, mode="dirl")
            fetch_absolute_high(reg, memory[add(reg["indirl"], 1)], step=4, mode="dirh")
            sbc_execute(reg, memory[get_dir(reg)], step=5)
            print()

        case 0xF5:
            # SBC zp, x: 3 cycles
            print(f"---SBC zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SBC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            sbc_execute(reg, memory[reg["dirl"]], step=3)
            print()

        case 0xF6:
            # INC zp, x: 4 cycles
            print(f"---INC zp, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="INC", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            increment_execute(reg, memory[reg["dirl"]], step=3, mode="result")
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0xF7:
            # SMB7 zp: 4 cycles
            print(f"---SMB7 zp Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SMB7", inc=True)
            fetch_zero(reg, memory[get_pc(reg)], step=2, mode="dirl", inc=True)
            smb_execute(reg, memory[reg["dirl"]], bit=7, step=3)
            store_mem(reg, memory, reg["dirl"], reg["result"], step=4)
            print()

        case 0xF8:
            # SED i: 2 cycles
            print(f"---SED i Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SEC", inc=True)
            flags_set(reg, 0b00001000, step=2)
            print()

        case 0xF9:
            # SBC a, y: 4 cycles
            print(f"---SBC a, y Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SBC", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="y", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="y", inc=True)
            sbc_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0xFA:
            # PLX s: 2 cycles
            print(f"---PLX s Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="PLX", inc=True)
            pull(reg, memory, step=2, mode="x", update_flags=True)
            print()

        case 0xFD:
            # SBC a, x: 4 cycles
            print(f"---SBC a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="SBC", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            sbc_execute(reg, memory[get_dir(reg)], step=4)
            print()

        case 0xFE:
            # INC a, x: 5 cycles
            print(f"---INC a, x Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="INC", inc=True)
            fetch_absolute_low(reg, memory[get_pc(reg)], step=2, mode="dirl", plus="x", inc=True)
            fetch_absolute_high(reg, memory[get_pc(reg)], step=3, mode="dirh", plus="x", inc=True)
            increment_execute(reg, memory[get_dir(reg)], step=4, mode="result")
            store_mem(reg, memory, get_dir(reg), reg["result"], step=5)
            print()

        case 0xFF:
            # BBS7 r: 2/3 cycles
            print(f"---BBS7 r Instruction at address {hex(address)}---")
            fetch_instruction(reg, step=1, name="BBS7", inc=True)
            branch_check(reg, memory, step=2, check=(get_bit(memory[get_pc(reg)], 7)), inc=True)
            branch_execute(reg, step=3)
            print()

    

    for y in range(height):
        for x in range(width):
            data = memory[pos]
            pos += 1

            if data == 0:
                pixel_color = (0, 0, 0)  # Black
            else:
                pixel_color = (255, 255, 255)  # White

            pixel_pos = (x * pixel_size, y * pixel_size)
            pygame.draw.rect(screen, pixel_color, (pixel_pos, (pixel_size, pixel_size)))

    # Update the screen
    pygame.display.flip()

    # Fetch next instruction
    address = get_pc(reg)
