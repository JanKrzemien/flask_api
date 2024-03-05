class Config:
    TESTING = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///devices.db"
