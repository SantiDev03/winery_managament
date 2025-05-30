from flask import Blueprint, render_template, redirect, url_for, flash
from models import db, ProcesoVinificacion, VariedadUva
from datetime import date

procesos_vinificacion = Blueprint('procesos_vinificacion', __name__)

@procesos_vinificacion.route('/procesos')
def listar_procesos():
    procesos = ProcesoVinificacion.query.all()
    return render_template('procesos/listar.html', procesos=procesos)

@procesos_vinificacion.route('/procesos/nuevo/<variedad_id>', methods=['GET'])
def nuevo_proceso(variedad_id):
    variedad = VariedadUva.query.get(variedad_id)
    if not variedad:
        flash('Variedad no encontrada.', 'danger')
        return redirect(url_for('variedades.listar_variedades'))

    proceso = ProcesoVinificacion(
        variedad_id=variedad_id,
        fecha_inicio=date.today()
    )
    db.session.add(proceso)
    db.session.commit()
    flash('Proceso iniciado. Complete las etapas.', 'success')
    return redirect(url_for('etapas.ver_etapas', proceso_id=proceso.id))

@procesos_vinificacion.route('/procesos/<proceso_id>')
def detalle_proceso(proceso_id):
    proceso = ProcesoVinificacion.query.get_or_404(proceso_id)
    return render_template('procesos/detalle.html', proceso=proceso)