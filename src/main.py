from typing import Optional

import pigpio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.config import load_local_config
from src.discovery import ACInventory
from src.ir_engine import DaikinIREngine, DaikinState

config = load_local_config()
pigpio_config = config.get("pigpio", {})
api_config = config.get("api", {})

app = FastAPI(title="Daikin AutoRemote API")
inventory = ACInventory()

pi = pigpio.pi(
    str(pigpio_config.get("host", "localhost")),
    int(pigpio_config.get("port", 8888)),
)


class ACCommand(BaseModel):
    power: Optional[bool] = None
    temp: Optional[int] = None
    mode: Optional[str] = None
    fan: Optional[str] = None


@app.get("/units")
def list_units():
    return inventory.units


@app.post("/units/{unit_id}/control")
def control_unit(unit_id: int, cmd: ACCommand):
    unit = inventory.get_unit(unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    if not pi.connected:
        raise HTTPException(status_code=500, detail="pigpio daemon not reachable")

    engine = DaikinIREngine(pi, unit["gpio"])
    state = DaikinState()

    if cmd.power is not None:
        state.power = cmd.power
    if cmd.temp is not None:
        state.temp = cmd.temp
    if cmd.mode is not None:
        state.mode = cmd.mode
    if cmd.fan is not None:
        state.fan = cmd.fan

    try:
        engine.send_command(state.get_frames())
        return {"status": "success", "sent": cmd}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.on_event("shutdown")
def shutdown_event():
    if pi.connected:
        pi.stop()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=str(api_config.get("bind_host", "127.0.0.1")),
        port=int(api_config.get("port", 8000)),
    )
