FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Create a non-root user
RUN addgroup -S appuser && adduser -S appuser -G appuser

COPY requirements.txt .
# Update packages to fix vulnerabilities and install dependencies
RUN apk update && \
    apk add --no-cache build-base gcc postgresql-dev linux-headers && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
RUN chmod 755 docker-entrypoint.sh

# Set ownership of the application files
RUN chown -R appuser:appuser /usr/src/app

# Switch to non-root user
USER appuser

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
