import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

async def test_connection():
    load_dotenv()
    uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB_NAME")
    
    print(f"🔍 Testing MongoDB connection...")
    print(f"📊 Database: {db_name}")
    
    try:
        client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        # Force connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # List databases
        db_list = await client.list_database_names()
        print(f"📚 Available databases: {db_list}")
        
        client.close()
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())