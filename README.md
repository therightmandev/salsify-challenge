### How does your system work? (if not addressed in comments in source)

First, the system pre-processes the file line by line, to avoid loading the entire file into memory. Then, it saves the character offset of every 10000th line in an index called `LINE_INDEX`.

Then, the server is started. For each request, the system gets the closest index entry to the  requested line (for line 21000, it gets `LINE_INDEX[2]`, which corresponds to line 20000) and, starting from the retrieved offset, reads line by line until the specified line is found and returns the line.




### How will your system perform with a 1 GB file? a 10 GB file? a 100 GB file?

Pre-processing will take proportionally longer with bigger files:
- 14MB file -> 5 seconds
- 1 GB file -> 179 seconds
- 10 GB file -> ~1790 seconds (estimate)

Responding to each request is the same speed, regardless of file size.
For example, here’s the average response time for a test I ran with 2 different files:
- 14 MB file -> 0.0401 seconds
- 1 GB file -> 0.0371 seconds
- 10 GB file -> ~0.04 seconds (estimate)

If the file gets too big, the index may not fit in memory, and we'd have to move it to a separate database. The number of elements in `LINE_INDEX` is `<number of lines in file> / 10000`. A file with 1 million lines would have 100 list elements, so it is a residual amount. If the `INDEX_INTERVAL` was reduced, this may deserve more consideration.




### How will your system perform with 100 users? 10000 users? 1000000 users?

Testing with hey (https://github.com/rakyll/hey) reveals that 50000 requests sent by 50 concurrent threads were processed efficiently. Here is a relevant statistic:
- 99% of requests were processed in 0.1022 secs

It is important to note that the test was conducted over a local network.
Another important thing to note is that the requests were made to the URL "http://localhost:8000/lines/9999", so the program would have to read 9999 lines. The reason is that the index has the offset for lines 0, 10000, 20000, etc. So the program starts from line 0 and runs `f.readline()` until it reaches line 9999 and returns the result. This matters because this request performs 9999 more IO operations (`f.readline()`) than a request to line 0 would.

All in all, the system performed extremely well under load.

When I ran 500000 requests with 50000 concurrency, I started getting a "socket: too many open files" error. This seems to be an arbitrary limit imposed by the operating system (https://stackoverflow.com/questions/18280612/ioerror-errno-24-too-many-open-files), but at some point, with too many concurrent requests, the system would likely start to take longer to respond to each request.




### What documentation, websites, papers, etc did you consult in doing this assignment?

- https://docs.python.org/3/tutorial/inputoutput.html
- https://stackoverflow.com/questions/62409573/what-is-the-fastest-way-to-read-several-lines-of-data-from-a-large-file
- https://stackoverflow.com/questions/33824359/read-file-line-by-line-with-asyncio
- https://stackoverflow.com/questions/15599639/what-is-the-perfect-counterpart-in-python-for-while-not-eof
- https://fastapi.tiangolo.com
- https://chat.deepseek.com
- https://chatgpt.com
- https://github.com/Tinche/aiofiles
- https://github.com/rakyll/hey




### What third-party libraries or other tools does the system use? How did you choose each library or framework you used?

FastAPI was chosen for high performance, as well as async capabilities and ease of development. aiofiles was initially used to read files asynchronously, but after testing with hey (https://github.com/rakyll/hey), the performance was worse than using Python's built-in file reading functions. The reason is probably because we are making small reads (only one line at a time).




### How long did you spend on this exercise? If you had unlimited more time to spend on this, how would you spend it and how would you prioritize each item?

7-9 hours. Including researching potential problems and solutions, testing with different files, considering different options, coding and answering the questions.

If I had unlimited time, I would:
- Add a cache
- Store the line index in a separate database, which would allow it to grow bigger than the available memory in case of really big files and/or a reduction of `INDEX_INTERVAL`. It would also allow pre-processing to only be done once in case of horizontal scaling (since the servers would all read from the same database)
- Experiment with the `INDEX_INTERVAL` value (currently 10000), to see which number would get the best overall results for our specific use case. The number 10000 was chosen arbitrarily and seems to give acceptable results
- Scale the system horizontally, allowing more requests to be served concurrently
- Split the file in chunks and pre-process it in parallel
- Add tests

I would start by adding tests, then a cache, then storing the index in a separate database and then scale horizontally.




### If you were to critique your code, what would you have to say about it?

The code is lacking exception handling, input validation, caching and tests. The index is saved in memory, which puts a size limit on it. I could also move the pre-processing code to a different file, especially if it was part of a bigger project.
