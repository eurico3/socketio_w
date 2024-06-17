# Use the official Python image from the Docker Hub
FROM python:3.11
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . ./
# Copy the requirements file into the working directory
#COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV btc

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "app:app"]