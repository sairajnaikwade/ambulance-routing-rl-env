import random
from .models import *

class AmbulanceEnv:
    def __init__(self):
        self.max_steps = 15
        self.steps = 0
        self.state_data = None
        self.current_patient = None

    def reset(self):
        self.state_data = AmbulanceState(
            ambulance_location=0,
            patients=[
                Patient(
                    location=random.randint(1, 10),
                    severity=random.uniform(0.6, 1.0),
                    time_left=random.randint(10, 18)
                ),
                Patient(
                    location=random.randint(1, 10),
                    severity=random.uniform(0.4, 0.9),
                    time_left=random.randint(12, 22)
                )
            ],
            hospitals=[
                Hospital(location=5, capacity=1),
                Hospital(location=10, capacity=2)
            ],
            traffic=[[abs(i - j) for j in range(11)] for i in range(11)]
        )
        self.steps = 0
        self.current_patient = None
        return self._get_obs()

    def _get_obs(self):
        return AmbulanceObservation(
            ambulance_location=self.state_data.ambulance_location,
            patients=self.state_data.patients,
            hospitals=self.state_data.hospitals
        )

    def step(self, action: AmbulanceAction):
        self.steps += 1
        reward = 0.0

        #  Move to patient
        if action.target_type == "patient":
            p = self.state_data.patients[action.target_id]
            travel = self.state_data.traffic[self.state_data.ambulance_location][p.location]

            self.state_data.ambulance_location = p.location
            p.time_left -= travel

            if p.time_left > 0:
                self.current_patient = p
                reward += 0.6 * p.severity
            else:
                reward -= 0.1

        # 🏥 Move to hospital
        elif action.target_type == "hospital":
            h = self.state_data.hospitals[action.target_id]
            travel = self.state_data.traffic[self.state_data.ambulance_location][h.location]

            self.state_data.ambulance_location = h.location

            if self.current_patient and self.current_patient.time_left > 0 and h.capacity > 0:
                reward += 1.4 * self.current_patient.severity
                h.capacity -= 1
                self.current_patient = None
            else:
                reward -= 0.2

        # ⏱️ lighter time penalty
        reward -= 0.01 * self.steps

        # clamp
        reward = max(min(reward, 1.0), -1.0)

        done = self.steps >= self.max_steps

        return {
            "observation": self._get_obs(),
            "reward": reward,
            "done": done,
            "info": {}
        }

    def state(self):
        return self.state_data