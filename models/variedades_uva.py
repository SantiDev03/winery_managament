import uuid
from models.db import db

class VariedadUva(db.Model):
    __tablename__ = 'variedades_uva'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String(100), nullable=False)
    origen = db.Column(db.String(100), nullable=False)
    foto_path = db.Column(db.String(200), nullable=False)

    procesos = db.relationship('ProcesoVinificacion', backref='variedad', cascade="all, delete-orphan")

    def __init__(self, nombre, origen, foto_path=None):
        self.nombre = nombre
        self.origen = origen
        self.foto_path = foto_path

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'origen': self.origen,
            'foto_path': self.foto_path,
        }
