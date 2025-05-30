import uuid
from datetime import date
from models.db import db

class ProcesoVinificacion(db.Model):
    __tablename__ = 'procesos_vinificacion'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    variedad_id = db.Column(db.String(36), db.ForeignKey('variedades_uva.id'), nullable=False)
    fecha_inicio = db.Column(db.Date, default=date.today)
    fecha_fin = db.Column(db.Date, nullable=True)

    recepcion = db.relationship('EtapaRecepcion', backref='proceso', cascade="all, delete-orphan")
    fermentacion = db.relationship('EtapaFermentacionAlc', backref='proceso', cascade="all, delete-orphan")
    crianza = db.relationship('EtapaCrianza', backref='proceso', cascade="all, delete-orphan")
    embotellado = db.relationship('EtapaEmbotellado', backref='proceso', cascade="all, delete-orphan")

    def __init__(self, variedad_id, fecha_inicio=None, fecha_fin=None):
        self.variedad_id = variedad_id
        self.fecha_inicio = fecha_inicio or date.today()
        self.fecha_fin = fecha_fin

    def serialize(self):
        return {
            'id': self.id,
            'variedad_id': self.variedad_id,
            'fecha_inicio': self.fecha_inicio.isoformat(),
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
        }