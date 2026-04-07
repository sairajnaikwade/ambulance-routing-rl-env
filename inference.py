import asyncio
from server.env import AmbulanceEnv
from server.models import AmbulanceAction

def log_start():
    print("[START] task=easy env=ambulance model=smart-agent")

def log_step(step, action, reward, done):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

def log_end(success, steps, score, rewards):
    r = ",".join(f"{x:.2f}" for x in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={r}")

async def main():
    env = AmbulanceEnv()
    obs = env.reset()

    rewards = []
    log_start()

    for step in range(1, 20):

        # 🔍 find alive patients
        alive_patients = [i for i, p in enumerate(obs.patients) if p.time_left > 0]

        if alive_patients:
            critical_patient_id = max(
                alive_patients,
                key=lambda i: obs.patients[i].severity
            )

            patient = obs.patients[critical_patient_id]

            # decision logic
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

    score = sum(rewards)
    success = score > 0.0  # balanced success

    log_end(success, step, score, rewards)

if __name__ == "__main__":
    asyncio.run(main())