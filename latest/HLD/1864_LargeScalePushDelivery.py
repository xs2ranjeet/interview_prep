'''
1864. Large Scale Push Notification Delivery System
High-Level Design (HLD)System DesignBackendDistributed SystemDatabasesNotification SystemMessage Queue
Hard
Design a system similar to APNS or FCM that can deliver billions of push notifications to mobile devices across the world. The system should be able to handle both high priority notifications such as transactional alerts and low priority notifications such as marketing messages.

Key points to think about:

How the system will manage connections with millions of devices that are always coming online and going offline
How push delivery differs from a pull based model and when to use each
How to ensure that high priority messages are delivered quickly while low priority messages do not block the system
How to design storage for queued notifications including the choice of database or data store
How the system will handle retries in case a device is not reachable
How to design the architecture to scale to billions of notifications per day while keeping latency low
How to monitor delivery status and provide feedback to clients about success or failure of notification delivery
'''