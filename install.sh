#!/bin/bash

git clone https://github.com/hugo-andriamaromanana/dorsal-ronflex.git

cd dorsal-ronflex

poetry install

poetry build

pip install dist/dorsal_ronflex-0.1.0.tar.gz

cd ..

rm -rf dorsal-ronflex

echo "Installation completed. You can now use the 'dorsal-ronflex' command to run the program."