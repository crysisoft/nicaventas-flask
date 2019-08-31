from config import db


class Active(db.Model):
    __tablename__ = "actives"
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    country = db.Column(db.String(2), nullable=False)
    city = db.Column(db.String(30), nullable=False)


class Descripcion(db.Model):
    __tablename__ = "descripciones"
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(7), unique=True, nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)


class Regla(db.Model):
    __tablename__ = "reglas"
    id_regla = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(60), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    sku = db.Column(db.String(50), db.ForeignKey('descripciones.sku'), nullable=False)
    min_condition = db.Column(db.Integer, nullable=False)
    max_condition = db.Column(db.Integer, nullable=False)
    variation = db.Column(db.Float, nullable=False)
