import random


def simulate_load():
    return random.randint(20, 90)


def simulate_scaling(load=simulate_load, iterations=20):
    high = low = 0
    instances = 1
    history = []
    for step in range(iterations):
        cpu = load()
        high = high + 1 if cpu > 70 else 0
        low = low + 1 if cpu < 30 else 0
        action = "hold"
        if high == 3:
            instances += 1
            action, high = "start", 0
        elif low == 3 and instances > 1:
            instances -= 1
            action, low = "stop", 0
        history.append(
            {
                "step": step + 1,
                "cpu": cpu,
                "action": action,
                "instances": instances,
            }
        )
    return history


def demo(work, cloud):
    loads = iter([80, 81, 90, 25, 22, 20] + [50] * 14)
    return simulate_scaling(lambda: next(loads))
