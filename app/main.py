from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from app.personas import create_demo_personas
from app.simulate import run_simulation

app = FastAPI(title="TinyTroupe POC")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/personas/demo")
def personas_demo():
    personas_data = create_demo_personas()
    return personas_data


class SimulateRequest(BaseModel):
    topic: str = "Say hello"
    steps: int = 2


@app.post("/simulate/echo")
def simulate_echo(request: SimulateRequest):
    result = run_simulation(request.topic, request.steps)
    return result
