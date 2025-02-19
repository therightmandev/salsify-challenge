# helper file to create files to test the server

import random


CHUNK = 100000
FILE_NAME = "file_served4.txt"

with open(FILE_NAME, "w") as file:
    for i in range(CHUNK):
        file.write(f"{i} " * random.randint(1,3))
        file.write("\n")


offset = 0
total = 500

for i in range(total):
    if i % 100 == 0:
        print(f"{i}/{total}")
    offset += CHUNK
    with open(FILE_NAME, "a") as file:
        for j in range(CHUNK):
            file.write(f"{offset + j} " * random.randint(1,3))
            file.write("\n")
