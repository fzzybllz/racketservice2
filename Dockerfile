FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential gcc libpq-dev netcat-openbsd
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
RUN chmod 755 docker-entrypoint.sh

# Set ownership of the application files
RUN chown -R appuser:appuser /usr/src/app

# Switch to non-root user
USER appuser

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
