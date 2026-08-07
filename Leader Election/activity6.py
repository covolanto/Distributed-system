"""Activity 6: Comparative Performance"""

import statistics

from cluster import BullyCluster


def run(sizes=(10,)):
    print("\n--- Activity 6: Comparative Performance ---")
    print(f"{'Nodes':<8}{'Avg Time(s)':<15}{'Avg Messages':<15}")

    results = {}
    for size in sizes:
        cluster = BullyCluster(size)
        times, messages = [], []

        for _ in range(3):
            if cluster.coordinator is None:
                break
            cluster.kill(cluster.coordinator)
            _, _, elapsed, msg_count = cluster.history[-1]
            times.append(elapsed)
            messages.append(msg_count)

        results[size] = (statistics.mean(times), statistics.mean(messages))
        print(f"{size:<8}{results[size][0]:<15.4f}{results[size][1]:<15.1f}")

    return results
