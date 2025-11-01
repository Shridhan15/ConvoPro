import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any

import sys, os   
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 


from pymongo import DESCENDING
from db.mongo import get_collection

# Access the "conversations" collection from MongoDB
conversations = get_collection("conversations")

# Create an index on 'last_interacted' to speed up recent conversations queries
conversations.create_index([("last_interacted", DESCENDING)])


# ---------- Helper Functions ----------

def now_utc():
    """Return the current UTC time with timezone info."""
    return datetime.now(timezone.utc)


def create_new_conversation_id() -> str:
    """Generate a unique conversation ID using UUID4."""
    return str(uuid.uuid4())


# ---------- Core Conversation Services ----------

def create_new_conversation(
    title: Optional[str] = None,
    role: Optional[str] = None,
    content: Optional[str] = None
) -> str:
    """
    Create a new conversation document in MongoDB.

    Args:
        title (str, optional): Title for the conversation. Defaults to 'Untitled Conversation'.
        role (str, optional): Role of the first message (e.g., 'user', 'assistant').
        content (str, optional): Content of the first message.

    Returns:
        str: The generated conversation ID.
    """
    conv_id = create_new_conversation_id()
    ts = now_utc()

    # Base conversation document
    doc = {
        "_id": conv_id,
        "title": title or "Untitled Conversation",
        "messages": [],
        "last_interacted": ts,
    }

    # If an initial message is provided, add it to the conversation
    if role and content:
        doc["messages"].append({"role": role, "content": content, "ts": ts})

    # Insert conversation into MongoDB
    conversations.insert_one(doc)
    return conv_id


def add_message(conv_id: str, role: str, content: str) -> bool:
    """
    Add a message to an existing conversation.

    Args:
        conv_id (str): ID of the conversation.
        role (str): Message sender's role ('user' or 'assistant').
        content (str): Message content.

    Returns:
        bool: True if the conversation was found and updated, False otherwise.
    """
    ts = now_utc()

    # Update conversation by adding message and refreshing 'last_interacted' timestamp
    res = conversations.update_one(
        {"_id": conv_id},
        {
            "$push": {"messages": {"role": role, "content": content, "ts": ts}},
            "$set": {"last_interacted": ts},
        },
    )

    # matched_count == 1 means the conversation existed and was updated
    return res.matched_count == 1


def get_conversation(conv_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a specific conversation by its ID and update its last interaction timestamp.

    Args:
        conv_id (str): ID of the conversation to retrieve.

    Returns:
        dict | None: The conversation document, or None if not found.
    """
    ts = now_utc()

    # Find and update the conversation’s last_interacted time
    doc = conversations.find_one_and_update(
        {"_id": conv_id},
        {"$set": {"last_interacted": ts}},
        return_document=True,
    )
    return doc


def get_all_conversations() -> Dict[str, str]:
    """
    Retrieve all conversations sorted by most recent interaction.

    Returns:
        dict: Mapping of conversation IDs to their titles.
    """
    # Fetch only '_id' and 'title' fields, sorted by latest activity
    cursor = conversations.find({}, {"title": 1}).sort("last_interacted", DESCENDING)

    # Convert cursor to a dictionary of {id: title}
    return {doc["_id"]: doc["title"] for doc in cursor}



# --- Example usage ---

# For a new conversation (with the first message):
# conv_id = create_new_conversation(title="Intro to Deep Learning", role="user", content="What is DL?")
# add_message(conv_id, "assistant", "Answer for DL query")
# print(get_conversation(conv_id))
# print(get_all_conversations())
#
# # For an existing conversation:
# add_message(conv_id, "user", "What is ML?")
# add_message(conv_id, "assistant", "Answer for ML query")
# print(get_conversation(conv_id))
# print(get_all_conversations())
#
# # # For a new conversation (with a different title and first message):
# conv_id2 = create_new_conversation(title="Intro to Generative AI", role="user", content="What is Generative AI?")
# add_message(conv_id2, "assistant", "Answer for Generative AI query")
# print(get_conversation(conv_id2))
# print(get_all_conversations())