## Essentail uv commands

```
## To define project dependencies in a pyproject.toml file:
```
[project]
dependencies = [
  "httpx",
  "ruff>=0.3.0"
]
```

## To define optional dependencies in a pyproject.toml file:
```
[project.optional-dependencies]
cli = [
  "rich",
  "click",
]
```

## docs
https://docs.astral.sh/uv/pip/packages/#installing-a-package