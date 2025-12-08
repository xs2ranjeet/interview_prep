'''
442. News Aggregator System | Design a High-Scale Event News Feed System
Medium
https://enginebogie.com/public/question/news-aggregator-system-design-a-high-scale-event-news-feed-system/442
Design a scalable news aggregator system that collects news articles from multiple external sources, categorizes them, and serves them to end users via a web or mobile interface.

Core Requirements:
News Collection:

Ingest articles from various sources such as:

RSS feeds
Public APIs
Web scraping (if required)
Handle deduplication of identical or near-identical articles.

Normalize data into a common format (title, content, author, publishedAt, source, etc.)

Categorization & Tagging:

Automatically classify articles into categories (e.g., Politics, Sports, Technology).
Support tagging (e.g., India, Elections, AI) for better filtering.
Articles may belong to multiple categories/tags.
User Experience:

Support endpoints like:

/latest
/trending
/category/:name
/search?q=...
Sort by recency, popularity, or relevance.

User Personalization (Optional for follow-up):

Allow users to follow categories or keywords.
Personalize the feed based on user interests and reading behavior.
Scalability & Performance:

System must handle:

High ingestion rate (hundreds of articles per minute).
High read traffic (millions of daily active users).
Use caching and efficient storage formats to optimize performance.

Follow-up Questions:
How would you handle breaking news updates?
How would you implement spam detection or content moderation?
How would you monitor and retry failed ingestions?

'''