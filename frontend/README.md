### github pages for Bahn API history data

Visit at [defgsus.github.io/bahn-api-history/](https://defgsus.github.io/bahn-api-history/)

To run the site for development call 

`frontend/run-server.sh` 

within the `frontend` directory.

It will start an additional file server in the `/docs` directory using python.

To compile run 

`publish.sh`

It will copy `dist/index.html` to `../docs/index.html` and the js and css files
to `../docs/js/` as they seem to not be delivered when placed directly into `../docs/`.
