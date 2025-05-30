# routes_recepcion.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, EtapaRecepcion, ProcesoVinificacion 
from uuid import uuid4
import datetime #Lo importamos para el manejo de fechas

recepcion = Blueprint('recepcion', __name__, url_prefix='/recepcion') 

@recepcion.route('/crear/<proceso_id>', methods=['GET', 'POST'])

def crear_recepcion(proceso_id):
    if request.method == 'POST':
        
        fecha_str = request.form.get('fecha') # Obtenemos la fecha como string
        cantidad = request.form.get('cantidad_kg')
        

        if not fecha_str or not cantidad: # Validamos los campos de Recepcion
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(request.url)

        try:
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date() # Convertimos la fecha a tipo string.
            cantidad = float(cantidad)
            
        except ValueError:
            flash('Debe ingresar valores válidos para la fecha y la cantidad.', 'danger')
            return redirect(request.url)

        nueva_recepcion = EtapaRecepcion(
            id=str(uuid4()),
            proceso_id=proceso_id,
            fecha=fecha,
            cantidad_kg=cantidad
        )
        db.session.add(nueva_recepcion)
        db.session.commit()
        flash('Recepción de uva registrada.', 'success')
        # Ajustamos la redirección a la ruta indicada

        return redirect(url_for('proceso.detalles_proceso', proceso_id=proceso_id)) # Ajustamos la redirección a la ruta indicada

    return render_template('recepcion/crear.html', proceso_id=proceso_id)

@recepcion.route('/editar/<recepcion_id>', methods=['GET', 'POST'])

def editar_recepcion(recepcion_id):
    recepcion_existente = EtapaRecepcion.query.get_or_404(recepcion_id) # Usar EtapaRecepcion

    if request.method == 'POST':
        fecha_str = request.form.get('fecha') # Obtener la fecha como string
        cantidad = request.form.get('cantidad_kg')

        if not fecha_str or not cantidad:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(request.url)

        try:
            recepcion_existente.fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date() # Convertir la fecha
            recepcion_existente.cantidad_kg = float(cantidad)
        except ValueError:
            flash('Debe ingresar valores válidos para la fecha y la cantidad.', 'danger')
            return redirect(request.url)

        db.session.commit()
        flash('Recepción actualizada correctamente.', 'success')
        
        return redirect(url_for('proceso.detalles_proceso', proceso_id=recepcion_existente.proceso_id)) # Ajustamos la redirección a la ruta indicada

    return render_template('recepcion/editar.html', recepcion=recepcion_existente)


@recepcion.route('/eliminar/<recepcion_id>', methods=['POST'])

def eliminar_recepcion(recepcion_id):
    recepcion_a_eliminar = EtapaRecepcion.query.get_or_404(recepcion_id) 
    proceso_id_relacionado = recepcion_a_eliminar.proceso_id
    db.session.delete(recepcion_a_eliminar)
    db.session.commit()
    flash('Recepción eliminada correctamente.', 'success')
    
    return redirect(url_for('proceso.detalles_proceso', proceso_id=proceso_id_relacionado)) # Ajustamos la redirección a la ruta indicada