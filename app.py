from flask import Flask
from db_models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
