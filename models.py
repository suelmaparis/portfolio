from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(100), nullable=False, default='default-client.jpg')
