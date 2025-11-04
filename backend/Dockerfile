# Use official Python image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install system package dependencies
RUN apt-get update

# Upgrade Python packaging tools
RUN pip install --upgrade pip setuptools

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY ./app ./app

# Expose FastAPI port
EXPOSE 8001

# Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
