import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    """
    A configuration class that retrieves environment variables and stores configuration settings.
    """

    # API and Model configurations
    HOSTED_BASE_URL = os.getenv("HOSTED_BASE_URL")
    HOSTED_API_KEY = os.getenv("HOSTED_API_KEY")
    LOCAL_BASE_URL = os.getenv("LOCAL_BASE_URL")

    # Available models
    AVAILABLE_MODELS = [
        "meta-llama/Meta-Llama-3.2-11B-Vision-Instruct-Turbo",
    ]