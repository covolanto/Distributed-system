"""Activity 1: Random Leader Failures"""

from cluster import BullyCluster


def run():
    print("\n--- Activity 1: Random Leader Failures ---")
    cluster = BullyCluster(5)
    print("start:", cluster.status())

    for _ in range(3):
        cluster.kill(cluster.coordinator)
        print("after failure:", cluster.status())

    return cluster
