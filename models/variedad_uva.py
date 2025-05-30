import uuid
from models.db import db

class VariedadUva(db.Model):
    __tablename__ = 'variedades_uva'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String(100), nullable=False)
    origen = db.Column(db.String(100), nullable=False)
    foto_path = db.Column(db.String(200), nullable=False)

    procesos = db.relationship('ProcesoVinificacion', backref='variedad', cascade="all, delete-orphan")

    def __init__(self,name,origin,photo=None):
        self.name=name
        self.origin=origin
        self.photo=photo

    def serialize(self):
        return {
            'id_grape_variety':self.id_grape_variety,
            'name':self.name,
            'origin':self.origin,
            'photo':self.photo,
        }