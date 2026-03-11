"""
Seed script - inserts 30 grid-scale BESS units (all >= 1000 kWh) into the batteries table.
Run from your project root with the venv active:
    python seed_batteries.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Battery

batteries = [
    # Tesla Megapack 2 XL
    Battery(name="Tesla Megapack 2 XL - Unit 01", capacity_kwh=4000.0, max_charge_rate_kw=1900.0, max_discharge_rate_kw=1900.0, efficiency=0.94, is_active=True),
    Battery(name="Tesla Megapack 2 XL - Unit 02", capacity_kwh=4000.0, max_charge_rate_kw=1900.0, max_discharge_rate_kw=1900.0, efficiency=0.94, is_active=True),
    Battery(name="Tesla Megapack 2 XL - Unit 03", capacity_kwh=4000.0, max_charge_rate_kw=1900.0, max_discharge_rate_kw=1900.0, efficiency=0.94, is_active=False),

    # Fluence Gridstack Pro
    Battery(name="Fluence Gridstack Pro - Unit 01", capacity_kwh=2000.0, max_charge_rate_kw=1000.0, max_discharge_rate_kw=1000.0, efficiency=0.95, is_active=True),
    Battery(name="Fluence Gridstack Pro - Unit 02", capacity_kwh=2000.0, max_charge_rate_kw=1000.0, max_discharge_rate_kw=1000.0, efficiency=0.95, is_active=True),
    Battery(name="Fluence Gridstack Pro - Unit 03", capacity_kwh=2000.0, max_charge_rate_kw=1000.0, max_discharge_rate_kw=1000.0, efficiency=0.93, is_active=False),

    # Sungrow PowerTitan ST2236UX
    Battery(name="Sungrow PowerTitan ST2236UX - Unit 01", capacity_kwh=2236.0, max_charge_rate_kw=1000.0, max_discharge_rate_kw=1000.0, efficiency=0.95, is_active=True),
    Battery(name="Sungrow PowerTitan ST2236UX - Unit 02", capacity_kwh=2236.0, max_charge_rate_kw=1000.0, max_discharge_rate_kw=1000.0, efficiency=0.95, is_active=True),
    Battery(name="Sungrow PowerTitan ST2236UX - Unit 03", capacity_kwh=2236.0, max_charge_rate_kw=1000.0, max_discharge_rate_kw=1000.0, efficiency=0.95, is_active=True),

    # CATL EnerC
    Battery(name="CATL EnerC - Unit 01", capacity_kwh=1500.0, max_charge_rate_kw=750.0, max_discharge_rate_kw=750.0, efficiency=0.95, is_active=True),
    Battery(name="CATL EnerC - Unit 02", capacity_kwh=1500.0, max_charge_rate_kw=750.0, max_discharge_rate_kw=750.0, efficiency=0.95, is_active=True),
    Battery(name="CATL EnerC - Unit 03", capacity_kwh=1500.0, max_charge_rate_kw=750.0, max_discharge_rate_kw=750.0, efficiency=0.95, is_active=False),

    # GE Reservoir
    Battery(name="GE Reservoir - Unit 01", capacity_kwh=4000.0, max_charge_rate_kw=2000.0, max_discharge_rate_kw=2000.0, efficiency=0.94, is_active=True),
    Battery(name="GE Reservoir - Unit 02", capacity_kwh=4000.0, max_charge_rate_kw=2000.0, max_discharge_rate_kw=2000.0, efficiency=0.94, is_active=True),
    Battery(name="GE Reservoir - Unit 03", capacity_kwh=4000.0, max_charge_rate_kw=2000.0, max_discharge_rate_kw=2000.0, efficiency=0.94, is_active=False),

    # Wartsila GridSolv Quantum
    Battery(name="Wartsila GridSolv Quantum - Unit 01", capacity_kwh=1120.0, max_charge_rate_kw=560.0, max_discharge_rate_kw=560.0, efficiency=0.96, is_active=True),
    Battery(name="Wartsila GridSolv Quantum - Unit 02", capacity_kwh=1120.0, max_charge_rate_kw=560.0, max_discharge_rate_kw=560.0, efficiency=0.96, is_active=True),
    Battery(name="Wartsila GridSolv Quantum - Unit 03", capacity_kwh=1120.0, max_charge_rate_kw=560.0, max_discharge_rate_kw=560.0, efficiency=0.94, is_active=False),

    # Stem Athena
    Battery(name="Stem Athena - Unit 01", capacity_kwh=1000.0, max_charge_rate_kw=500.0, max_discharge_rate_kw=500.0, efficiency=0.95, is_active=True),
    Battery(name="Stem Athena - Unit 02", capacity_kwh=1000.0, max_charge_rate_kw=500.0, max_discharge_rate_kw=500.0, efficiency=0.94, is_active=True),
    Battery(name="Stem Athena - Unit 03", capacity_kwh=1000.0, max_charge_rate_kw=500.0, max_discharge_rate_kw=500.0, efficiency=0.94, is_active=True),

    # Hitachi Energy Gridscale G2
    Battery(name="Hitachi Energy Gridscale G2 - Unit 01", capacity_kwh=1200.0, max_charge_rate_kw=600.0, max_discharge_rate_kw=600.0, efficiency=0.94, is_active=True),
    Battery(name="Hitachi Energy Gridscale G2 - Unit 02", capacity_kwh=1200.0, max_charge_rate_kw=600.0, max_discharge_rate_kw=600.0, efficiency=0.94, is_active=True),
    Battery(name="Hitachi Energy Gridscale G2 - Unit 03", capacity_kwh=1200.0, max_charge_rate_kw=600.0, max_discharge_rate_kw=600.0, efficiency=0.93, is_active=False),

    # BYD MC-Cube
    Battery(name="BYD MC-Cube - Unit 01", capacity_kwh=1672.0, max_charge_rate_kw=836.0, max_discharge_rate_kw=836.0, efficiency=0.96, is_active=True),
    Battery(name="BYD MC-Cube - Unit 02", capacity_kwh=1672.0, max_charge_rate_kw=836.0, max_discharge_rate_kw=836.0, efficiency=0.96, is_active=True),
    Battery(name="BYD MC-Cube - Unit 03", capacity_kwh=1672.0, max_charge_rate_kw=836.0, max_discharge_rate_kw=836.0, efficiency=0.96, is_active=True),

    # Powin Stack750
    Battery(name="Powin Stack750 - Unit 01", capacity_kwh=3000.0, max_charge_rate_kw=1500.0, max_discharge_rate_kw=1500.0, efficiency=0.95, is_active=True),
    Battery(name="Powin Stack750 - Unit 02", capacity_kwh=3000.0, max_charge_rate_kw=1500.0, max_discharge_rate_kw=1500.0, efficiency=0.95, is_active=True),

    # Nidec ESS Freqmax
    Battery(name="Nidec ESS Freqmax - Unit 01", capacity_kwh=1800.0, max_charge_rate_kw=900.0, max_discharge_rate_kw=900.0, efficiency=0.95, is_active=True),
    Battery(name="Nidec ESS Freqmax - Unit 02", capacity_kwh=1800.0, max_charge_rate_kw=900.0, max_discharge_rate_kw=900.0, efficiency=0.95, is_active=False),
]


def seed():
    db = SessionLocal()
    try:
        deleted = db.query(Battery).delete()
        db.commit()
        if deleted > 0:
            print(f"🗑️  Cleared {deleted} existing battery record(s).")
        db.add_all(batteries)
        db.commit()
        print(f"✅ Successfully inserted {len(batteries)} battery records.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
