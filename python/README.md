# How to run this code?

## Setup Python environment

Setup a python virtual environment:

```sh
python3 -m venv .venv
source ./.venv/bin/active
pip install -r requirements.txt
```

## Run the tests

We run the program by running the tests and see if they pass:

```sh
pytest
```

## REST server and API calls

``` language=bash
flask --app calculator/app.py run
```

Send a curl call with a payload:

``` language=bash
curl -X POST http://127.0.0.1:5000/getTax \
  -H 'Content-Type: application/json' \
  -d '{"dates": [
    "2013-02-08 14:35:00", 
    "2013-02-08 15:29:00"
  ]}'
```

Another example:

``` language=bash
curl -X POST http://127.0.0.1:5000/getTax \
  -H 'Content-Type: application/json' \
  -d '{"dates": [
    "2013-02-08 09:01:00",
    "2013-02-08 10:02:00",
    "2013-02-08 11:03:00",
    "2013-02-08 12:04:00",
    "2013-02-08 14:05:00"
  ]}'
```
