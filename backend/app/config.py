import os
from dotenv import load_dotenv

# Load environment variables from .env file explicitly
load_dotenv()

class Config:
    """Centralized configuration for the JEE Predictor Backend."""
    
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    
    # Dynamic resolving for deployment
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Point data path securely. Default points to `../../data` locally, 
    # but in lambda it could point to `/var/task/data` or `/tmp`
    DATA_PATH = os.getenv("DATA_PATH", os.path.join(BASE_DIR, "..", "..", "data"))
    
    # Optional S3 settings for massive datasets that exceed lambda 250MB size limit
    S3_BUCKET = os.getenv("S3_BUCKET", None)
    S3_DATA_KEY = os.getenv("S3_DATA_KEY", None)
    
    # CORS logic
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

# Expose globally
config = Config()
