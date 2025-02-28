# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements_docker.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements_docker.txt

# Copy the rest of the application
COPY . .

# Create output directory for saved assets
RUN mkdir -p output

# Make sure the output directory is writable
RUN chmod 777 output

# Expose the port Streamlit runs on
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]