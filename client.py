from server.env import AmbulanceEnv

env = AmbulanceEnv()

def reset():
    return env.reset()

def step(action):
    return env.step(action)

def state():
    return env.state()