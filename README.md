# 🚑 Ambulance Routing RL Environment

## 📌 Overview

This project implements a **real-world Reinforcement Learning environment** for emergency ambulance routing using the OpenEnv framework.

The agent must decide:

* Which patient to pick
* When to go to hospital
* How to maximize survival reward under time constraints

---

## ⚙️ Features

* OpenEnv-compatible environment (`step()`, `reset()`, `state()`)
* Dynamic patients with severity & time limits
* Traffic-based travel cost
* Reward optimization strategy
* FastAPI deployment for API access
* Dockerized for Hugging Face Spaces

---

## 🧠 Environment Logic

* 🚑 Ambulance starts at location `0`
* 🧍 Patients have:

  * Location
  * Severity (priority)
  * Time left
* 🏥 Hospitals have limited capacity
* 🚦 Traffic affects travel time

---

## 🎯 Objective

Maximize total reward by:

* Saving critical patients
* Minimizing delays
* Efficient routing decisions

---

## ▶️ API Endpoints

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

## 🐳 Run Locally

```bash
docker build -t ambulance-env .
docker run -p 7860:7860 ambulance-env
```

---

## 📦 Requirements

* Python 3.10
* FastAPI
* Uvicorn
* OpenEnv

---

## 👨‍💻 Team KHX_BS
Sairaj Naikwade
Bhushan Korde

---
