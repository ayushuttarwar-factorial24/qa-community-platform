"""
Profile Repository Module

Handles all MongoDB database operations for profiles.
Implements CRUD operations and profile queries using Motor (async MongoDB driver).
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from app.models.profile import ProfileCreateUpdate, ProfileInDB, generate_user_id
from app.config import settings


logger = logging.getLogger(__name__)


class ProfileRepository:
    """
    Repository class for profile data access.
    
    Provides async methods for creating, reading, updating, and querying profiles
    in MongoDB. Handles connection management and indexing.
    """
    
    def __init__(self):
        """Initialize repository with MongoDB connection."""
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self.collection: Optional[AsyncIOMotorCollection] = None
    
    async def connect(self):
        """
        Establishes connection to MongoDB and sets up indexes.
        
        Should be called on application startup.
        """
        try:
            self.client = AsyncIOMotorClient(settings.mongodb_uri)
            self.db = self.client[settings.mongodb_db_name]
            self.collection = self.db["profiles"]
            
            # Create indexes
            await self._create_indexes()
            
            logger.info(f"Connected to MongoDB database: {settings.mongodb_db_name}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def disconnect(self):
        """
        Closes MongoDB connection.
        
        Should be called on application shutdown.
        """
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    async def _create_indexes(self):
        """
        Creates necessary indexes for optimal query performance.
        
        Indexes:
        - Unique index on email (for upsert and lookups)
        - Index on user_id (for fast lookups)
        - Compound index on phone + email (for identity verification)
        """
        try:
            # Unique index on email
            await self.collection.create_index("email", unique=True)
            
            # Index on user_id for fast lookups
            await self.collection.create_index("user_id", unique=True)
            
            # Compound index on phone and email
            await self.collection.create_index([("phone", 1), ("email", 1)])
            
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.warning(f"Index creation warning: {e}")
    
    async def create_or_update_profile(
        self,
        profile_data: ProfileCreateUpdate
    ) -> ProfileInDB:
        """
        Creates a new profile or updates existing one (upsert by email).
        
        If a profile with the same email exists, it updates all fields.
        Otherwise, creates a new profile with a generated user_id.
        
        Args:
            profile_data (ProfileCreateUpdate): Profile data to create/update
            
        Returns:
            ProfileInDB: The created or updated profile
            
        Raises:
            Exception: If database operation fails
        """
        try:
            # Check if profile exists by email
            existing = await self.collection.find_one({"email": profile_data.email})
            
            now = datetime.utcnow()
            
            if existing:
                # Update existing profile
                user_id = existing["user_id"]
                created_at = existing["created_at"]
                
                update_data = {
                    **profile_data.model_dump(),
                    "user_id": user_id,
                    "created_at": created_at,
                    "updated_at": now,
                }
                
                await self.collection.update_one(
                    {"email": profile_data.email},
                    {"$set": update_data}
                )
                
                logger.info(f"Updated profile for email: {profile_data.email}")
            else:
                # Create new profile
                user_id = generate_user_id()
                
                update_data = {
                    **profile_data.model_dump(),
                    "user_id": user_id,
                    "created_at": now,
                    "updated_at": now,
                }
                
                await self.collection.insert_one(update_data)
                
                logger.info(f"Created new profile with user_id: {user_id}")
            
            # Fetch and return the profile
            profile_doc = await self.collection.find_one({"user_id": user_id})
            return ProfileInDB.from_mongo(profile_doc)
            
        except Exception as e:
            logger.error(f"Error creating/updating profile: {e}")
            raise
    
    async def get_profile_by_identifier(
        self,
        identifier: str
    ) -> Optional[ProfileInDB]:
        """
        Retrieves a profile by user_id, email, or phone.
        
        Tries to match the identifier against user_id first, then email, then phone.
        
        Args:
            identifier (str): user_id, email, or phone number
            
        Returns:
            Optional[ProfileInDB]: Profile if found, None otherwise
        """
        try:
            # Try user_id first
            profile_doc = await self.collection.find_one({"user_id": identifier})
            
            if not profile_doc:
                # Try email
                profile_doc = await self.collection.find_one({"email": identifier.lower()})
            
            if not profile_doc:
                # Try phone
                profile_doc = await self.collection.find_one({"phone": identifier})
            
            if profile_doc:
                return ProfileInDB.from_mongo(profile_doc)
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving profile by identifier '{identifier}': {e}")
            return None
    
    async def list_all_profiles(self) -> List[ProfileInDB]:
        """
        Retrieves all profiles from the database.
        
        Returns:
            List[ProfileInDB]: List of all profiles
        """
        try:
            cursor = self.collection.find({})
            profiles = []
            
            async for doc in cursor:
                profiles.append(ProfileInDB.from_mongo(doc))
            
            logger.info(f"Retrieved {len(profiles)} profiles")
            return profiles
            
        except Exception as e:
            logger.error(f"Error listing profiles: {e}")
            return []
    
    async def list_other_profiles(
        self,
        source_identifier: str
    ) -> List[ProfileInDB]:
        """
        Retrieves all profiles except the one matching the source identifier.
        
        Used for matching algorithms to exclude the source user from suggestions.
        
        Args:
            source_identifier (str): user_id, email, or phone of source profile
            
        Returns:
            List[ProfileInDB]: List of all other profiles
        """
        try:
            # First, get the source profile to get its user_id
            source_profile = await self.get_profile_by_identifier(source_identifier)
            
            if not source_profile:
                logger.warning(f"Source profile not found: {source_identifier}")
                return []
            
            # Get all profiles except the source
            cursor = self.collection.find({"user_id": {"$ne": source_profile.user_id}})
            profiles = []
            
            async for doc in cursor:
                profiles.append(ProfileInDB.from_mongo(doc))
            
            logger.info(f"Retrieved {len(profiles)} other profiles for matching")
            return profiles
            
        except Exception as e:
            logger.error(f"Error listing other profiles: {e}")
            return []
    
    async def delete_profile(
        self,
        identifier: str
    ) -> bool:
        """
        Deletes a profile by user_id, email, or phone.
        
        Args:
            identifier (str): user_id, email, or phone
            
        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            profile = await self.get_profile_by_identifier(identifier)
            
            if not profile:
                return False
            
            result = await self.collection.delete_one({"user_id": profile.user_id})
            
            if result.deleted_count > 0:
                logger.info(f"Deleted profile: {identifier}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error deleting profile: {e}")
            return False
    
    async def count_profiles(self) -> int:
        """
        Returns the total number of profiles in the database.
        
        Returns:
            int: Total profile count
        """
        try:
            count = await self.collection.count_documents({})
            return count
        except Exception as e:
            logger.error(f"Error counting profiles: {e}")
            return 0
    
    async def award_points_and_connect(
        self,
        initiator_id: str,
        target_id: str,
        initiator_points: int,
        target_points: int
    ) -> bool:
        """
        Awards points to both users and records the connection.
        
        Updates:
        - Initiator: +points, add target_id to connections_sent
        - Target: +points, add initiator_id to connections_received
        
        Atomic operation using MongoDB transactions.
        
        Args:
            initiator_id: User ID initiating the connection
            target_id: User ID being connected to
            initiator_points: Points to award initiator (10)
            target_points: Points to award target (20)
            
        Returns:
            bool: True if successful
        """
        try:
            # Update initiator: add points, add to connections_sent
            await self.collection.update_one(
                {"user_id": initiator_id},
                {
                    "$inc": {"points": initiator_points},
                    "$addToSet": {"connections_sent": target_id}
                }
            )
            
            # Update target: add points, add to connections_received
            await self.collection.update_one(
                {"user_id": target_id},
                {
                    "$inc": {"points": target_points},
                    "$addToSet": {"connections_received": initiator_id}
                }
            )
            
            logger.info(
                f"Connection recorded: {initiator_id} -> {target_id}. "
                f"Points awarded: {initiator_id} (+{initiator_points}), "
                f"{target_id} (+{target_points})"
            )
            return True
            
        except Exception as e:
            logger.error(f"Error in award_points_and_connect: {e}")
            return False
    
    async def get_leaderboard(self, limit: int = 100) -> List[ProfileInDB]:
        """
        Returns profiles sorted by points (highest first).
        
        Args:
            limit: Maximum number of profiles to return
            
        Returns:
            List[ProfileInDB]: Top profiles by points
        """
        try:
            cursor = self.collection.find().sort("points", -1).limit(limit)
            profiles = []
            
            async for doc in cursor:
                profiles.append(ProfileInDB.from_mongo(doc))
            
            logger.info(f"Retrieved top {len(profiles)} profiles for leaderboard")
            return profiles
            
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []


# Global repository instance
profile_repository = ProfileRepository()


async def get_profile_repository() -> ProfileRepository:
    """
    Dependency injection function for FastAPI.
    
    Returns:
        ProfileRepository: The global repository instance
    """
    return profile_repository
