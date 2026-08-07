# Bully Algorithm - Leader Election Simulation

A short, from-scratch simulation of the **Bully Algorithm** for distributed
leader election, split into small files, covering 7 practical activities.

## What it does

In the Bully Algorithm, the alive node with the **highest ID** (or highest
priority, in the optimized variant) is always the coordinator. When a node
notices the coordinator is gone, it starts an election:

- It "messages" every higher-ranked alive node.
- If a higher node exists, that node takes over instead.
- If no higher node is alive, the node that started the election declares
  itself coordinator and "broadcasts" that to everyone else.

## File structure

```
bully_fresh/
├── node.py          # Node class: id, alive flag, priority, message counter
├── cluster.py        # BullyCluster class: manages nodes, runs elections
├── activity1.py      # Random Leader Failures
├── activity2.py       # Dynamic Node Join
├── activity3.py       # Dynamic Node Leave
├── activity4.py       # Communication Delay
├── activity5.py       # Process Crash Recovery
├── activity6.py       # Comparative Performance
├── activity7.py       # Priority-Based Election
├── main.py            # Entry point — runs all 7 activities in order
└── README.md          # This file
```

## Requirements

- Python 3.7+
- No external packages — only the standard library (`time`, `random`,
  `statistics`).

## How to run

All files import each other by module name (e.g. `from cluster import
BullyCluster`), so you must run from **inside** the `bully_fresh/` folder.

### Run everything (all 7 activities)

```bash
cd bully_fresh
python main.py
```

(use `python3 main.py` if that's how Python 3 is aliased on your system)

Prints all 7 activities back-to-back, no prompts — done in under a second.

### Run a single activity

```bash
cd bully_fresh
python -c "import activity1; activity1.run()"
```

Swap `activity1` for any of: `activity2`, `activity3`, `activity4`,
`activity5`, `activity6`, `activity7`.

### Use the cluster directly

```python
from cluster import BullyCluster

c = BullyCluster(5)
c.kill(c.coordinator)   # triggers an election automatically
print(c.coordinator)    # next highest alive node
print(c.status())       # "1, 2, 3, 4*, 5(dead)"
```

## Activities covered

| # | Activity | What it tests |
|---|----------|----------------|
| 1 | Random Leader Failures | Repeated coordinator crashes and re-elections |
| 2 | Dynamic Node Join | New nodes joining and taking over as highest ID |
| 3 | Dynamic Node Leave | Nodes leaving, including the coordinator |
| 4 | Communication Delay | Election time scaling with 10ms / 100ms / 500ms delay |
| 5 | Process Crash Recovery | A node crashing mid-election |
| 6 | Comparative Performance | Election cost for a given cluster size (10 nodes by default) |
| 7 | Priority-Based Election | Coordinator chosen by priority instead of raw ID |

## Notes

- `BullyCluster.kill(id)` always restarts the election from the **highest
  still-alive node**, never from the node that just died — this avoids a
  dead node ever "winning" an election.
- `status()` prints one compact line per state change (`*` = coordinator,
  `(dead)` = dead) instead of a full table, to keep output short.
- Activity 6 tests a single cluster size (10 nodes) by default. To compare
  multiple sizes, call `activity6.run(sizes=(5, 10, 20))` instead of the
  default `run()`.
