from fastapi import FastAPI

app = FastAPI(title="AvenueCDC")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
