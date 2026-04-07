def easy_grader(env):
    return 1.0 if env.state().patients[0].time_left > 0 else 0.0


def medium_grader(env):
    return sum([p.time_left for p in env.state().patients]) / 20


def hard_grader(env):
    saved = sum([1 for p in env.state().patients if p.time_left > 0])
    return saved / len(env.state().patients)