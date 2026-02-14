'''
https://open.substack.com/pub/programmingappliedai/p/lld-design-a-connection-pool-with?utm_campaign=post-expanded-share&utm_medium=web

LLD: Design a Connection Pool with an Internal Request
It will focus on thread safety,fairness vs internal queue,boundness resources and clean separation of responsibilities

Functional
- Maintain a pool of reusable connections
- Allow concurrent threads to acquire connections
- Block or queue requests when no connection is available
- Support timeout on acquire
- Release connections back to the pool
- Validate connections before reuse
- Support graceful shutdown

Non-Functional
- Thread-safe
- Fair ordering (FIFO)
- High throughput
- No connection leaks
- Configurable pool size


class ConnectionPool

class PoolConnection -> DBConnection
'''