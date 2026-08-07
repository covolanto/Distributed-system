"""Activity 2: Dynamic Node Join"""

from cluster import BullyCluster


def run():
    print("\n--- Activity 2: Dynamic Node Join ---")
    cluster = BullyCluster(3)
    print("start:", cluster.status())

    for new_id in (4, 5):
        cluster.add_node(new_id)
        print(f"node {new_id} joined:", cluster.status())

    return cluster
