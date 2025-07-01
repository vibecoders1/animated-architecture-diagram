# animated-architecture-diagram
architecture-diagram python code

## run animated_derivatives_full.py
```
uv run manim -pql animated_derivatives_full.py VisualDerivativeRules
```

## run DistributedSystemDiagram.py
```
uv run manim -pql DistributedSystemDiagram.py DistributedSystemDiagram
```


## UV Commands

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