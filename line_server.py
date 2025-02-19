import sys

import uvicorn

from fastapi import FastAPI, Response, status
from time import perf_counter_ns


app = FastAPI()

if len(sys.argv) != 2:
    print("Usage: python3 line_server.py <text_file>")
    sys.exit(1)
    start_server()

FILE = sys.argv[1]
INDEX_INTERVAL = 10000


def create_index():
    print("creating index")
    line_index = []
    i = 0
    with open(FILE, mode="r", encoding="ascii") as f:
        offset = f.tell()
        line = f.readline()
        while line:
            if i % 100000 == 0:
                print(f"Processed {i} lines")
            if i % INDEX_INTERVAL == 0:
                line_index.append(offset)
            offset = f.tell()
            line = f.readline()
            i += 1
    print(f"Processed {i} lines")
    print("returning index")
    return line_index, i


LINE_INDEX, LINE_COUNT = create_index()


async def get_line(line_number):
    line = ""
    with open(FILE, mode="r", encoding="ascii") as f:
        start = line_number // INDEX_INTERVAL
        f.seek(LINE_INDEX[start])
        for i in range(line_number % INDEX_INTERVAL + 1):
            line = f.readline()
    return line


@app.get("/lines/{line_number}", status_code=200)
async def get_line_endpoint(line_number: int, response: Response):
    if line_number >= LINE_COUNT:
        response.status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        return ""
    t1_start = perf_counter_ns()
    line = await get_line(line_number)
    print(f"{perf_counter_ns() - t1_start} ns")
    return f"{line}"


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
