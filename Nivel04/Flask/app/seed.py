from sqlalchemy import *
import os
from sqlalchemy.orm import (
    relationship,
    sessionmaker,
    scoped_session)

DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
ruta = "postgresql://{}:{}@{}/{}".format(DATABASE_USER, DATABASE_PASSWORD,
                                         DATABASE_HOST, DATABASE_NAME)

engine = create_engine(ruta)

metadata = MetaData()

actives = Table('actives', metadata,
                Column('id', Integer, primary_key=True),
                Column('active', Boolean),
                Column('country', String(60), nullable=False),
                Column('city', String(50), nullable=False)
                )

descripciones = Table('descripciones', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('sku', String(7), unique=True, nullable=False),
                      Column('descripcion', String(100), nullable=False),
                      Column('precio', Float, nullable=False)
                      )

reglas = Table('reglas', metadata,
               Column('id_regla', Integer, primary_key=True),
               Column('city', String(60), nullable=False),
               Column('country', String(50), nullable=False),
               Column('sku', String(50), ForeignKey('descripciones.sku'), nullable=False),
               Column('min_condition', Integer, nullable=False),
               Column('max_condition', Integer, nullable=False),
               Column('variation', Float, nullable=False),
               )


def create_seed():
    metadata.create_all(engine)
    llenarTabla()


def llenarTabla():
    conn = engine.connect()
    Session = scoped_session(sessionmaker(bind=engine))
    # Tabla de Actives
    q = Session.query(actives).count()
    if q == 0:
        conn.execute(actives.insert(), [
            {'city': 'Nueva Guinea', 'country': 'ni', 'active': True},
            {'city': 'León', 'country': 'ni', 'active': True},
            {'city': 'Managua', 'country': 'ni', 'active': True},
            {'city': 'Masaya', 'country': 'ni', 'active': True}
        ])
    d = Session.query(descripciones).count()
    if d == 0:
        conn.execute(descripciones.insert(), [
            {'sku': 'AZ00001', 'descripcion': 'Paraguas de señora estampado', 'precio': 10},
            {'sku': 'AZ00002', 'descripcion': 'Helado de sabor fresa', 'precio': 1},
        ])
    r = Session.query(reglas).count()
    if r == 0:
        conn.execute(reglas.insert(), [
            {
                'city': 'León',
                'country': 'ni',
                'sku': 'AZ00001',
                'min_condition': 500,
                'max_condition': 599,
                'variation': 1.5
            },
            {
                'city': 'León',
                'country': 'ni',
                'sku': 'AZ00002',
                'min_condition': 500,
                'max_condition': 599,
                'variation': 0.5
            },
            {
                'city': 'León',
                'country': 'ni',
                'sku': 'AZ00002',
                'min_condition': 800,
                'max_condition': 810,
                'variation': 1.5
            },
            {
                'city': 'León',
                'country': 'ni',
                'sku': 'AZ00001',
                'min_condition': 800,
                'max_condition': 810,
                'variation': 0.5
            },
            {
                'city': 'Nueva Guinea',
                'country': 'ni',
                'sku': 'AZ00001',
                'min_condition': 500,
                'max_condition': 599,
                'variation': 1.5
            },
            {
                'city': 'Nueva Guinea',
                'country': 'ni',
                'sku': 'AZ00002',
                'min_condition': 500,
                'max_condition': 599,
                'variation': 0.5
            },
        ])
