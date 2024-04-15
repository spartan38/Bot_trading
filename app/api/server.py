from process.comparative.process_stocks import ProcessStock
from process.portfolio.portfolio import get_portfolio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import API_HOST, API_PORT, EXCHANGES

app = FastAPI()

origins = [
    "http://localhost",
    f"http://{API_HOST}:{API_PORT}",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

@app.get("/get_portfolio_data")
def get_portfolio_data():
    portfolio = get_portfolio(EXCHANGES)
    return {
        "portfolio": portfolio,
        "status": 200
    }

@app.get("/test_comparative")
def get_portfolio_data():
    data = ProcessStock.run()
    return {
        "data": data,
        "status": 200
    }