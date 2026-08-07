# Cristian's Algorithm - Clock Synchronization

A real client-server implementation of **Cristian's Algorithm**, where
clients synchronize their clocks with a time server over TCP sockets.

## Overview

Cristian's Algorithm is a simple way for a client to estimate the true
time from a trusted server, correcting for network round-trip delay:

1. Client records `t0`, then sends a request to the server.
2. Server responds with its current time, `t1`.
3. Client records `t2` the moment the response arrives.
4. Round-trip time: `RTT = t2 - t0`.
5. Estimated true time when the reply arrived: `t1 + RTT / 2`
   (assumes the request and response each took half the round trip).
6. Adjustment needed: `estimated_time - t2`.
7. Uncertainty in that estimate: `RTT / 2` (the "error bound").

## Files

- `time_server.py` - The time server (run first)
- `time_client.py` - Client that syncs its clock against the server (run second)

## Requirements

- Python 3.7+
- No external dependencies — just the standard library (`socket`, `argparse`,
  `threading`, `statistics`).

## How to run

### Step 1: Start the server

```bash
python time_server.py
```

### Step 2: Start a client (in a separate terminal)

```bash
python time_client.py --id 1
```

The server must be running before the client connects, or you'll get a
`Connection refused` error.

## Commands

### Server

```bash
# Default port 8000
python time_server.py

# Different port
python time_server.py --port 8001

# Simulate processing delay (adds to RTT, useful for testing accuracy under load)
python time_server.py --delay 100
```

| Flag | Default | Description |
|------|---------|-------------|
| `--host` | `localhost` | Host to bind to |
| `--port` | `8000` | Port to listen on |
| `--delay` | `0` | Simulated processing delay in ms before responding |

### Client

```bash
# Basic client
python time_client.py --id 1

# Different port (must match the server)
python time_client.py --id 1 --port 8001

# Sync every 5 seconds instead of every 2
python time_client.py --id 1 --interval 5

# Run for 60 seconds instead of the default 30
python time_client.py --id 1 --duration 60
```

| Flag | Default | Description |
|------|---------|-------------|
| `--id` | *(required)* | Client identifier, shown in output |
| `--host` | `localhost` | Server host to connect to |
| `--port` | `8000` | Server port |
| `--interval` | `2.0` | Seconds between sync attempts |
| `--duration` | `30.0` | Total time to keep syncing, in seconds |

## Expected output

### Server

```
🕐 TIME SERVER RUNNING
   Host: localhost
   Port: 8000
   Press Ctrl+C to stop

   [Request #1] from 127.0.0.1:54321 → 1722976545.123456
   [Request #2] from 127.0.0.1:54322 → 1722976546.234567
```

### Client

```
👤 CLIENT 1 INITIALIZED
   Server: localhost:8000
   Initial local time: 1722976540.123456
🔄 CLIENT 1 - Continuous Sync
   Interval: 2.0s, Duration: 30.0s
--------------------------------------------------
   [1] Sync #1: RTT=1.2ms, Adj=2.3ms, Error=0.5ms
   [1] Sync #2: RTT=1.1ms, Adj=1.8ms, Error=0.3ms

📊 CLIENT 1 - SUMMARY
==================================================
Total syncs: 15
Error Statistics:
  Min: 0.12ms
  Max: 1.34ms
  Avg: 0.45ms
RTT Statistics:
  Min: 0.80ms
  Max: 2.10ms
  Avg: 1.20ms
```

## Common issues

| Issue | Solution |
|-------|----------|
| **Port 8000 in use** | `python time_server.py --port 8001` (and match `--port` on the client) |
| **Connection refused** | Start the server *before* the client |
| **Sync fails repeatedly** | Check the server is still running and the host/port match on both sides |
| **High error values** | Try `--delay 0` on the server, or check for network/firewall interference |

## How it works

1. Client sends a small `"TIME"` request to the server.
2. Server responds with its current clock reading.
3. Client measures the round-trip time (RTT) and estimates the server's
   time at the moment the response arrived (`server_time + RTT/2`).
4. Client computes the adjustment needed to align with that estimate, and
   an error bound of `RTT/2` (Cristian's algorithm's own uncertainty).
5. This repeats every `--interval` seconds until `--duration` elapses, then
   prints min/max/avg statistics for both RTT and error.

The server is threaded, so it can handle multiple clients syncing at once —
try running several `time_client.py --id N` instances against the same
server in different terminals.
