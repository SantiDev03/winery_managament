import uuid 
from models.db import db 

class EtapaFermentacionAlc(db.Model):
    _tablename_ = 'etapas_fermentacion'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    proceso_id = db.Column(db.String(36), db.ForeignKey('procesos_vinificacion.id'), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    temperatura = db.Column(db.Float, nullable=False)
    acidez = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)

    def __init__(self,proceso_id,fecha_inicio,fecha_fin,temperatura,acidez,ph):
        self.proceso_id = proceso_id
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.temperatura = temperatura
        self.acidez = acidez
        self.ph = ph 

    def serialize(self):
        return {
            'id' : self.id,
            'proceso_id' : self.proceso_id,
            'fecha_inicio' : self.fecha_inicio,
            'fecha_fin' : self.fecha_fin,
            'temperatura' : self.temperatura,
            'acidez' : self.acidez,
            'ph' : self.ph
        }
