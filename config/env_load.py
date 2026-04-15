from dotenv import load_dotenv
import os

# Load once
load_dotenv()

MISTRAL_API_IP = os.getenv("MISTRAL_API_IP")
GOOGLE_SERVER_IP = os.getenv("GOOGLE_SERVER_IP")