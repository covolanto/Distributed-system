"""
Bully Algorithm - Node
A single process in the cluster.
"""


class Node:
    def __init__(self, node_id, priority=None):
        self.id = node_id
        self.alive = True
        # priority defaults to the node's own id, so plain Bully
        # (highest id wins) and priority-based Bully share one code path
        self.priority = priority if priority is not None else node_id
        self.messages_sent = 0

    def __repr__(self):
        return f"Node({self.id}, alive={self.alive}, priority={self.priority})"
