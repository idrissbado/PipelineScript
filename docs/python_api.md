# Python API

```python
from pipelinescript import Pipeline

pipeline = (Pipeline()
    .load("data.csv")
    .clean_missing()
    .encode()
    .split(0.8, target="label")
    .train("xgboost")
    .evaluate())

result = pipeline.run()
```
