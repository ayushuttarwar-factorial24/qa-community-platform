"""
MongoDB Database Connection Manager for Streamlit

Provides connection pooling and database operations for the Streamlit app.
Uses pymongo (sync) for simplicity with Streamlit's execution model.
"""

import streamlit as st
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_mongodb_uri() -> str:
    """
    Get MongoDB URI from Streamlit secrets or environment.
    
    Returns:
        str: MongoDB connection URI
    """
    # Try Streamlit secrets first (for deployment)
    try:
        return st.secrets["mongodb"]["uri"]
    except (KeyError, FileNotFoundError):
        pass
    
    # Fallback to environment variable (for local development)
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise ValueError("MongoDB URI not found in secrets or environment variables")
    
    return uri


def get_database_name() -> str:
    """
    Get database name from Streamlit secrets or environment.
    
    Returns:
        str: Database name
    """
    # Try Streamlit secrets first
    try:
        return st.secrets["mongodb"]["database"]
    except (KeyError, FileNotFoundError):
        pass
    
    # Fallback to environment variable or default
    import os
    from .constants import DATABASE_NAME
    return os.getenv("MONGODB_DB_NAME", DATABASE_NAME)


@st.cache_resource
def get_mongo_client() -> MongoClient:
    """
    Creates and caches MongoDB client connection.
    
    Uses Streamlit's cache_resource to maintain connection across reruns.
    Connection pool is managed by pymongo.
    
    Returns:
        MongoClient: MongoDB client instance
    """
    uri = get_mongodb_uri()
    
    # Create client with connection pooling
    client = MongoClient(
        uri,
        maxPoolSize=10,
        minPoolSize=1,
        maxIdleTimeMS=30000,
        connectTimeoutMS=5000,
        serverSelectionTimeoutMS=5000
    )
    
    # Test connection
    try:
        client.admin.command('ping')
        logger.info("MongoDB connection established successfully")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
    
    return client


def get_database() -> Database:
    """
    Get database instance.
    
    Returns:
        Database: MongoDB database
    """
    client = get_mongo_client()
    db_name = get_database_name()
    return client[db_name]


def get_profiles_collection() -> Collection:
    """
    Get profiles collection.
    
    Returns:
        Collection: Profiles collection
    """
    db = get_database()
    return db.profiles


def close_connection():
    """Close MongoDB connection (for cleanup)."""
    try:
        client = get_mongo_client()
        client.close()
        logger.info("MongoDB connection closed")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")
