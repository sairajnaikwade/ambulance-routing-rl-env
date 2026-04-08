import os
import asyncio
from openai import OpenAI
from server.env import AmbulanceEnv
from server.models import AmbulanceAction

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def log_start(model_name):
    print(f"[START] task=easy env=ambulance model={model_name}")

def log_step(step, action, reward, done, error=None):
    error_str = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_str}")

def log_end(success, steps, rewards):
    r = ",".join(f"{x:.2f}" for x in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={r}")

async def main():
    env = AmbulanceEnv()
    obs = env.reset()
    rewards = []
    log_start(MODEL_NAME)

    for step in range(1, 20):
        alive_patients = [i for i, p in enumerate(obs.patients) if p.time_left > 0]

        if alive_patients:
            critical_patient_id = max(
                alive_patients,
                key=lambda i: obs.patients[i].severity
            )
            patient = obs.patients[critical_patient_id]

            if obs.ambulance_location == patient.location:
                action = AmbulanceAction(target_type="hospital", target_id=0)
                action_str = "go_hospital"
            else:
                action = AmbulanceAction(target_type="patient", target_id=critical_patient_id)
                action_str = "go_patient"
        else:
            action = AmbulanceAction(target_type="hospital", target_id=0)
            action_str = "idle"

        result = env.step(action)
        obs = result["observation"]
        reward = result["reward"]
        done = result["done"]

        rewards.append(reward)
        log_step(step, action_str, reward, done)

        if done:
            break

    success = sum(rewards) > 0.0
    log_end(success, step, rewards)

if __name__ == "__main__":
    asyncio.run(main())
