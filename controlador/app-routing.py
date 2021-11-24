from flask import Flask,render_template,request,flash, redirect, url_for
from flask_bootstrap import Bootstrap
from DAO import db, Servicios, Usuario, Clientes
from flask_login import LoginManager,current_user,login_required,login_user,logout_user


app=Flask(__name__,template_folder='../pages',static_folder='../static')
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Hola.123@127.0.0.1/checkCar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='cl4v3'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = u"! Debes iniciar sesión !"

@app.route('/')
def incio():    
    return  render_template('inicio/inicio.html')

# Enrutamiento login
@app.route('/usuarios/login',methods=['post'])
def validarUsuario():
    user=Usuario()
    email=request.form['email']
    password=request.form['password']
    user=user.validar(email,password)
    if user!=None:
        login_user(user)
        return render_template('inicio/inicio.html')
    else:
        flash('!Datos de la sesión incorrectos!')
        return render_template('login/login.html')

@app.route('/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

@app.route('/login')
def login():    
    return  render_template('login/login.html')

# Enrutamiento a Servicios
@app.route('/servicios')
def servicios():  
    s=Servicios()
    servicios= s.consultarAll() 
    return  render_template('servicios/servicios.html', servicios=servicios) 

@app.route('/formularioServicios')
def registrarServicios():  
    s=Servicios()
    s.tipo = ''
    s.problema = ''
    s.avance = ''
    s.estatus = ''       
    return  render_template(
        'servicios/servicios-formulario.html',
        servicios = s,
        editar = 0)

@app.route('/formularioServicios/<int:id>')
def editarServicios(id):
    s=Servicios()        
    return  render_template(
        'servicios/servicios-formulario.html',
         servicios = s.consultar(id),
         editar=1)

@app.route('/servicios/guardar/<int:editar>',methods=['post'])
def guardarS(editar): 
        s=Servicios()          
        s.idAutomovil= request.form['auto']
        s.tipo=request.form['tipo']
        s.llegada=request.form['llegada']
        s.salida=request.form['salida']
        s.problema=request.form['problema']
        s.avance=request.form['avance']
        s.garantia=request.form['garantia']
        s.estatus=request.form['estatus']
        s.manoObra=request.form['manoObra']
        s.total=request.form['total']        
        if editar==1:
            s.idServicio= int(request.form['id'])                             
            s.actualizar()
            flash('Servicio editado con exito')                       
        else:             
            s.registrar()
            flash('Servicio registrado exitosamente')
        return  render_template(
            'servicios/servicios-formulario.html',
            servicios = s,
            editar=1
            )

@app.route('/servicios/<int:id>')
def eliminarS(id):
    s=Servicios()
    s.eliminar(id)
    flash('Servicio eliminado con exito')        
    return  servicios()

@app.route('/detallesServicios')
def detallesServicios():       
    return  render_template('servicios/servicios-detalles.html')

# Enrutamiento a Autos
@app.route('/autos')
def autos():    
    return  render_template('autos/autos.html')    

@app.route('/formularioAutos')
def formularioAutos():    
    return  render_template('autos/autos-formulario.html')

# Enrutamiento a Mecanicos
@app.route('/mecanicos')
def mecanicos():    
    return  render_template('mecanicos/mecanicos.html')

@app.route('/formularioMecanicos')
def formularioMecanicos():    
    return  render_template('mecanicos/mecanicos-formulario.html')


# Enrutamiento a Clientes
@app.route('/clientes')
def clientes():    
    return  render_template('clientes/clientes.html')

@app.route('/formularioClientes')
def formularioCliente():    
    return  render_template('clientes/clientes-formulario.html')

@app.route('/formularioClientes/guardar',methods=['post'])
def guardarC():

    user=Usuario()
    user.nombre = request.form['nombre']   
    user.userName = request.form['userName']
    user.email = request.form['email']
    user.password = request.form['password']
    user.tipo = request.form['tipo']
    user.estatus = request.form['estatus']   
    user.registrar()

    cliente = Clientes()
    cliente.idUsuario = user.idUsuario
    cliente.empresa = request.form['empresa']    
    cliente.telefono = request.form['tel']    
    cliente.calle = request.form['calle']
    cliente.numExt = request.form['numExt']
    cliente.numInt = request.form['numInt']
    cliente.colonia = request.form['colonia']
    cliente.municipio = request.form['municipio']
    cliente.estado = request.form['estado']    
    cliente.registrar()

    
    #flash('Usuario registrado con exito')
    return clientes()

# Enrutamiento a Productos
@app.route('/productos')
def productos():    
    return  render_template('productos/productos.html') 

@app.route('/formularioProductos')
def formularioProductos():    
    return  render_template('productos/productos-formularios.html') 


if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)