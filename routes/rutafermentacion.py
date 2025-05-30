# routes_fermentacion.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, fermentacion, ProcesoVinificacion # Asegúrate de importar EtapaFermentacionAlc con el nombre correcto
from uuid import uuid4
import datetime # Necesario para manejar fechas

fermentacion = Blueprint('fermentacion', __name__, url_prefix='/fermentacion') 

@fermentacion.route('/crear/<proceso_id>', methods=['GET', 'POST'])
def crear_fermentacion(proceso_id):
    if request.method == 'POST':
        # Campos requeridos de la entidad
        fecha_inicio_str = request.form.get('fecha_inicio')
        fecha_fin_str = request.form.get('fecha_fin')
        temperatura_str = request.form.get('temperatura')
        acidez_str = request.form.get('acidez')
        ph_str = request.form.get('ph')

        # Validamos que todos los campos se completen
        if not all([fecha_inicio_str, fecha_fin_str, temperatura_str, acidez_str, ph_str]):
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(request.url)

        try:
            fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            temperatura = float(temperatura_str)
            acidez = float(acidez_str)
            ph = float(ph_str)
        except ValueError:
            flash('Debe ingresar valores válidos para fechas y números.', 'danger')
            return redirect(request.url)

        # Creamos una nueva instancia de Fermentacion
        nueva_fermentacion = fermentacion(
            id=str(uuid4()),
            proceso_id=proceso_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            temperatura=temperatura,
            acidez=acidez,
            ph=ph
        )
        db.session.add(nueva_fermentacion)
        db.session.commit()
        flash('Etapa de fermentación registrada correctamente.', 'success')
        
        return redirect(url_for('etapas.registrar_etapas', proceso_id=proceso_id)) # Ajustamos la redirección a la ruta indicada

    return render_template('fermentacion/crear.html', proceso_id=proceso_id)


@fermentacion.route('/editar/<fermentacion_id>', methods=['GET', 'POST'])
def editar_fermentacion(fermentacion_id):
    # Obtener la instancia de EtapaFermentacionAlc por su ID
    etapa_fermentacion = fermentacion.query.get_or_404(fermentacion_id)

    if request.method == 'POST':
        # Campos de la entidad EtapaFermentacionAlc
        fecha_inicio_str = request.form.get('fecha_inicio')
        fecha_fin_str = request.form.get('fecha_fin')
        temperatura_str = request.form.get('temperatura')
        acidez_str = request.form.get('acidez')
        ph_str = request.form.get('ph')

        # Validar que todos los campos obligatorios estén presentes
        if not all([fecha_inicio_str, fecha_fin_str, temperatura_str, acidez_str, ph_str]):
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(request.url)

        try:
            # Actualizar los atributos de la instancia existente
            etapa_fermentacion.fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            etapa_fermentacion.fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            etapa_fermentacion.temperatura = float(temperatura_str)
            etapa_fermentacion.acidez = float(acidez_str)
            etapa_fermentacion.ph = float(ph_str)
        except ValueError:
            flash('Debe ingresar valores válidos para fechas y números.', 'danger')
            return redirect(request.url)

        db.session.commit()
        flash('Etapa de fermentación actualizada correctamente.', 'success')
        # Ajusta la redirección a la página donde se listan las etapas del proceso
        return redirect(url_for('etapas.registrar_etapas', proceso_id=etapa_fermentacion.proceso_id)) # Ajustamos la redirección a la ruta indicada

    # Si es GET, renderizar el formulario de edición con los datos actuales
    return render_template('fermentacion/editar.html', fermentacion=etapa_fermentacion)


@fermentacion.route('/eliminar/<fermentacion_id>', methods=['POST'])
def eliminar_fermentacion(fermentacion_id):
    # Obtenemos la instancia de EtapaFermentacionAlc por su ID
    etapa_fermentacion = fermentacion.query.get_or_404(fermentacion_id)
    proceso_id_relacionado = etapa_fermentacion.proceso_id # Guardar el ID del proceso antes de eliminar

    db.session.delete(etapa_fermentacion)
    db.session.commit()
    flash('Etapa de fermentación eliminada correctamente.', 'success')
    
    return redirect(url_for('etapas.registrar_etapas', proceso_id=proceso_id_relacionado)) # Ajustamos la redirección a la ruta indicada