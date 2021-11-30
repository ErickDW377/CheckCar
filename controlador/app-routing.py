from flask import Flask,render_template,request,flash, redirect, url_for
from flask_bootstrap import Bootstrap
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.sqltypes import String
from DAO import db, Servicios, Usuario, Clientes,Autos
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
def iniciar():    
    return  render_template('inicio/inicio.html')

@app.route('/inicio')
def inicio():    
    return  render_template('inicio/inicio.html')

# Enrutamiento login
@app.route('/login')
def login():    
    return  render_template('login/login.html')

@app.route('/usuarios/login',methods=['post'])
def validarUsuario():
    user=Usuario()
    email=request.form['email']
    password=request.form['password']
    user=user.validar(email,password)
    if user!=None:
        login_user(user)
        return inicio()
    else:
        flash('!Datos de la sesión incorrectos!')
        return login()

@app.route('/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('inicio'))

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

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
def guardarServicios(editar): 
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
        return  editarServicios(s.idServicio)

@app.route('/servicios/<int:id>')
def eliminarServicios(id):
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
    a=Autos()
    autos=a.consultarAll()
    return  render_template('autos/autos.html',autos=autos)  

@app.route('/formularioAutos')  
def registrarAutos():
    a=Autos()
    a.idAutomovil= 0
    a.idCliente= 0
    a.placa= ''
    a.marca= ''
    a.modelo= ''
    a.color= ''
    a.año= ''
    a.transmicion= ''
    return render_template(
        'autos/autos-formulario.html',autos=a,editar=0 
    )
@app.route ('/formularioAutos/<int:id>')
def editarAutos(id):
    a=Autos()
    return render_template(
         'autos/autos-formulario.html', 
         autos=a.consultar(id),
         editar=1)
    
@app.route('/autos/guardar/<int:editar>',methods=['post'])
def guardarAutos(editar): 
    a=Autos()
    a.idCliente= request.form['cliente']
    a.placa= request.form['placa']
    a.marca=request.form['marca']                  
    a.modelo=request.form['modelo']                 
    a.color= request.form['color']
    a.año= request.form['año']
    a.transmicion=request.form['transmicion']
    if editar==1:
        a.idAutomovil= int(request.form['id'])                             
        a.actualizar()
        flash('Auto editado con exito')                       
    else:             
            a.registrar()
            flash('Auto registrado exitosamente')
            
    return  editarAutos(a.idAutomovil)
    
      
@app.route('/autos/<int:id>')
def eliminarAutos(id):
    a=Autos()
    a.eliminar(id)
    flash('Auto eliminado con exito')        
    return  autos()







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
    c = Clientes()
    clientes = c.consultarAll()    
    return  render_template('clientes/clientes.html', clientes = clientes)

@app.route('/formularioClientes/<string:url>')
def registrarClientes(url):
    c=Clientes()
    c.empresa= '' 
    c.telefono= '' 
    c.calle= ''
    c.numExt= 0    
    c.numInt= '' 
    c.colonia= '' 
    c.municipio= ''
    c.estado= '' 
    c.cp= ''

    u = Usuario()
    u.nombre = ''
    u.userName = ''
    u.email = ''
    u.password = ''    

    return  render_template(
        'clientes/clientes-formulario.html',
         clientes = c,
         usuarios = u,
         editar=0,
         url = url)   

@app.route('/formularioClientes/<int:idc>/<int:idu>/<string:url>')
def editarClientes(idc, idu, url):    
    c=Clientes()
    if idc == 0:
        c = c.buscarXusuario(idu)        
    else:
        c = c.consultar(idc)        
    
    u= Usuario()
    usuarios = u.consultar(idu)    
    return  render_template(
        'clientes/clientes-formulario.html',
         clientes = c,
         usuarios = usuarios,
         editar=1,
         url= url)

@app.route('/formularioClientes/guardar/<int:editar>/<string:url>',methods=['post'])
def guardarClientes(editar, url):

    user=Usuario()
    user.nombre = request.form['nombre']   
    user.userName = request.form['userName']
    user.email = request.form['email']
    user.password = request.form['password']
    tipo = request.form.get('tipo')    
    if tipo != None:        
        user.tipo = tipo
    else:
        user.tipo = 'cliente'
    estatus = request.values.get('estatus',False)
    if estatus=="True":
        user.estatus=True
    else:
        user.estatus=False

    if user.tipo == 'cliente':
        cliente = Clientes()        
        cliente.empresa = request.form['empresa']    
        cliente.telefono = request.form['tel']    
        cliente.calle = request.form['calle']        
        cliente.numExt =   request.form['numExt']      
        cliente.numInt = request.form['numInt']
        cliente.colonia = request.form['colonia']
        cliente.municipio = request.form['municipio']
        cliente.estado = request.form['estado']     
        cliente.cp = request.form['cp']
    if editar==1:
        user.idUsuario= int(request.form['idU'])                             
        user.actualizar()
        if user.tipo == 'cliente':
            cliente.idUsuario = user.idUsuario
            cliente.idCliente = int(request.form['idC'])
            cliente.actualizar()
        flash('Usuario editado con exito')                       
    else:             
        user.registrar()
        if user.tipo == 'cliente':
            cliente.idUsuario = user.idUsuario
            cliente.registrar()
        flash('Usuario registrado exitosamente')
    return  editarClientes(cliente.idCliente,user.idUsuario,url)

@app.route('/clientes/<int:id>')
def eliminarClientes(id):
    c=Clientes()
    c.eliminar(id)
    flash('Cliente eliminado con exito')        
    return  clientes()

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
    
