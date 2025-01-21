# Use the official Python 3.11 image as a base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock ./

# Install pipenv and project dependencies
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy the entire project to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py

# Run the Flask application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

