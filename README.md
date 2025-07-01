# animated-architecture-diagram
architecture-diagram python code

```
uv init venv
uv venv
source .venv/bin/activate
deactivate
uv pip install -r requirements.txt 

uv pip list
uv pip freeze
uv pip check

uv pip sync requirements.txt
uv pip compile requirements.in --constraint constraints.txt

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