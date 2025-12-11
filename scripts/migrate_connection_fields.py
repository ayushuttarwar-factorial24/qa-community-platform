"""
Migration Script: Update Connection Fields

Migrates existing profiles from 'connected_with' to new structure:
- connections_sent: List of user_ids this user sent connection requests to
- connections_received: List of user_ids who connected with this user

For existing data, we'll distribute connected_with into both fields
to maintain existing connections.
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()


async def migrate_connection_fields():
    """
    Migrates all profiles to use new connection structure.
    
    Strategy:
    1. For each profile with 'connected_with' field:
       - Copy to 'connections_sent' (they initiated these)
       - Add empty 'connections_received' if not exists
    2. Calculate connections_received by checking who has this user in their connections_sent
    3. Remove old 'connected_with' field
    """
    
    # Connect to MongoDB
    mongodb_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB_NAME", "qa_community")
    
    if not mongodb_uri:
        print("❌ MONGODB_URI not found in environment variables")
        return
    
    client = AsyncIOMotorClient(mongodb_uri)
    db = client[db_name]
    collection = db.profiles
    
    print(f"🔗 Connected to MongoDB: {db_name}")
    
    try:
        # Get all profiles
        all_profiles = await collection.find({}).to_list(length=None)
        print(f"📊 Found {len(all_profiles)} total profiles")
        
        if not all_profiles:
            print("✅ No profiles to migrate")
            return
        
        # Step 1: Add new fields and copy connected_with to connections_sent
        migrated_count = 0
        for profile in all_profiles:
            user_id = profile.get('user_id')
            connected_with = profile.get('connected_with', [])
            
            # Skip if already migrated
            if 'connections_sent' in profile and 'connections_received' in profile:
                print(f"⏭️  Skipping {profile.get('name')} - already migrated")
                continue
            
            # Add new fields
            update_data = {}
            
            # Copy connected_with to connections_sent if exists
            if connected_with:
                update_data['connections_sent'] = connected_with
            else:
                update_data['connections_sent'] = []
            
            # Initialize connections_received as empty (will be calculated next)
            update_data['connections_received'] = []
            
            await collection.update_one(
                {'user_id': user_id},
                {'$set': update_data}
            )
            
            migrated_count += 1
            print(f"✅ Migrated {profile.get('name')} - {len(connected_with)} connections sent")
        
        print(f"\n📝 Phase 1 Complete: {migrated_count} profiles migrated")
        
        # Step 2: Calculate connections_received
        # For each profile, find who has them in their connections_sent
        print("\n📝 Phase 2: Calculating connections_received...")
        
        all_profiles = await collection.find({}).to_list(length=None)
        
        for profile in all_profiles:
            user_id = profile.get('user_id')
            
            # Find all profiles that have this user_id in their connections_sent
            received_from = await collection.find(
                {'connections_sent': user_id}
            ).to_list(length=None)
            
            received_ids = [p['user_id'] for p in received_from]
            
            if received_ids:
                await collection.update_one(
                    {'user_id': user_id},
                    {'$set': {'connections_received': received_ids}}
                )
                print(f"✅ {profile.get('name')} received {len(received_ids)} connections")
        
        print(f"\n✅ Phase 2 Complete: connections_received calculated")
        
        # Step 3: Remove old connected_with field
        print("\n📝 Phase 3: Removing old 'connected_with' field...")
        
        result = await collection.update_many(
            {'connected_with': {'$exists': True}},
            {'$unset': {'connected_with': ''}}
        )
        
        print(f"✅ Removed 'connected_with' from {result.modified_count} profiles")
        
        # Summary
        print("\n" + "="*50)
        print("✅ MIGRATION COMPLETE!")
        print("="*50)
        
        final_profiles = await collection.find({}).to_list(length=None)
        
        total_sent = sum(len(p.get('connections_sent', [])) for p in final_profiles)
        total_received = sum(len(p.get('connections_received', [])) for p in final_profiles)
        
        print(f"📊 Total profiles: {len(final_profiles)}")
        print(f"📤 Total connections sent: {total_sent}")
        print(f"📥 Total connections received: {total_received}")
        print(f"✅ All profiles now use new connection structure")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        client.close()
        print("\n🔌 Database connection closed")


if __name__ == "__main__":
    print("="*50)
    print("CONNECTION FIELDS MIGRATION SCRIPT")
    print("="*50)
    print("\nThis script will:")
    print("1. Copy 'connected_with' to 'connections_sent'")
    print("2. Calculate 'connections_received' for each profile")
    print("3. Remove old 'connected_with' field")
    print("\nPress Ctrl+C to cancel...")
    
    try:
        input("\nPress Enter to continue...\n")
        asyncio.run(migrate_connection_fields())
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled by user")
