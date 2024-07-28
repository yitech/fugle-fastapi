# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install vim for debugging purposes
RUN apt-get update && apt-get install -y vim && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container at /app
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1
ENV PYTHON_KEYRING_BACKEND=keyrings.cryptfile.cryptfile.CryptFileKeyring

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
