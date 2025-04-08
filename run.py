from flask import Flask
from extensions import db, migrate

from routes import register_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)



from models import Hero, Power, HeroPower

register_routes(app)

if __name__ == '__main__':
    app.run(port=5555)
