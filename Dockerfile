# Use the official Python image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the Python script and the file to be served into the container
COPY line_server.py .

EXPOSE 8000

# Run the Python script with the provided argument
CMD ["python3", "line_server.py", "file_served2.txt"]
