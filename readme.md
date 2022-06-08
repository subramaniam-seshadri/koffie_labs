# Decode VIN App
This application decodes VIN, powered by the vPIC API and backed by a SQLite cache.

## Features

- Export cache of queried VIN details to a parquet file.
- Lookup VIN details from cache. If a vehicle was looked up earlier it will be saved in cache unless deleted.
- Remove VIN details from cache. 

## Tech

This project uses the following technologies :

- [FastAPI](https://fastapi.tiangolo.com/) - FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- [SQLite](https://www.sqlite.org/index.html) - SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
- [Python](https://www.python.org/) - Python is a programming language that lets you work more quickly and integrate your systems more effectively.

## Resources
- This application uses [vPIC API](https://vpic.nhtsa.dot.gov/api/) to query vehicle details based on VIN.

## Dependencies
Dependencies can be installed from the requirements.txt file
## Installation

This application requires Python 3.6+ to run.

Install the dependencies start the server.

```sh
cd koffie_labs
pip install requirements.txt
uvicorn main:app --reload
```

For production environments...

```sh
uvicorn main:app
```

## Testing
For testing, navigate to the 'tests' folder and run the tests with [pytest](https://docs.pytest.org/en/7.1.x/).
```sh
cd tests
pytest
```
## Author
Subramaniam Seshadri
subramaniam.seshadri@outlook.com