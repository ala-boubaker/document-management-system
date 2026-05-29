from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "document_management_system")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=30000
)

db = client[DB_NAME]
collection = db[COLLECTION_NAME]

documents = [
    {
        "document_id": "DOC001",
        "title": "MongoDB Basics",
        "content": "Introduction to MongoDB and NoSQL databases.",
        "category": "Technology",
        "author": "Alaeddine"
    },
    {
        "document_id": "DOC002",
        "title": "Python Programming Guide",
        "content": "Comprehensive guide for Python development.",
        "category": "Technology",
        "author": "John Smith"
    },
    {
        "document_id": "DOC003",
        "title": "University Research Proposal",
        "content": "Research proposal for Big Data applications.",
        "category": "Research",
        "author": "Sarah Johnson"
    },
    {
        "document_id": "DOC004",
        "title": "Machine Learning Notes",
        "content": "Important machine learning concepts and algorithms.",
        "category": "AI",
        "author": "Michael Brown"
    },
    {
        "document_id": "DOC005",
        "title": "Database Design Report",
        "content": "Normalization and database schema design.",
        "category": "Database",
        "author": "David Wilson"
    },
    {
        "document_id": "DOC006",
        "title": "Big Data Assignment",
        "content": "Analysis of large-scale datasets.",
        "category": "Education",
        "author": "Emma Davis"
    },
    {
        "document_id": "DOC007",
        "title": "Flask Web Development",
        "content": "Building web applications with Flask.",
        "category": "Technology",
        "author": "Robert Miller"
    },
    {
        "document_id": "DOC008",
        "title": "NoSQL Concepts",
        "content": "Comparison between SQL and NoSQL databases.",
        "category": "Database",
        "author": "Lisa Anderson"
    },
    {
        "document_id": "DOC009",
        "title": "Artificial Intelligence Trends",
        "content": "Current trends in AI and deep learning.",
        "category": "AI",
        "author": "James Taylor"
    },
    {
        "document_id": "DOC010",
        "title": "Cloud Computing Overview",
        "content": "Introduction to cloud platforms and services.",
        "category": "Technology",
        "author": "Sophia Moore"
    }
]

collection.insert_many(documents)

print("10 test documents inserted successfully!")