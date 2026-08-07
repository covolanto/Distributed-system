"""
Bully Algorithm - Cluster
Manages a set of nodes and runs elections between them.
"""

import time

from node import Node


class BullyCluster:
    def __init__(self, n, delay_ms=0, use_priority=False):
        self.nodes = [Node(i) for i in range(1, n + 1)]
        self.delay = delay_ms / 1000.0
        self.use_priority = use_priority
        self.history = []  # list of (old_coordinator, new_coordinator, seconds, messages)
        self.coordinator = self._winner(self.alive_nodes())

    def _rank(self, node):
        return node.priority if self.use_priority else node.id

    def _winner(self, candidates):
        return max(candidates, key=self._rank).id if candidates else None

    def alive_nodes(self):
        return [n for n in self.nodes if n.alive]

    def get(self, node_id):
        for n in self.nodes:
            if n.id == node_id:
                return n
        return None

    def add_node(self, node_id, priority=None):
        self.nodes.append(Node(node_id, priority))
        self.coordinator = self._winner(self.alive_nodes())

    def kill(self, node_id):
        """Mark a node dead. If it was the coordinator, trigger an election."""
        node = self.get(node_id)
        if node:
            node.alive = False

        if node_id == self.coordinator:
            alive = self.alive_nodes()
            if alive:
                starter = max(alive, key=self._rank)
                self.elect(starter.id)
            else:
                self.coordinator = None

    def elect(self, starter_id):
        """Run one election starting from starter_id."""
        start_time = time.time()
        starter = self.get(starter_id)
        messages = 0

        higher = [n for n in self.alive_nodes()
                  if n.id != starter_id and self._rank(n) > self._rank(starter)]

        for _ in higher:
            time.sleep(self.delay)
            messages += 1
        starter.messages_sent += messages

        winner = self._winner(higher) if higher else starter_id

        # winning coordinator broadcasts to everyone else alive
        messages += len([n for n in self.alive_nodes() if n.id != winner])

        elapsed = time.time() - start_time
        old_coordinator = self.coordinator
        self.coordinator = winner
        self.history.append((old_coordinator, winner, elapsed, messages))
        return winner, elapsed, messages

    def status(self):
        parts = []
        for n in self.nodes:
            label = str(n.id)
            if n.id == self.coordinator:
                label += "*"
            if not n.alive:
                label += "(dead)"
            parts.append(label)
        return ", ".join(parts)
