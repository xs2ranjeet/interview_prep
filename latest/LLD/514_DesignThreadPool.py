'''
514. Design Thread-Safe Connection Pool
https://enginebogie.com/public/question/design-thread-safe-connection-pool/514
Hard
Design a thread-safe connection pool for managing database connections in a multi-threaded environment. A connection pool is a crucial component for improving the performance and resource utilization of database connections, particularly in applications where multiple threads may require concurrent database access. Your design should ensure that multiple threads can safely acquire, use, and release database connections without conflicts or contention.

Design Requirements:

Connection Pool Management:

Create and maintain a pool of database connections.
Limit the maximum number of connections in the pool to prevent resource exhaustion.
Thread Safety:

Implement mechanisms to make the connection pool thread-safe.
Ensure that multiple threads can safely request and release connections without data corruption or resource leaks.
Connection Reuse:

Reuse connections to minimize the overhead of creating and destroying connections for each database request.
Connection Validation:

Validate connections before handing them to requesting threads to ensure they are in a usable state.
Timeouts and Wait Strategies:

Handle cases where all connections in the pool are in use, including timeouts and wait strategies for thread contention.
Resource Cleanup:

Ensure that connections are properly released and resources are cleaned up when connections are closed or returned to the pool.
Compatibility:

The connection pool should be compatible with different database systems and connection libraries.
Example:

// Example of using a thread-safe connection pool in Java
ConnectionPool pool = new ConnectionPool("jdbc:mysql://localhost:3306/mydb", "username", "password");
try (Connection connection = pool.getConnection()) {
    // Use the connection for database operations
    // ...
} catch (SQLException e) {
    // Handle exceptions
} finally {
    pool.releaseConnection(connection);
}
'''