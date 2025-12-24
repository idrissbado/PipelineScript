# Quick Start

## 1. Install

```bash
pip install pipelinescript
```

## 2. Create a `.psl` file

`my_pipeline.psl`

```text
load iris.csv
clean missing
encode
split 80/20 --target species
train random_forest
evaluate
export iris_model.pkl
```

## 3. Run

CLI:

```bash
pipelinescript run my_pipeline.psl
```

Python:

```python
from pipelinescript import run
result = run("my_pipeline.psl")
```
