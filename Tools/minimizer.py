import sys

# open file
try:
    file = open('hex.txt', 'r')
except IOError:
    print("Failed to open file")
    sys.exit()

mem = []
temp = []
res = []

# read file
for line in file:
    hex = line.strip()
    binary_val = bin(int(hex, 16))[2:].zfill(8)
    binary_list = [bit for bit in binary_val]  # Split binary string into a list of bits
    mem.append(binary_list)

# close file
file.close()

while mem != [] or temp != []:
    while mem != []:
        # Iterate thorugh mem
        for i in range(len(mem)):
            # Iterate through all 8 bits
            same = 8
            bit_idx = 0
            for j in range(8):
                if mem[0][j] != mem[i][j]:
                    same -= 1
                    bit_idx = j

            if same == 7:
                mem[0][bit_idx] = 'X'
                temp.append(mem[0])
                mem.pop(i)
                mem.pop(0)
                break

            if i == len(mem) - 1:
                res.append(mem[0])
                mem.pop(0)

    mem = temp
    temp = []

print("Result:")
for i in range(len(res)):
    print(''.join(res[i]))
    