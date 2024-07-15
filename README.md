# dependencies
dependencies are listed in requirements.txt file, that is hopefuly up to date.

# running application
- create and activate virtualenv
- install dependencies from requirements.txt file
- inside project folder create file ./flaskr/config.py and add configuration. Example of configuration:
```
class Config:
    TESTING = False

class DevelopmentConfig(Config):
    SECRET_KEY='dev'
    TOKEN_EXPIRATION=3060
    ACCESS_TOKEN_TYPE='access_token'
    REFRESH_TOKEN_TYPE='refresh_token'
```

- initialize database with command 'flask --app flaskr init-db'
- run project with command 'flask --app flaskr run'