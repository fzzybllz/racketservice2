FROM python:3.11-alpine

WORKDIR /usr/src/app

# Create a non-root user
RUN addgroup -S appuser && adduser -S appuser -G appuser

# Copy requirements file
COPY requirements.txt .

# Update packages to fix vulnerabilities and install dependencies
RUN apk update && \
    apk add --no-cache build-base gcc postgresql-dev linux-headers && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Change ownership of the application files to the non-root user
RUN chown -R appuser:appuser /usr/src/app

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "wsgi.py"]
