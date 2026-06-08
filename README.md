# Personnal website (Jekyll)

To launch it in local, install Jekyll and run `bundle exec jekyll serve`

## Flask app (Docker)

Add docker-compose.override.yml

```
services:
  web:
    ports:
      - "5000:5000"
    labels:
      - "traefik.enable=false"
    environment:
      - FLASK_ENV=development
```

```bash
# Copy and fill in env vars
cp .env.example .env

# Build and start
docker compose up --build

# App available at http://localhost:5000
```

To stop:

```bash
docker compose down
```
