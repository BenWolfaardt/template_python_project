# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2024-08-22

### Added

- `tryceratops`  in Ruff config
- Schemas for all requests and responses in OpenAPI docs

### Fixed

- Request ID query parameter in the API

### Changed

- Logging config to be part of the settings adapter
- Overall logging of the API
- Improved exception handling in the SQL store


## [1.2.0] - 2024-04-01

### Added

- `FastAPI` server (run as a thread)
- CRUD interactors

### Fixed

- Custom exception logic

### Changed

- Contents of `Data`
- `Data` from a `@dataclass` to a `BaseModel` (simplifying `_data_row_to_data`)
- Config printing now pretty prints in `json`


## [1.1.0] - 2024-03-13

### Added

- `PostgreSQL` DB
- Improved `Dockerfile`
  - Use of layered caching
  - Parsed in `.env` variables
- Run migrations script
- `.dockerignore`

### Fixed

- Improved the `YAML` to `Python` settings
- Logger implementation
- Hexagonal architecture for `settings.py`


## [1.0.1] - 2023-08-19

### Fixed

- `pyproject.toml` project name


## [1.0.0] - 2023-08-19

### Added

- Simple `pre-commit`
- Dockerise project
- Logging
- Pythonic settings
