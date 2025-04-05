import os
from src.utils.enviroment_load import load_enviroment

ROOT_PATH = None
RESOURCE_PATH = None
IMAGE_PATH = None
ICON_PATH = None
FONT_PATH = None


env = {"DB_HOST": os.getenv("DB_HOST"),
    "DB_USER": os.getenv("DB_USER"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    "DB_DATABASE": os.getenv("DB_DATABASE"),
    "DB_PORT": os.getenv("DB_PORT") }


def init(root_path):
    load_enviroment()
    global ROOT_PATH, RESOURCE_PATH, IMAGE_PATH, ICON_PATH, FONT_PATH
    ROOT_PATH = root_path
    RESOURCE_PATH = os.path.join(ROOT_PATH, 'res')
    IMAGE_PATH = os.path.join(RESOURCE_PATH, 'images')
    ICON_PATH = os.path.join(RESOURCE_PATH, 'icons')
    FONT_PATH = os.path.join(RESOURCE_PATH, 'fonts')
    env["DB_HOST"] = os.getenv("DB_HOST")
    env["DB_USER"] = os.getenv("DB_USER")
    env["DB_PASSWORD"] = os.getenv("DB_PASSWORD")
    env["DB_DATABASE"] = os.getenv("DB_DATABASE")
    env["DB_PORT"] = os.getenv("DB_PORT") 