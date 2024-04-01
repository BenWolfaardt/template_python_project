# Template Python Project

A template `Python` project implemented using hexagonal architecture with a `YAML` Pythonic config, `SQLAlchemy PostgreSQL` DB and `FastAPI` - the basics to get most projects up and running in no time.

## Table of Contents

1. [Local Setup and Configuration](#local-setup-and-configuration)
    - 1.1 [Run Locally](#run-locally)
    - 1.2 [Run on Docker](#run-on-docker)
    - 1.3 [Pre-commit](#pre-commit)
2. [Scripts](#scripts)
3. [Todos](#todos)

## Local Setup and Configuration

Things to know to get up and running.

- Run the application using either the local or `Docker` approach.
- See the `./configs/` directory to modify the behaviour of the application.
- Interact with the application in your browser at: [http://localhost:8080/docs](http://localhost:8080/docs)

### Run Locally

Setting up our environment

```sh
  poetry install
  poetry shell
```

> `python -m src --env <choice>`

See `python -m src -h` for a list of choices.

### Run on Docker

```sh
  docker compose up
```

### Pre-commit

> To be setup before commiting any code.

Setup and run the pre-commit (uses .pre-commit-config.yaml):

```sh
  pre-commit install
  pre-commit run --all-files
```

> The above needs to be performed from within the virtual environment.

## Scripts

- `python scripts/run_migration.py --env local`
  - Create `Alembic` migrations for table changes.

## Todos

- [ ] Add GitHub actions
- [ ] Have other branches with less should one want to start from a smaller footprint than this
- [ ] Update pre-commit to use ruff - see FastApi tutorial for Pull Request
- [ ] Update to SQLAlchemy v2
- [ ] See FastApi template repo for other tips and tricks
- [ ] pscopy parse in argument in pyprojects.toml
- [ ] init.sql to work with .env variable - see phoen stack overflow
- [ ] Have the repetitive part of my README in a gist?
- [ ] Add coverages reports
- [ ] Add tests
- [ ] Parse in logging level from config to logger
- [ ] Better FastAPI exception handling: @app.exception_handler(Error)  # async def error_handler(_: Request, e: Error):
- [ ] Add tracebacks to logging
