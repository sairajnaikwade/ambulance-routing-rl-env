def easy_grader(env):
    state = env.state()
    alive = [p for p in state.patients if p.time_left > 0]
    score = len(alive) / len(state.patients)
    # Clamp strictly between 0 and 1
    return max(0.01, min(score, 0.99))


def medium_grader(env):
    state = env.state()
    total_time = sum(p.time_left for p in state.patients)
    max_possible = 22 * len(state.patients)
    score = total_time / max_possible
    return max(0.01, min(score, 0.99))


def hard_grader(env):
    state = env.state()
    saved = sum(1 for p in state.patients if p.time_left > 0)
    severity_sum = sum(p.severity for p in state.patients if p.time_left > 0)
    total_severity = sum(p.severity for p in state.patients)
    if total_severity == 0:
        return 0.01
    score = severity_sum / total_severity
    return max(0.01, min(score, 0.99))
