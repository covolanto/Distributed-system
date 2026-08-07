"""Activity 7: Priority-Based Election"""

import random

from cluster import BullyCluster


def run():
    print("\n--- Activity 7: Priority-Based Election ---")
    cluster = BullyCluster(5, use_priority=True)

    for n in cluster.nodes:
        n.priority = random.randint(1, 100)
    print("priorities:", {n.id: n.priority for n in cluster.nodes})

    winner, elapsed, messages = cluster.elect(2)
    print(f"winner=Node {winner} (priority={cluster.get(winner).priority}), time={elapsed:.4f}s")

    return cluster
