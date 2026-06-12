# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install playwright browsers
RUN playwright install

# Expose the port that Streamlit runs on (default is 8501)
EXPOSE 8501

# Environment variables for PostgreSQL (can be overridden at runtime)
ENV PGHOST=localhost \
    PGDATABASE=postgres \
    PGUSER=postgres \
    PGPASSWORD=63540@Post

# Run the Streamlit application when the container launches
# To run the console version, use: CMD ["python", "main.py"]
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]