from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import engine, SessionLocal
from models import Base, Asset, AssetType, StateOfCharge
from llm_service import ask_grid_question_stream

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Grid Asset Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Asset Grid Manager API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/assetslist")
def get_assets(db: Session = Depends(get_db)):
    
    # Subquery — most recent state_of_charge timestamp per asset
    latest_soc = (
        db.query(
            StateOfCharge.asset_id,
            func.max(StateOfCharge.timestamp).label("latest_ts")
        )
        .group_by(StateOfCharge.asset_id)
        .subquery()
    )

    # Join assets → latest state_of_charge row
    results = (
        db.query(Asset, StateOfCharge)
        .join(latest_soc, Asset.id == latest_soc.c.asset_id)
        .join(StateOfCharge, (StateOfCharge.asset_id == Asset.id) &
                             (StateOfCharge.timestamp == latest_soc.c.latest_ts))
        #.filter(Asset.asset_type == AssetType.BATTERY)
        .all()
    )

    return [
        {
            "id":                   asset.id,
            "asset_type":            asset.asset_type,
            "eic_code":             asset.eic_code,
            "name":                 asset.name,
            "max_capacity_mwh":     asset.max_capacity_mwh,
            "max_charge_rate_mw":   asset.max_charge_rate_mw,
            "max_discharge_rate_mw": asset.max_discharge_rate_mw,
            "reactive_power_capacity_mvar": asset.reactive_power_capacity_mvar,
            "efficiency":           asset.efficiency,
            # Live data from latest StateOfCharge
            "soc_id":               soc.id,
            "operational_mode":     soc.operational_mode.value if soc.operational_mode else None,
            "asset_status":         soc.asset_status.value if soc.asset_status else None,
            "energy_mwh":           soc.energy_mwh,
            "power_mw":             soc.power_mw,
            "reactive_power_mvar":  soc.reactive_power_mvar,
            "power_factor":         soc.power_factor,
            "last_updated":         soc.timestamp.isoformat(),
        }
        for asset, soc in results
    ]



@app.get("/assets/summary")
def get_asset_summary(db: Session = Depends(get_db)):

    # Subquery — most recent state_of_charge timestamp per asset
    latest_soc = (
        db.query(
            StateOfCharge.asset_id,
            func.max(StateOfCharge.timestamp).label("latest_ts")
        )
        .group_by(StateOfCharge.asset_id)
        .subquery()
    )

    # Join assets → latest state_of_charge row
    results = (
        db.query(Asset, StateOfCharge)
        .join(latest_soc, Asset.id == latest_soc.c.asset_id)
        .join(StateOfCharge, (StateOfCharge.asset_id == Asset.id) &
                             (StateOfCharge.timestamp == latest_soc.c.latest_ts))
        .all()
    )

    # Aggregate in Python across the latest rows
    total_power_mw        = sum(soc.power_mw or 0.0 for _, soc in results)
    total_energy_mwh      = sum(soc.energy_mwh or 0.0 for _, soc in results)
    total_reactive_mvar   = sum(soc.reactive_power_mvar or 0.0 for _, soc in results)

    # Break down by asset type
    by_type = {}
    for asset, soc in results:
        t = asset.asset_type.value
        if t not in by_type:
            by_type[t] = {"power_mw": 0.0, "energy_mwh": 0.0, "asset_count": 0}
        by_type[t]["power_mw"]    += soc.power_mw or 0.0
        by_type[t]["energy_mwh"]  += soc.energy_mwh or 0.0
        by_type[t]["asset_count"] += 1

    return {
        "total_power_mw":      round(total_power_mw, 3),
        "total_energy_mwh":    round(total_energy_mwh, 3),
        "total_reactive_mvar": round(total_reactive_mvar, 3),
        "by_asset_type": {
            "all": {
                "power_mw":    round(total_power_mw, 3),
                "energy_mwh":  round(total_energy_mwh, 3),
                "asset_count": len(results),
            },
            **{
                k: {
                    "power_mw":    round(v["power_mw"], 3),
                    "energy_mwh":  round(v["energy_mwh"], 3),
                    "asset_count": v["asset_count"],
                }
                for k, v in by_type.items()
            }
        }
    }







@app.post("/llm/ask")
def ask_llm(question: str):
    return StreamingResponse(
        ask_grid_question_stream(question),
        media_type="text/plain"
    )

