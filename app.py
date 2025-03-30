from flask import Flask
from dotenv import load_dotenv
from extensions.database import db, jwt
from api.routes import register_routes
import os
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
jwt.init_app(app)


register_routes(app)

with app.app_context():
    db.create_all() 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
