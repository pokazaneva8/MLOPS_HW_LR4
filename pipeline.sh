#!/bin/bash

poetry run python3 src/first_load.py \
    data/raw/extract_data.csv

poetry run python3 src/extract.py \
    extract_data.csv \
    data/external/extracted.csv

poetry run python3 src/modeling/transform.py \
    --data-path data/external/extracted.csv

poetry run python3 src/modeling/train.py \
    --data-path data/processed/preprocessed_data.csv \
    --params config/hyperparams.yaml