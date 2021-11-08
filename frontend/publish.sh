#!/bin/bash

cd ../frontend || exit
rm -r dist/*
yarn build || exit

rm ../docs/index*.*
cp dist/index*.* ../docs/
