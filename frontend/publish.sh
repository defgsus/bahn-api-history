#!/bin/bash

cd ../frontend || exit
rm ../docs/*.js
rm ../docs/*.css
yarn build
