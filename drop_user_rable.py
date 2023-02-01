from sqlalchemy import create_engine
from setup_db import db
from dao.model import user
from app import create_app
from config import Config

app = create_app(Config)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

with app.app_context():
    conn = engine.connect()
    conn.execute("DROP TABLE IF EXISTS user")
    conn.close()
    db.create_all()
