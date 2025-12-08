'''
https://enginebogie.com/interview/experience/salesforce-senior-member-of-technical-staff/381
1794. Design a Scalable Cloud-Based Property Listing Platform
High-Level Design (HLD)System DesignHigh ScalabilityHigh AvailabilityData ConsistencyMicroservicesDistributed System
Medium
A property dealer currently has a traditional on-premise website where brokers and merchants can list properties. Each property listing includes photos, location, and basic details. The company now wants to migrate to a cloud-based system that is more scalable, faster, and secure.

Key concerns:

Data consistency must be maintained.
High performance is required for large volumes of listings and searches.
System must handle future growth without major rework.
You are required to design the complete system considering both functional and non-functional requirements.

Functional Requirements:

Users can browse property listings.
Users can search for properties based on filters like location, price range, and property type.
Users can login, register, and logout securely.
On the property listing page, properties must be grouped by merchant name.
Non-Functional Requirements:

High scalability to handle peak traffic.
Strong security for user data and merchant details.
Consistent and up-to-date property information.
Fast response times for browsing and searching.
Constraints to Consider:

Millions of property listings.
Tens of thousands of concurrent users.
Search results must be returned in under 300 ms.
Images should load quickly even under heavy load.
System must be resilient to partial failures.
'''