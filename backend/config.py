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
DEBUG = os.environ.get('DEBUG', False)
EDITOR_USERNAME = os.environ.get('EDITOR_USERNAME', 'editor')
EDITOR_PASSWORD_HASH = os.environ.get('EDITOR_PASSWORD_HASH', 'pbkdf2:sha256:600000$0R5mehSek6l3xXgW$c5c7e16cf6fd4b7313093e3aac9b261dcd70eaaadd2262ec1c4ae56de79a976c')
MEDSENGER_KEY = os.environ.get('MEDSENGER_KEY', '')
MEDSENGER_HOST = os.environ.get('VUE_APP_MEDSENGER_HOST', '')
MEDSENGER_LOGIN = os.environ.get('MEDSENGER_LOGIN', False)
STORAGE_PATH = os.environ.get('STORAGE_PATH', '')