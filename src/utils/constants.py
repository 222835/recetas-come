import os

ROOT_PATH = None
RESOURCE_PATH = None
IMAGE_PATH = None
ICON_PATH = None
FONT_PATH = None

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

def init(root_path):
    global ROOT_PATH, RESOURCE_PATH, IMAGE_PATH, ICON_PATH, FONT_PATH
    ROOT_PATH = root_path
    RESOURCE_PATH = os.path.join(ROOT_PATH, 'res')
    IMAGE_PATH = os.path.join(RESOURCE_PATH, 'images')
    ICON_PATH = os.path.join(RESOURCE_PATH, 'icons')
    FONT_PATH = os.path.join(RESOURCE_PATH, 'fonts')