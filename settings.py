import os
from dotenv import load_dotenv


load_dotenv()
LOCATION_ZIP_CSVFILE = os.getenv('LOCATION_ZIP_CSVFILE')
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
SOLV_HEALTH_API_HOST = os.environ.get('SOLV_HEALTH_API_HOST')
