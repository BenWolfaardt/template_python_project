# Template Python Project

A template making use of hexagonal architecture making use of a Pythonic config, SQLAlchemy PostgreSQL DB and FastAPI - the basics to get most projects up and running in no time.

## Todos

- [ ] Update pre-commit to use ruff - see FastApi tutorial  for Pull Request
- [ ] Update to SQLAlchemy v2
- [ ] See FastApi template repo for other tips and tricks
- [ ] pscopy parse in argument in pyprojects.toml
- [ ] init.sql to work with .env variable - see phoen stack overflow
- [ ] Have the repetitive part of my README in a gist?

## Local Setup and Configuration

Things to know to get up and running.

### Run Locally

Setting up our environment

```sh
  poetry install
  poetry shell
```

> `python -m src --env <choice>`

See `python -m src -h` for a list of choices.

### Run Tests

Then run dependencies with pytest:

```sh
  poetry run pytest tests/
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
