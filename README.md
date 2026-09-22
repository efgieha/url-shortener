# url-shortener

A minimal URL shortening API.

## Tech stack
 - backend: Django + DRF 
 - database: PostgreSQL 18
 - package manager: uv
 - Docker with Docker Compose

## Quick start

```bash
cp .envs/.example.env .envs/.local.env
cp .envs/.example.postgres.env .envs/.postgres.env
docker compose up --build
```

The API is available at http://localhost:9000. Migrations run automatically on container startup.

## Endpoints

| Method | Path                       | Description                                     |
| ------ | -------------------------- | ----------------------------------------------- |
| `POST` | `/api/links/`              | creates a short link from `{"long_url": "..."}` |
| `GET`  | `/api/links/<short_code>/` | expands a short code back to the original URL   |
| `GET`  | `/<short_code>/`           | redirects (302) to the original URL             |
| `GET`  | `/api/docs/`               | Swagger UI                                      |
| `GET`  | `/api/schema/`             | OpenAPI schema                                  |

## Usage

```bash
# shorten
curl -X POST http://localhost:9000/api/links/ \
  -H 'Content-Type: application/json' \
  -d '{"long_url": "http://example.com/very-very/long/url/even-longer"}'

# {"short_code": "aB3xY7kQ",
#  "long_url": "http://example.com/very-very/long/url/even-longer",
#  "short_url": "http://localhost:9000/aB3xY7kQ/"}

# expand
curl http://localhost:9000/api/links/aB3xY7kQ/

# redirect
curl -i http://localhost:9000/aB3xY7kQ/
```

## How to run tests

```bash
docker compose run --rm web pytest
```

## Project layout

```
config/          Django project: settings, root URLconf, wsgi/asgi
url_shortener/   project package
  links/         the shortener app: model, redirect view, API
tests/           unit tests, end-to-end tests, and type checks with mypy
```

## Decisions

- redirects use HTTP 302 to avoid browsers permanetly caching the redirect destination
- since "expanding a short URL" could mean returning the original URL or a redirecting to it, both are implemented
- short codes contain 8 randomly generated letters and digits with uniqueness enforced at the database level

## Some ideas for improvements (skipped for minimal version)

- custom aliases
- editing or disabling an existing link
- auth and link ownership
- link expiry
- rate limiting
- click analytics: counts, unique visitors, etc

