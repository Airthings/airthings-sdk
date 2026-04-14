[![Airthings][logo]](https://www.airthings.com)

# Airthings API SDK for Python

API SDK for Airthings consumer products.

## Prerequisites

- [Python](https://www.python.org/downloads/) 3.10+
- [Poetry](https://python-poetry.org/docs/#installation) 2.x

## Getting started

```bash
make install
```

## Available commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make generate` | Regenerate API client from `openapi.yaml` |
| `make format` | Format code with black |
| `make lint` | Run black, pylint, and mypy |
| `make check` | Format + lint |

## Regenerating the API client

The `airthings_api_client/` package is auto-generated from `openapi.yaml` using `openapi-python-client`. Do not edit it manually.

```bash
make generate
```

[logo]: https://upload.wikimedia.org/wikipedia/commons/d/d1/Airthings_logo.svg