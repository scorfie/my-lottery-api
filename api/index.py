# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
# pyrefly: ignore [missing-import]
import srilanka_lottery as sl

app = FastAPI(
    title="Sri Lanka Lottery API",
    description="Unofficial API to fetch Sri Lankan lottery results from NLB and DLB.",
    version="1.0.0",
    docs_url="/api/docs",      # Re-routing documentation path for Vercel
    openapi_url="/api/openapi.json"
)

# Root path check
@app.get("/api")
def read_root():
    return {"status": "Sri Lanka Lottery API is running on Vercel"}

# --- DLB ENDPOINTS ---
@app.get("/api/dlb/lotteries")
def get_dlb_lotteries():
    try:
        return sl.scrape_dlb_lottery_names()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dlb/latest")
def get_dlb_latest(name: str, limit: int = 5):
    try:
        return sl.scrape_dlb_latest_results(name, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dlb/result")
def get_dlb_result(name: str, query: str):
    try:
        if query.isdigit():
            return sl.scrape_dlb_result(name, int(query))
        return sl.scrape_dlb_result(name, query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- NLB ENDPOINTS ---
@app.get("/api/nlb/lotteries")
def get_nlb_lotteries():
    try:
        result, _ = sl.scrape_nlb_active_lottery_names()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nlb/latest")
def get_nlb_latest(name: str, limit: int = 5):
    try:
        _, session = sl.scrape_nlb_active_lottery_names()
        return sl.scrape_nlb_latest_results(session, name, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nlb/result")
def get_nlb_result(name: str, query: str):
    try:
        if query.isdigit():
            return sl.scrape_nlb_result(name, int(query))
        return sl.scrape_nlb_result(name, query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))