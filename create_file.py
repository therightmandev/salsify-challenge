import random

CHUNK = 100000
FILE_NAME = "file_served2.txt"

with open(FILE_NAME, "w") as file:
    for i in range(CHUNK):
        file.write(f"{i} " * random.randint(1,3))
        file.write("\n")


offset = 0

for i in range(9):
    offset += CHUNK
    with open(FILE_NAME, "a") as file:
        for i in range(CHUNK):
            file.write(f"{offset + i} " * random.randint(1,3))
            file.write("\n")
