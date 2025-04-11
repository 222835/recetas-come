import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from src.database.connector import Base


