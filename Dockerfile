# Use the Selenium base image
FROM selenium/standalone-chrome:latest

# Set the working directory for the container to use
WORKDIR /app

# Install necessary dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other files over
COPY . .

# Run the application
CMD ["python", "main.py"]
