from ..extensions import db
from datetime import datetime

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=True)  # Для текстового содержимого поста
    created_at = db.Column(db.DateTime, default=datetime.now())
    image_url = db.Column(db.String(2048), nullable=True)
    video_url = db.Column(db.String(2048), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
