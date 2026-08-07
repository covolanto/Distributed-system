"""Activity 4: Communication Delay"""

from cluster import BullyCluster


def run():
    print("\n--- Activity 4: Communication Delay ---")
    results = {}

    for delay_ms in (10, 100, 500):
        cluster = BullyCluster(5, delay_ms=delay_ms)
        # elect from node 1: it has the most higher nodes to message,
        # so the delay's effect is actually visible
        _, elapsed, messages = cluster.elect(1)
        results[delay_ms] = (elapsed, messages)
        print(f"delay={delay_ms}ms -> election time={elapsed:.3f}s, messages={messages}")

    return results
