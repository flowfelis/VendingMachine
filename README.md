# Vending Machine

An API for a vending machine, allowing users with a “seller” role to add, update or remove products,
while users with a “buyer” role can deposit coins into the machine and make purchases.
Vending machine only accepts 5, 10, 20, 50 and 100 cent coins.

## Requirements
Python 3.9+

## Tech Stack
* Python
* FastAPI
* SqlAlchemy
* PyTest
* SqlLite3

## How to start and use
* create virtualenv
* `pip install -r requirements.txt`
* `uvicorn app.main:app`
* go to *localhost:8000/docs* on your browser
* You can see the API documentation
* You can fire requests and try out endpoints
* Also for detailed API documentation, visit *localhost:8000/redoc*