# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask application port (default is 5000)
EXPOSE 5000

# Default command will be overridden by docker-compose
CMD ["flask", "run", "--host=0.0.0.0"]
