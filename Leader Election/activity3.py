"""Activity 3: Dynamic Node Leave"""

from cluster import BullyCluster


def run():
    print("\n--- Activity 3: Dynamic Node Leave ---")
    cluster = BullyCluster(5)
    print("start:", cluster.status())

    for leaving_id in (3, 5):
        cluster.kill(leaving_id)
        print(f"node {leaving_id} left:", cluster.status())

    return cluster
