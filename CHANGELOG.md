# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Hexagonal architecturefor `settings.py`


## [1.0.1] - 2023-08-19

### Fixed

- `pyproject.toml` project name


## [1.0.0] - 2023-08-19

### Added

- Simple `pre-commit`
- Dockerise project
- Logging
- Pythonic settings
