# PipelineScript

Human-readable ML pipeline language (DSL) for building, debugging, and visualizing machine learning pipelines.

- PyPI: https://pypi.org/project/pipelinescript/
- GitHub: https://github.com/idrissbado/PipelineScript

## Why PipelineScript?

- Write pipelines in plain text: `load`, `clean`, `encode`, `split`, `train`, `evaluate`
- Debug interactively with breakpoints and context inspection
- Visualize pipelines (ASCII or matplotlib)
- Use CLI or Python API

## Install

```bash
pip install pipelinescript
# Optional extras
pip install pipelinescript[full]
```

## Quick Example (DSL)

```text
load iris.csv
clean missing
encode
split 80/20 --target species
train random_forest
evaluate
export iris_model.pkl
```

## Quick Example (Python)

```python
from pipelinescript import Pipeline

result = (Pipeline()
    .load("data.csv")
    .clean_missing()
    .encode()
    .split(0.8, target="label")
    .train("xgboost")
    .evaluate()
    .run())
```

## Links

- Report issues: https://github.com/idrissbado/PipelineScript/issues
- Discussions: https://github.com/idrissbado/PipelineScript/discussions
