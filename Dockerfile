# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 to the outside world
EXPOSE 8000

# Define environment variables (optional)
ENV NODE_ENV=production

# Run Gunicorn using pipenv's virtual environment
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "app:app"]