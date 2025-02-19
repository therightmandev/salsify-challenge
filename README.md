### How does your system work? (if not addressed in comments in source)

Pre-process the file line by line, to avoid loading the entire file into memory. Save the character offset of every 10000th line in an index. For each request, go to the nearest index entry, read line by line until the specified line is found and return the line.



### How will your system perform with a 1 GB file? a 10 GB file? a 100 GB file?

Pre-processing will take proportionally longer with bigger files. Responding to each request will be the same speed, regardless of file size. If the file gets too big, the index may not fit in memory, and we'd have to move it to a separate database.



### How will your system perform with 100 users? 10000 users? 1000000 users?

Testing with hey (https://github.com/rakyll/hey) reveals that 50000 requests sent by 50 concurrent threads were processed efficiently. Here are some relevant stats:
- 99% of requests were processed in 0.1022 secs

It is important to note that the test was conducted over a local network. Another important thing to note is that the requests were made to the URL "http://localhost:8000/lines/9999", so the program would have to read 9999 lines. The reason is that the index has the offset for lines 0, 10000, 20000, etc. So the program starts from line 0 and runs f.readline() until it reaches line 9999 and returns the result. This matters because this request performs 9999 more IO operations (f.readline()) than a request to line 0 would.

All in all, the system performed extremely well under load. When I ran 500000 requests with 50000 concurrency, I started getting a "socket: too many open files" error. This seems to be an arbitrary limit imposed by the operating system (https://stackoverflow.com/questions/18280612/ioerror-errno-24-too-many-open-files), but at some point, with too many concurrent requests, the system would likely start to take longer to respond to each request.



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

FastAPI was chosen for high performance, as well as async capabilities. aiofiles was initially used to read files asynchronously, but after testing with hey (https://github.com/rakyll/hey), the performance was worse than using Python's built-in file reading functions. The reason is probably because we are making small reads (only one line at a time).



### How long did you spend on this exercise? If you had unlimited more time to spend on this, how would you spend it and how would you prioritize each item?

6-8 hours. If I had unlimited time, I would start by adding a cache. I would move the line index to a separate database, like Redis. I would also experiment with the `INDEX_INTERVAL` value, to see which number would get the best overall results for our specific use case. I would also scale the system horizontally, allowing more requests to be served concurrently.

If the priority is handling bigger files, my first step would be to use Redis for the index. Then, I would add a cache, then scale horizontally.



### If you were to critique your code, what would you have to say about it?

The code is lacking exception handling, input validation, caching. The index is saved in memory, which puts a size limit on it.
