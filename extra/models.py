from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "users.db"
class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True  

    def is_anonymous(self):
        return False
