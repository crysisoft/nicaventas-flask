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


def create_seed():
    metadata.create_all(engine)
    llenarTabla()


def llenarTabla():
    conn = engine.connect()
    Session = scoped_session(sessionmaker(bind=engine))
    q = Session.query(actives).count()
    if q == 0:
        conn.execute(actives.insert(), [
            {'city': 'Nueva Guinea', 'country': 'Ni', 'active': True},
            {'city': 'León', 'country': 'Ni', 'active': True},
            {'city': 'Managua', 'country': 'Ni', 'active': True},
            {'city': 'Masaya', 'country': 'Ni', 'active': True}
        ])
