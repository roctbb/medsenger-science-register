from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

JS_HOST = os.environ.get('VUE_APP_MAINHOST')
DB_HOST = os.environ.get('DB_HOST')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_PORT = os.environ.get('DB_PORT')
DB_LOGIN = os.environ.get('DB_LOGIN')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
APP_SECRET = os.environ.get('APP_SECRET')
PORT = os.environ.get('API_PORT')
