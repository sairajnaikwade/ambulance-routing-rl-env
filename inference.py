import os
import asyncio
from openai import OpenAI
from server.env import AmbulanceEnv
from server.models import AmbulanceAction

# Required env vars per submission guidelines
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
    print(f"[START] task=easy env=ambulance model={model_name}", flush=True)

def log_step(step, action, reward, done, error=None):
    error_str = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_str}", flush=True)

def log_end(success, steps, rewards):
    r = ",".join(f"{x:.2f}" for x in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={r}", flush=True)

def get_llm_action(obs) -> tuple[str, int]:
    """Ask the LLM to decide the next action based on current observation."""
    
    patients_info = "\n".join([
        f"  Patient {i}: location={p.location}, severity={p.severity:.2f}, time_left={p.time_left:.1f}"
        for i, p in enumerate(obs.patients)
    ])
    hospitals_info = "\n".join([
        f"  Hospital {i}: location={h.location}, capacity={h.capacity}"
        for i, h in enumerate(obs.hospitals)
    ])

    prompt = f"""You are an ambulance dispatcher AI. Choose the best action.
Current State:
- Ambulance location: {obs.ambulance_location}
- Patients:
{patients_info}
- Hospitals:
{hospitals_info}
Rules:
- Pick up the most critical (highest severity) patient with time_left > 0
- After picking up a patient (ambulance at patient location), go to hospital
- If no patients alive, go to hospital
Respond with ONLY one of these formats (nothing else):
  patient <id>
  hospital <id>
Your decision:"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0.0
        )
        text = response.choices[0].message.content.strip().lower()
        
        parts = text.split()
        if len(parts) == 2:
            target_type = parts[0]   # "patient" or "hospital"
            target_id = int(parts[1])
            
            # Validate
            if target_type == "patient" and 0 <= target_id < len(obs.patients):
                return "patient", target_id
            elif target_type == "hospital" and 0 <= target_id < len(obs.hospitals):
                return "hospital", target_id
    except Exception:
        pass

    # Fallback: greedy rule if LLM fails
    alive = [i for i, p in enumerate(obs.patients) if p.time_left > 0]
    if alive:
        best = max(alive, key=lambda i: obs.patients[i].severity)
        if obs.ambulance_location == obs.patients[best].location:
            return "hospital", 0
        return "patient", best
    return "hospital", 0

async def main():
    env = AmbulanceEnv()
    obs = env.reset()

    rewards = []
    log_start(MODEL_NAME)

    last_step = 1
    for step in range(1, 20):
        last_step = step

        target_type, target_id = get_llm_action(obs)

        action = AmbulanceAction(target_type=target_type, target_id=target_id)
        action_str = f"{target_type}_{target_id}"

        result = env.step(action)

        obs = result["observation"]
        reward = result["reward"]
        done = result["done"]

        rewards.append(reward)
        log_step(step, action_str, reward, done)

        if done:
            break

    success = sum(rewards) > 0.0
    log_end(success, last_step, rewards)

if __name__ == "__main__":
    asyncio.run(main())
