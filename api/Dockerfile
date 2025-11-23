# Use a Python base image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the uv requirements file
COPY api/requirements.txt api/

# Install dependencies using uv
RUN uv pip install -r api/requirements.txt --system

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
