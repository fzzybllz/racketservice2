# Racketservice

A web application for managing tennis racket stringing services. This application helps track customers, rackets, strings, and stringing orders.

## Features

- Customer management
- Racket inventory and tracking
- String inventory
- Order management with status tracking
- Hybrid string support

## Tech Stack

- Flask (Python web framework)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Docker & Docker Compose (Containerization)
- Gunicorn (WSGI HTTP Server)

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system
- Git (optional, for cloning the repository)

### Installation

1. Clone the repository (or download the source code):
   ```
   git clone <repository-url>
   cd racketservice2
   ```

2. Create a `.env` file in the project root with the following environment variables:
   ```
   SECRET_KEY=your-secret-key
   FLASK_APP=wsgi.py
   FLASK_DEBUG=0
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```

3. Build and start the Docker containers:
   ```
   docker compose up --build
   ```

4. Access the application at [http://localhost:8000](http://localhost:8000)

### Database Management

The application uses Flask-Migrate for database migrations.

#### Creating a new migration

After making changes to the models, create a new migration:

```
docker compose run --rm web flask db migrate -m "Description of changes"
```

#### Applying migrations

Apply pending migrations to the database:

```
docker compose run --rm web flask db upgrade
```

## Project Structure

- `app/` - Main application package
  - `__init__.py` - Application factory and route definitions
  - `models.py` - Database models
  - `forms.py` - Form definitions
  - `extensions.py` - Flask extensions
  - `templates/` - Jinja2 templates
  - `static/` - Static files (CSS, JS, images)
- `migrations/` - Database migrations
- `docker-compose.yml` - Docker Compose configuration
- `docker-compose.dev.yml` - Development Docker Compose configuration
- `Dockerfile` - Docker container definition
- `docker-entrypoint.sh` - Container startup script
- `docker-entrypoint-dev.sh` - Development container startup script
- `dev.sh` - Script to start development environment
- `config.py` - Application configuration
- `wsgi.py` - WSGI entry point

## Development

### Development Mode with Hot-Reloading

For active development with hot-reloading (changes apply immediately without restarting the container):

1. Make sure you have the `.env` file as described in the Installation section.

2. Start the development environment:
   ```
   ./dev.sh
   ```
   
   This script will:
   - Set up a fresh development environment
   - Mount your local code directories as volumes
   - Enable hot-reloading for Flask
   - Expose the PostgreSQL port for direct database access
   
3. Access the application at [http://localhost:8000](http://localhost:8000)

4. Make changes to the code and they will be automatically applied

5. The PostgreSQL database is accessible at `localhost:5432` with the credentials from your `.env` file

### Running locally with SQLite

For development, you can also run the application locally using SQLite:

1. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Modify `config.py` to use SQLite:
   ```python
   SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
       'sqlite:///' + os.path.join(basedir, 'app.db')
   ```

3. Initialize the database:
   ```
   flask db upgrade
   ```

4. Run the development server:
   ```
   flask run
   ```

### Docker Commands

- Start containers in background: `docker compose up -d`
- Stop containers: `docker compose down`
- Rebuild containers: `docker compose up --build`
- View logs: `docker compose logs`
- Execute command in web container: `docker compose run --rm web <command>`
- Start development mode: `./dev.sh`

## License

This project is licensed under the MIT License.
