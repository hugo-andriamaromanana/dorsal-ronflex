#!/bin/bash

git clone https://github.com/hugo-andriamaromanana/dorsal-ronflex.git

cd dorsal-ronflex

poetry install

poetry build

pip install dist/dorsal_ronflex-0.1.0.tar.gz