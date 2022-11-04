import dotenv
import os

dotenv.load_dotenv()
envDict = os.environ

def env(key, default):
    return envDict.get(key, default)