"""Activity 5: Process Crash Recovery"""

from cluster import BullyCluster


def run():
    print("\n--- Activity 5: Crash During Election ---")
    cluster = BullyCluster(5)

    # node 4 crashes right as node 3 starts an election
    cluster.get(4).alive = False
    winner, elapsed, messages = cluster.elect(3)

    print(f"election survives the crash -> winner=Node {winner}, time={elapsed:.4f}s")
    print("status:", cluster.status())

    return cluster
