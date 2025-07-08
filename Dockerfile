# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only essential files
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Install only what we need
RUN pip install --no-cache-dir Flask==2.3.3 google-generativeai==0.3.2 python-dotenv==1.0.0 gunicorn==20.1.0

# Expose port
EXPOSE 5000

# Set environment variable
ENV FLASK_APP=app.py

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
