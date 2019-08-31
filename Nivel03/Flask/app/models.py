from config import db


class Active(db.Model):
    __tablename__ = "actives"
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    country = db.Column(db.String(2), nullable=False)
    city = db.Column(db.String(30), nullable=False)
