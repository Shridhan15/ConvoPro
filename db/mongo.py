import sys, os 
# ensure the project root is in sys.path so config can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 
from config.settings import Settings

from pymongo import MongoClient 

 
# Load settings
settings = Settings()

# Create MongoDB client
_client = MongoClient(settings.MONGO_DB_URL, tz_aware=True)

# ✅ Correct way to get database
_db = _client[settings.MONGO_DB_NAME]

def get_collection(name: str):
    """Return a MongoDB collection by name"""
    return _db[name]


# if __name__ == "__main__":
#     print("✅ Connected to DB:", settings.MONGO_DB_NAME)
#     print("📦 Collections available:", _db.list_collection_names())
