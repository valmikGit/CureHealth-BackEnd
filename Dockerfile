# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the Docker image
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver"]