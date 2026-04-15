FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 6767

# Run the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:6767", "app:app"]
