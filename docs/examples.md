# Examples

## Classification

```text
load titanic.csv
clean missing
encode
split 80/20 --target survived
train random_forest
evaluate
```

## Regression

```text
load housing.csv
clean outliers
select bedrooms bathrooms sqft price
scale
split 75/25 --target price
train linear
evaluate
```
