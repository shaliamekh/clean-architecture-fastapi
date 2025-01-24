# Clean Architecture on Python with FastAPI

<a href="https://github.com/shaliamekh/clean-architecture-fastapi/actions?query=workflow%3A+branch%3Amain++" target="_blank">
    <img src="https://github.com/shaliamekh/clean-architecture-fastapi/actions/workflows/ci.yaml/badge.svg?branch=main&event=push" alt="CI">
</a>

This repository serves as an illustrative example of implementing Clean Architecture 
principles in a Python application using FastAPI. It accompanies the Medium article
[“Clean Architecture with Python”](https://medium.com/@shaliamekh/clean-architecture-with-python-d62712fd8d4f).

## Local setup

Create a virtual environment and install dependencies

```shell
  python3 -m venv venv && venv/bin/pip install -r src/requirements.txt
```
Launch a mongodb instance using Docker
```shell
  docker run --rm -d -p 27017:27017 --name=mongo-auctions mongo:8.0.4
```

Run tests
```shell
  venv/bin/pytest src/tests
```

Start FastAPI application

```shell
  venv/bin/fastapi dev src/drivers/rest/main.py
```

## Clean up

Remove the mongodb container
```shell
  docker rm -f mongo-auctions
```
