class Config:
    TESTING = False

class DevelopmentConfig(Config):
    SECRET_KEY='dev'
    TOKEN_EXPIRATION=3060
    ACCESS_TOKEN_TYPE='access_token'
    REFRESH_TOKEN_TYPE='refresh_token'