import uuid 
from models.db import db

class EtapaRecepcion(db.Model):
    _tablename_ = 'etapas_recepcion'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    proceso_id = db.Column(db.String(36), db.ForeignKey('procesos_vinificacion.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    cantidad_kg = db.Column(db.Float, nullable=False)

    def __init__(self,proceso_id,fecha,cantidad_kg):
        self.proceso_id = proceso_id
        self.fecha = fecha
        self.cantidad_kg= cantidad_kg

    def serialize(self):
        return {
            'id' : self.id,
            'proceso_id' : self.proceso_id,
            'fecha' : self.fecha,
            'cantidad_kg' : self.cantidad_kg
        }

