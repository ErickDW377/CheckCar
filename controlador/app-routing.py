from flask import Flask,render_template,request,flash, redirect, url_for, abort
from flask_bootstrap import Bootstrap
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.sqltypes import String
from DAO import db, Servicios, Usuario, Clientes,Autos, Mecanicos, Productos,Detalle
from flask_login import LoginManager,current_user,login_required,login_user,logout_user
from array import array



app=Flask(__name__,template_folder='../pages',static_folder='../static')
Bootstrap(app)

import json

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
@login_required
def servicios():  
    s=Servicios()
    servicios= s.consultarAll() 
    return  render_template('servicios/servicios.html', servicios=servicios) 

@app.route('/formularioServicios')
@login_required
def registrarServicios():
    if current_user.is_authenticated and current_user.is_admin():  
        s=Servicios()
        s.tipo = ''
        s.problema = ''
        s.avance = ''
        s.estatus = ''  
        autos = Autos() 
        return  render_template(
            'servicios/servicios-formulario.html',
            servicios = s,
            autos = autos.consultarAll(),                     
            editar = 0)
    else:
        abort(404)

@app.route('/formularioServicios/<int:id>')
@login_required
def editarServicios(id):
    if current_user.is_authenticated and current_user.is_admin():
        s=Servicios()
        detalles = Detalle()
           
        return  render_template(
            'servicios/servicios-formulario.html',
            servicios = s.consultar(id),
            detalles = detalles.consultar(id),            
            editar=1)
    else:
        abort(404)

@app.route('/servicios/guardar/<int:editar>',methods=['post'])
@login_required
def guardarServicios(editar):
    if current_user.is_authenticated and current_user.is_admin():
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
    else:
        abort(404)

@app.route('/servicios/<int:id>')
@login_required
def eliminarServicios(id):
    if current_user.is_authenticated and current_user.is_admin():
        s=Servicios()
        s.eliminar(id)
        flash('Servicio eliminado con exito')        
        return  servicios()
    else:
        abort(404)

@app.route('/servicios/detallesTotal/<int:id>',methods=['get'])
@login_required
def consultarSubtotal(id):
    if current_user.is_authenticated and current_user.is_admin():
        detalles=Detalle()
        return json.dumps(detalles.getSuma(id))
    else:
        abort(404)

#Enrutamiento Detalles Servicios
@app.route('/detallesServicios/<int:servicio>')
@login_required
def detallesServicios(servicio):
    if current_user.is_authenticated and current_user.is_admin():      
        productos = Productos()
        mecanicos = Mecanicos()
        return  render_template('servicios/servicios-detalles.html',
         servicio = servicio,
         mecanicos = mecanicos.consultarAll(),
         productos = productos.consultarAll())
    else:
        abort(404)

@app.route('/detallesServicios/guardar', methods=['post'])
@login_required
def guardarDetalleServicios():
    if current_user.is_authenticated and current_user.is_admin():    
        detalle = Detalle()
        detalle.idServicio= int(request.form['id'])
        detalle.idProducto = int(request.form['producto'])
        detalle.cantidad = request.form['cantidad']
        detalle.costosU = request.form['costo']
        detalle.costoTotal = request.form['total']
        detalle.areaReparacion = request.form['area']
        detalle.idEmpleado = int(request.form['mecanico'])       

        detalle.registrar()

        producto= Productos()
        producto=producto.consultar(detalle.idProducto)
        producto.restarUnidades(detalle.cantidad)

        return editarServicios(detalle.idServicio)
    else:
        abort(404)

@app.route('/producto/precio/<int:id>',methods=['get'])
@login_required
def consultarPrecio(id):
    if current_user.is_authenticated and current_user.is_admin():
        producto=Productos()
        return json.dumps(producto.consultarPrecio(id))
    else:
        abort(404)

@app.route('/detalles/<int:id>/<int:idS>')
@login_required
def eliminarDetalle(id, idS):
    if current_user.is_authenticated and current_user.is_admin():
        detalle=Detalle()
        detalle.eliminar(id,idS)               
        return  editarServicios(idS)
    else:
        abort(404)




# Enrutamiento a Autos
@app.route('/autos')
@login_required
def autos():   
    a=Autos()
    autos=a.consultarAll()
    return  render_template('autos/autos.html',autos=autos)  

@app.route('/formularioAutos')
@login_required  
def registrarAutos():
    if current_user.is_authenticated and current_user.is_admin():
        a=Autos()    
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
    else:
        abort(404)

@app.route ('/formularioAutos/<int:id>')
@login_required
def editarAutos(id):
    if current_user.is_authenticated and current_user.is_admin():
        a=Autos()
        return render_template(
            'autos/autos-formulario.html', 
            autos=a.consultar(id),
            editar=1)
    else:
        abort(404)
    
@app.route('/autos/guardar/<int:editar>',methods=['post'])
@login_required
def guardarAutos(editar):
    if current_user.is_authenticated and current_user.is_admin(): 
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
    else:
        abort(404)
    
      
@app.route('/autos/<int:id>')
@login_required
def eliminarAutos(id):
    if current_user.is_authenticated and current_user.is_admin():
        a=Autos()
        a.eliminar(id)
        flash('Auto eliminado con exito')        
        return  autos()
    else:
        abort(404)


# Enrutamiento a Mecanicos
@app.route('/mecanicos')
@login_required
def mecanicos():
    if current_user.is_authenticated and current_user.is_admin():
        m = Mecanicos()
        mecanicos = m.consultarAll()    
        return  render_template('mecanicos/mecanicos.html', mecanicos = mecanicos)
    else:
        abort(404)

@app.route('/formularioMecanicos')
@login_required
def registrarMecanicos():
    if current_user.is_authenticated and current_user.is_admin(): 
        m=Mecanicos()
        m.nombre = ''
        m.apellidoPaterno = ''
        m.apellidoMaterno = ''
        m.sexo = ''
        m.telefono = ''
        m.calle = ''
        m.numExt = 0
        m.numInt = ''   
        m.colonia = ''  
        m.municipio = ''
        m.estado = ''
        m.cp = ''
        m.puesto = ''
        m.numSeguroS = ''
        m.rfc = ''
        return  render_template(
        'mecanicos/mecanicos-formulario.html',
        mecanicos = m,
        editar = 0)
    else:
        abort(404)

@app.route('/formularioMecanicos/<int:id>')
@login_required
def editarMecanicos(id):
    if current_user.is_authenticated and current_user.is_admin():
        m=Mecanicos()        
        return  render_template(
            'mecanicos/mecanicos-formulario.html',
            mecanicos = m.consultar(id),
            editar=1)
    else:
        abort(404)

@app.route('/mecanicos/guardar/<int:editar>',methods=['post'])
@login_required
def guardarMecanicos(editar):
    if current_user.is_authenticated and current_user.is_admin():
        m=Mecanicos()        
        m.nombre =request.form['nombre']
        m.apellidoPaterno = request.form['apellidoPaterno']
        m.apellidoMaterno = request.form['apellidoMaterno']
        m.fechaNac = request.form['fechaNac'] 
        m.sexo = request.form['sexo']
        m.telefono = request.form['telefono']
        m.calle = request.form['calle']
        m.numExt = request.form['numExt']
        m.numInt = request.form['numInt']
        m.colonia = request.form['colonia']  
        m.municipio = request.form['municipio']
        m.estado = request.form['estado']
        m.cp = request.form['cp']
        m.fechaContrato = request.form['contratacion']
        m.puesto = request.form['puesto']
        m.numSeguroS = request.form['nss']
        m.rfc = request.form['rfc']   
        if editar==1:
            m.idEmpleado= int(request.form['id'])                             
            m.actualizar()
            flash('Mecanico editado con exito')                       
        else:             
            m.registrar()
            flash('Mecanico registrado exitosamente')
        return  editarMecanicos(m.idEmpleado)
    else:
        abort(404)

@app.route('/mecanicos/<int:id>')
@login_required
def eliminarMecanico(id):
    if current_user.is_authenticated and current_user.is_admin():
        m=Mecanicos()
        m.eliminar(id)
        flash('Mecanico eliminado con exito')        
        return  mecanicos()
    else:
        abort(404)



#Enrutamiento a Usuarios
@app.route('/usuarios')
@login_required
def usuarios():
    if current_user.is_authenticated and current_user.is_admin():
        u = Usuario()
        usuarios = u.consultarAll('administrador')    
        return  render_template('login/usuarios.html', usuarios = usuarios)
    else:
        abort(404)

@app.route('/formularioUsuarios/<string:url>')
@login_required
def registrarUsuarios(url):
    if current_user.is_authenticated and current_user.is_admin():
        u = Usuario()
        u.nombre = ''
        u.userName = ''
        u.email = ''
        u.password = ''
        u.estatus = True    

        return  render_template(
            'login/usuarios-formulario.html',
            usuarios = u,
            editar=0,
            url = url
            )
    else:
        abort(404) 

@app.route('/formularioUsuarios/<int:id>/<string:url>')
@login_required
def editarUsuarios(id, url):
    if current_user.is_authenticated and current_user.is_admin():
        u= Usuario()    
        return  render_template(
            'login/usuarios-formulario.html',         
            usuarios = u.consultar(id),
            editar = 1,
            url = url
            )
    else:
        abort(404)

@app.route('/formularioUsuarios/guardar/<int:editar>/<string:url>',methods=['post'])
@login_required
def guardarUsuarios(editar, url):
    if current_user.is_authenticated and current_user.is_admin():
        user=Usuario() 
        user.nombre = request.form['nombre']   
        user.userName = request.form['userName']
        user.email = request.form['email']
        user.password = request.form['password']
        user.tipo = 'administrador'
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            user.estatus=True
        else:
            user.estatus=False   
        if editar==1:
            user.idUsuario= int(request.form['idU'])                             
            user.actualizar()            
            flash('Usuario editado con exito')                       
        else:             
            user.registrar()        
            flash('Usuario registrado exitosamente')
        return  editarUsuarios(user.idUsuario, url)
    else:
        abort(404)

@app.route('/usuarios/<int:id>')
@login_required
def eliminarUsuarios(id):
    if current_user.is_authenticated and current_user.is_admin():
        u=Usuario()
        u.eliminar(id)
        flash('Usuario eliminado con exito')        
        return  usuarios()
    else:
        abort(404)

@app.route('/usuarios/email/<string:email>',methods=['get'])
def consultarEmail(email):
    usuario=Usuario()
    print("Holi")
    return json.dumps(usuario.consultarEmail(email))
                      
                      
# Enrutamiento a Clientes
@app.route('/clientes')
@login_required
def clientes():
    if current_user.is_authenticated and current_user.is_admin():
        c = Clientes()
        clientes = c.consultarAll()    
        return  render_template('clientes/clientes.html', clientes = clientes)
    else:
        abort(404)

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

@app.route('/formularioClientes/<int:id>/<string:url>')
@login_required
def editarClientes(id,url):    
    c=Clientes()
    c = c.consultar(id)
    idu = c.idUsuario
    u= Usuario()
    u = u.consultar(idu)    
    return  render_template(
        'clientes/clientes-formulario.html',
         clientes = c,
         usuarios = u,
         editar=1,
         url= url)

@app.route('/formularioClientes/guardar/<int:editar>/<string:url>',methods=['post'])
def guardarClientes(editar, url):

    user=Usuario() 
    user.nombre = request.form['nombre']   
    user.userName = request.form['userName']
    user.email = request.form['email']
    user.password = request.form['password']
    user.tipo = 'cliente'
    estatus = request.values.get('estatus',False)
    if estatus=="True":
        user.estatus=True
    else:
        user.estatus=False
    
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
        cliente.idUsuario = user.idUsuario       
        cliente.idCliente = int(request.form['idC'])
        cliente.actualizar()    
        flash('Cliente editado con exito')                       
    else:             
        user.registrar()        
        cliente.idUsuario = user.idUsuario
        cliente.registrar()
        flash('Cliente registrado exitosamente')
    return  editarClientes(cliente.idCliente,url)

@app.route('/clientes/<int:id>')
@login_required
def eliminarClientes(id):
    if current_user.is_authenticated and current_user.is_admin():
        c=Clientes()    
        c.eliminar(id)
        flash('Cliente eliminado con exito')        
        return  clientes()
    else:
        abort(404)

# Enrutamiento a Productos
@app.route('/productos')
@login_required
def productos():
    if current_user.is_authenticated and current_user.is_admin():
        p = Productos()
        productos= p.consultarAll()    
        return  render_template('productos/productos.html', productos= productos)
    else:
        abort(404)

@app.route('/formularioProductos')
@login_required
def registrarProductos():
    if current_user.is_authenticated and current_user.is_admin(): 
        p=Productos()
        p.nombre= '' 
        p.marca= '' 
        p.modelo= ''
        p.tipo=''     
        p.anaquel= 0 
        p.estante= 0 
        p.costo= 0
        p.precio= '' 
        p.descripcion= '' 
        p.unidades= 0      
        return render_template(
            'productos/productos-formularios.html',
            productos = p,
            editar = 0)
    else:
        abort(404)

@app.route('/formularioProductos/<int:id>')
@login_required
def editarProductos(id):
    if current_user.is_authenticated and current_user.is_admin():
        p=Productos()        
        return  render_template(
         'productos/productos-formularios.html',
         productos = p.consultar(id),
         editar=1)
    else:
        abort(404)

@app.route('/productos/guardar/<int:editar>',methods=['post'])
@login_required
def guardarProductos(editar):
    if current_user.is_authenticated and current_user.is_admin():
        p=Productos()          
        p.nombre=request.form['nombre']
        p.marca=request.form['marca']
        p.modelo=request.form['modelo']
        p.tipo=request.form['tipo']
        p.anaquel=request.form['anaquel']
        p.estante=request.form['estante']
        p.costo=request.form['costo']
        p.precio=request.form['precio']
        p.descripcion=request.form['descripcion']
        p.unidades=request.form['unidades']
        if editar==1:
            p.idProducto= int(request.form['id'])                             
            p.actualizar()
            flash('Producto editado con exito')                       
        else:             
            p.registrar()
            flash('Producto registrado exitosamente')
        return  editarProductos(p.idProducto)
    else:
        abort(404)

@app.route('/productos/<int:id>')
@login_required
def eliminarProductos(id):
    if current_user.is_authenticated and current_user.is_admin():
        p=Productos()
        p.eliminar(id)
        flash('Producto eliminado con exito')        
        return  productos()
    else:
        abort(404)

@app.errorhandler(404)
def error_404(e):
    return redirect(url_for('inicio'))


if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)
    
