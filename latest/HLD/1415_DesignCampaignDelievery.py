'''
1415. Marketing/Campaign Email/Notifications Delivery System for Large Scale Marketing
https://enginebogie.com/interview/experience/salesforce-principal-member-of-technical-staff/407
High-Level Design (HLD)System DesignBackendHigh ScalabilityHigh AvailabilityDistributed SystemNotification SystemDatabasesMessage Queue
Medium
Design a system that sends campaign email to users when a sale or event is live. A single campaign may need to send up to 100k emails. Over time the system may run millions of campaigns. The system must deliver emails reliably and report success or failure for each message.

Requirements:
Accept campaign definitions that include sender details email content a recipient list send window and throttling rules.
Deliver up to 100k emails per campaign while respecting provider rate limits and mailbox provider rules.
Support millions of campaigns over time while keeping storage and cost reasonable.
Report per message status delivered bounced deferred or blocked and expose simple metrics for campaign health.
Handle retries backoff and bounce handling without blocking other campaigns.
Allow scheduling campaigns for future times and support pause cancel and resume.
Keep delivery scalable and maintain good inbox placement for marketing emails.
'''