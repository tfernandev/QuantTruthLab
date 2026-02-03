from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import backtest, market, discovery

app = FastAPI(title="Quant Terminal API", version="2.0.0")

# CORS (Allow Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(market.router, prefix="/api/market", tags=["Market Data"])
app.include_router(discovery.router, prefix="/api/discovery", tags=["Discovery"])
app.include_router(backtest.router, prefix="/api/backtest", tags=["Backtest"])

@app.get("/")
def read_root():
    return {"status": "ok", "system": "Quant Platform Ready"}
