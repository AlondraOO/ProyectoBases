from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu-clave-secreta-aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/gym_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos de Base de Datos

class Socio(db.Model):
    __tablename__ = 'socio'
    id_socio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    edad = db.Column(db.Integer)
    fecha_inscripcion = db.Column(db.Date, default=date.today)
    tipo_membresia = db.Column(db.String(20), nullable=False)  # MENSUAL, ANUAL, PREMIUM
    estado_membresia = db.Column(db.String(20), default='ACTIVO')
    
    pagos = db.relationship('Pago', backref='socio', lazy=True)
    asistencias = db.relationship('Asistencia', backref='socio', lazy=True)

class Clase(db.Model):
    __tablename__ = 'clase'
    id_clase = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    id_instructor = db.Column(db.Integer, db.ForeignKey('instructor.id_instructor'))
    
    asistencias = db.relationship('Asistencia', backref='clase', lazy=True)

class Instructor(db.Model):
    __tablename__ = 'instructor'
    id_instructor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(100))
    especialidad = db.Column(db.String(100))
    disponibilidad = db.Column(db.String(200))
    
    clases = db.relationship('Clase', backref='instructor', lazy=True)

class Pago(db.Model):
    __tablename__ = 'pago'
    id_pago = db.Column(db.Integer, primary_key=True)
    id_socio = db.Column(db.Integer, db.ForeignKey('socio.id_socio'), nullable=False)
    fecha_pago = db.Column(db.Date, default=date.today)
    monto = db.Column(db.Float, nullable=False)
    estado_pago = db.Column(db.String(20), default='PAGADO')
    tipo_pago = db.Column(db.String(20))  # INSCRIPCION, MENSUALIDAD, EXTRA

class Asistencia(db.Model):
    __tablename__ = 'asistencia'
    id_asistencia = db.Column(db.Integer, primary_key=True)
    id_socio = db.Column(db.Integer, db.ForeignKey('socio.id_socio'), nullable=False)
    id_clase = db.Column(db.Integer, db.ForeignKey('clase.id_clase'), nullable=False)
    fecha_asistencia = db.Column(db.Date, default=date.today)

# Rutas

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/socios')
def listar_socios():
    socios = Socio.query.all()
    return render_template('socios.html', socios=socios)

@app.route('/socios/nuevo', methods=['GET', 'POST'])
def nuevo_socio():
    if request.method == 'POST':
        try:
            socio = Socio(
                nombre=request.form['nombre'],
                correo=request.form['correo'],
                telefono=request.form['telefono'],
                edad=int(request.form['edad']),
                tipo_membresia=request.form['tipo_membresia']
            )
            db.session.add(socio)
            db.session.commit()
            
            # Crear pago de inscripción
            montos = {'MENSUAL': 500, 'ANUAL': 5000, 'PREMIUM': 1000}
            pago = Pago(
                id_socio=socio.id_socio,
                monto=montos[socio.tipo_membresia],
                tipo_pago='INSCRIPCION'
            )
            db.session.add(pago)
            db.session.commit()
            
            flash('Socio registrado exitosamente', 'success')
            return redirect(url_for('listar_socios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar socio: {str(e)}', 'danger')
    
    return render_template('nuevo_socio.html')

@app.route('/clases')
def listar_clases():
    clases = Clase.query.all()
    return render_template('clases.html', clases=clases)

@app.route('/clases/nueva', methods=['GET', 'POST'])
def nueva_clase():
    if request.method == 'POST':
        try:
            clase = Clase(
                nombre=request.form['nombre'],
                horario=request.form['horario'],
                capacidad=int(request.form['capacidad']),
                id_instructor=int(request.form['id_instructor']) if request.form['id_instructor'] else None
            )
            db.session.add(clase)
            db.session.commit()
            flash('Clase creada exitosamente', 'success')
            return redirect(url_for('listar_clases'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear clase: {str(e)}', 'danger')
    
    instructores = Instructor.query.all()
    return render_template('nueva_clase.html', instructores=instructores)

@app.route('/instructores')
def listar_instructores():
    instructores = Instructor.query.all()
    return render_template('instructores.html', instructores=instructores)

@app.route('/instructores/nuevo', methods=['GET', 'POST'])
def nuevo_instructor():
    if request.method == 'POST':
        try:
            instructor = Instructor(
                nombre=request.form['nombre'],
                telefono=request.form['telefono'],
                correo=request.form['correo'],
                especialidad=request.form['especialidad'],
                disponibilidad=request.form['disponibilidad']
            )
            db.session.add(instructor)
            db.session.commit()
            flash('Instructor registrado exitosamente', 'success')
            return redirect(url_for('listar_instructores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar instructor: {str(e)}', 'danger')
    
    return render_template('nuevo_instructor.html')

@app.route('/asistencia', methods=['GET', 'POST'])
def registrar_asistencia():
    if request.method == 'POST':
        try:
            asistencia = Asistencia(
                id_socio=int(request.form['id_socio']),
                id_clase=int(request.form['id_clase'])
            )
            db.session.add(asistencia)
            db.session.commit()
            flash('Asistencia registrada exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar asistencia: {str(e)}', 'danger')
    
    socios = Socio.query.filter_by(estado_membresia='ACTIVO').all()
    clases = Clase.query.all()
    asistencias = db.session.query(Asistencia, Socio, Clase)\
        .join(Socio).join(Clase)\
        .order_by(Asistencia.fecha_asistencia.desc()).limit(20).all()
    
    return render_template('asistencia.html', socios=socios, clases=clases, asistencias=asistencias)

@app.route('/pagos')
def listar_pagos():
    pagos = db.session.query(Pago, Socio)\
        .join(Socio)\
        .order_by(Pago.fecha_pago.desc()).all()
    return render_template('pagos.html', pagos=pagos)

@app.route('/pagos/nuevo', methods=['GET', 'POST'])
def nuevo_pago():
    if request.method == 'POST':
        try:
            pago = Pago(
                id_socio=int(request.form['id_socio']),
                monto=float(request.form['monto']),
                tipo_pago=request.form['tipo_pago']
            )
            db.session.add(pago)
            db.session.commit()
            flash('Pago registrado exitosamente', 'success')
            return redirect(url_for('listar_pagos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar pago: {str(e)}', 'danger')
    
    socios = Socio.query.all()
    return render_template('nuevo_pago.html', socios=socios)

@app.route('/init-db')
def init_db():
    try:
        db.create_all()
        return 'Base de datos inicializada correctamente'
    except Exception as e:
        return f'Error al inicializar base de datos: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)