from fastapi import FastAPI
from server.env import AmbulanceEnv
from server.models import AmbulanceAction
import uvicorn

app = FastAPI()
env = AmbulanceEnv()

@app.get("/")
def home():
    return {"message": "Ambulance RL Environment Running"}

@app.post("/reset")
def reset():
    return env.reset()

@app.get("/state")
def state():
    return env.state()

@app.post("/step")
def step(action: dict):
    act = AmbulanceAction(**action)
    return env.step(act)

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
