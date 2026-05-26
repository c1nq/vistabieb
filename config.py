import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://cypher@localhost/vistabieb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
