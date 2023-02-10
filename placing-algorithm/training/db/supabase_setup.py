from supabase import Client, create_client
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Root level configuration for project
    """

    URL = os.getenv("URL")
    KEY = os.getenv("KEY")


class SupabaseDB:
    """
    class instance for database connection to supabase
    :str: url: configuration for database url for data inside supafast project
    :str: key: configuration for database secret key for authentication
    :object: supabase: Supabase instance for connection to database environment
    """

    url: str = Config.URL
    key: str = Config.KEY
    supabase: Client = create_client(url, key)


if __name__ == "__main__":
    db = SupabaseDB()
    print(db.supabase)

    # Add a dummy element
    db.supabase.table("test").insert({"name": "test", "data": 2}).execute()



