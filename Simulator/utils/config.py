# Simulation settings
cycle_mode = "run"      # "run" or "step"
cycle_speed = 5         # 1-5
print_mode = "no"      # "yes" or "no"

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
nonmaskable_interupt_vector_low = 0xFFFA
nonmaskable_interupt_vector_high = 0xFFFB
reset_vector_low = 0xFFFC
reset_vector_high = 0xFFFD
interupt_vector_low = 0xFFFE
interupt_vector_high = 0xFFFF