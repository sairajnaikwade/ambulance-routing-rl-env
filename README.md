---
title: "Ambulance Environment Server"
emoji: "🚑"
colorFrom: "blue"
colorTo: "green"
sdk: "docker"
pinned: false
app_port: 7860
tags: ["openenv", "reinforcement-learning", "simulation", "healthcare", "routing"]
---

# 🚑 Ambulance Routing Environment for OpenEnv

Real-world reinforcement learning environment for emergency ambulance routing and decision-making under time-critical constraints.

This environment simulates ambulance dispatch scenarios where an agent must prioritize patients, navigate efficiently, and maximize survival outcomes.

---

## 🧠 What This Environment Does

Traditional benchmarks test reasoning in static scenarios.

This environment tests **real decision-making** where:

* Actions have consequences (delays reduce survival)
* Time is limited and critical
* Resource allocation matters (hospital capacity)
* Sequential decisions affect future outcomes

---

## ⚙️ Core Features

* OpenEnv-compliant API (`step()`, `reset()`, `state()`)
* Real-world ambulance routing simulation
* Dynamic patients with:

  * Location
  * Severity (priority)
  * Time-to-live
* Hospital constraints (limited capacity)
* Traffic-based travel delays
* Reward shaping for RL training
* Dockerized deployment (Hugging Face Spaces ready)

---

## 🚑 Environment Logic

* Ambulance starts at base location
* Multiple patients appear dynamically
* Each patient has:

  * 📍 Location
  * ⚠️ Severity
  * ⏳ Time remaining
* Hospitals:

  * Limited capacity
  * Must receive patients in time

---

## 🎯 Objective

Maximize total reward by:

* Saving high-priority patients
* Minimizing travel time
* Avoiding delays
* Making optimal routing decisions

---

## 📡 API Endpoints

| Method | Endpoint | Description       |
| ------ | -------- | ----------------- |
| GET    | `/`      | Check API status  |
| GET    | `/reset` | Reset environment |
| GET    | `/state` | Get current state |
| POST   | `/step`  | Perform action    |

---

## 🧪 Example Action

```json
{
  "target_type": "patient",
  "target_id": 0
}
```

---

## 🧩 Tasks & Difficulty Levels

This environment includes **3 graded tasks**:

* Easy → Single patient, minimal traffic
* Medium → Multiple patients, moderate constraints
* Hard → High traffic, limited hospital capacity, time pressure

Each task includes:

* Deterministic grader
* Score range: 0.0 → 1.0
* Progressive difficulty

---

## 🏆 Reward Design

The reward function provides:

* Positive reward for saving patients
* Partial reward for progress
* Penalty for delays and wrong decisions
* Time-based decay

This ensures meaningful learning signals across the full trajectory.

---

## 🚀 Quick Start

### Local Run

docker build -t ambulance-env .
docker run -p 7860:7860 ambulance-env

---

### Inference

python inference.py

---

## 🌐 Live Deployment

Hugging Face Space:
https://bhushankorde-ambulance-env.hf.space

---

## 🧠 Inspiration

This project is inspired by simulation-based environments like CARLA, but focuses on healthcare logistics and emergency response systems.

It represents a lightweight, real-world RL environment for critical decision-making under uncertainty.

---

## 🔧 Tech Stack

* Python 3.10
* OpenEnv Framework
* FastAPI
* Docker
* Hugging Face Spaces

---

## 👨‍💻 Team KHX_BS

* Bhushan Korde
* Sairaj Naikwade

---

## 📄 License

MIT License
