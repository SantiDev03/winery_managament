import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from models.db import db
from models.variedades_uva import VariedadUva
from models.procesos_vinificacion import ProcesoVinificacion

variedad_uva = Blueprint('variedades_uva',__name__)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@variedad_uva.route('/')
def index():
    return render_template('index.html')

@variedad_uva.route('/variedades')
def listar_variedades():
    variedades=VariedadUva.query.all()
    return render_template('variedades.html',variedades=variedades)

@variedad_uva.route('/variedades/nueva', methods=['GET','POST'])
def nueva_variedad():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip() #para que no se guarden los espacios al inicio y final
        origen = request.form.get('origen', '').strip()
        foto = request.files.get('foto')

        # Validaciones básicas
        if not nombre or not origen:
            flash('Nombre y origen son obligatorios.', 'danger')
            return redirect(request.url)

        if not foto or foto.filename == '':
            flash('Debe seleccionar una imagen.', 'danger')
            return redirect(request.url)

        if not allowed_file(foto.filename):
            flash('Formato de imagen no permitido. Solo png, jpg, jpeg, gif.', 'danger')
            return redirect(request.url)

        # Guardar archivo
        filename = secure_filename(foto.filename)
        ruta_foto = os.path.join(UPLOAD_FOLDER, filename)

        try:
            foto.save(ruta_foto)

            nueva = VariedadUva(
                nombre=nombre,
                origen=origen,
                foto_path=ruta_foto
            )
            db.session.add(nueva)
            db.session.commit()

            flash('Variedad agregada exitosamente', 'success')
            return redirect(url_for('variedades_uva.listar_variedades'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar la variedad: {str(e)}', 'danger')
            return redirect(request.url)

    return render_template('nueva_variedad.html')


@variedad_uva.route('/procesos/nuevo/<variedad_id>', methods=['GET'])
def nuevo_proceso(variedad_id):
    proceso = ProcesoVinificacion(
        variedad_id=variedad_id
    )
    db.session.add(proceso)
    db.session.commit()
    return redirect(url_for('etapas.registrar_etapas', proceso_id=proceso.id))