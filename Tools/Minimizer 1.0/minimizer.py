import sys

# open file
try:
    file = open('hex.txt', 'r')
except IOError:
    print("Failed to open file")
    sys.exit()

dup = set()

cur = []
temp = []
res = []

# read file
for line in file:
    hex = line.strip()
    # Check if empty
    if hex == '': continue
    # Check if duplicate
    if hex in dup: continue
    else: dup.add(hex)
    binary_val = bin(int(hex, 16))[2:].zfill(8)
    binary_list = [bit for bit in binary_val]  # Split binary string into a list of bits
    cur.append(binary_list)

print("Start:")
for i in range(len(cur)):
    print(''.join(cur[i]))
print()

# close file
file.close()

while cur != [] or temp != []:
    while cur != []:
        # Iterate thorugh mem
        for i in range(len(cur)):
            # Iterate through all 8 bits
            same = 8
            bit_idx = 0
            for j in range(8):
                if cur[0][j] != cur[i][j]:
                    same -= 1
                    bit_idx = j

            if same == 7:
                cur[0][bit_idx] = 'X'
                temp.append(cur[0])
                cur.pop(i)
                cur.pop(0)
                break

            elif i == len(cur) - 1:
                res.append(cur[0])
                cur.pop(0)

    cur = temp
    temp = []

print("Result:")
for i in range(len(res)):
    print(''.join(res[i]))
    