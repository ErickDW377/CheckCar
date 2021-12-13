from enum import unique

from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import VARCHAR
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,Date,Float,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from flask_login import UserMixin

db=SQLAlchemy()

class Servicios(db.Model):
    __tablename__= 'Servicios'
    idServicio = Column(Integer, primary_key=True)
    idAutomovil = Column(Integer, nullable=False)
    tipo = Column(String(20), nullable= False)
    llegada = Column(Date, nullable= False)
    salida = Column(Date, nullable= False)
    problema = Column(String(250), nullable= False)
    avance = Column(String(250), nullable= False)
    garantia = Column(Integer, nullable= False)
    estatus = Column(String(1),nullable= False)
    manoObra = Column(Float,nullable= False)
    total = Column(Float, nullable= False)
    #automovil= relationship('Automovil',backref='servicios',lazy='select')

    def registrar(self):
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        db.session.delete(objeto)
        db.session.commit()

    def getDetalles(self):
        detalles= Detalle()
        return detalles.consultar(self.idServicio)
        

class Detalle(db.Model):
    __tablename__= 'Detalles_Servicios'
    idServicio = Column(Integer,  primary_key= True)
    idProducto = Column(Integer, primary_key= True)
    cantidad = Column(Integer, nullable= False)
    costosU = Column(Float, nullable= False)
    costoTotal = Column(Float, nullable= False)
    areaReparacion = Column(String(30), nullable= False)
    idEmpleado = Column(Integer, nullable= False)   

    def registrar(self):
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.filter(Detalle.idServicio==id)
    
    def consultar2(self,id,idS):
        return self.query.filter(Detalle.idServicio==idS, Detalle.idProducto==id).first()

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id,idS):
        objeto=self.consultar2(id,idS)
        db.session.delete(objeto)
        db.session.commit()

    def getProducto(self):
        producto = Productos()
        producto= producto.consultar(self.idProducto)
        return producto.nombre

    def getSuma(self, id):
        salida={"estatus":"","suma":""} 
        detalles = self.consultar(id)
        suma = 0;
        for detalle in detalles:
            suma+= detalle.costoTotal

        salida["estatus"]="OK"
        salida["suma"]= suma       
        return salida
       


class Clientes(db.Model):
    __tablename__ = 'Clientes'
    idCliente = Column(Integer, primary_key=True)
    idUsuario = Column(Integer,nullable=False)
    empresa = Column(String(40), unique=True)    
    telefono = Column(String(12),nullable=False)    
    calle = Column(String(30))
    numExt = Column(Integer)
    numInt = Column(String(2))
    colonia = Column(String(20))
    municipio = Column(String(20))
    estado = Column(String(20))
    cp = Column(String(5))   
    
    def registrar(self):        
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        db.session.delete(objeto)                
        db.session.commit()
        usuario = Usuario()
        usuario.eliminar(objeto.idUsuario)

    def buscarXusuario(self,usuario):
        return self.query.filter(Clientes.idUsuario == usuario).first()

    def getUsuario(self):
        u = Usuario()
        u= u.consultar(self.idUsuario)
        return u

    def getNombre(self):        
        u = self.getUsuario()
        return u.nombre
    
    def getEmail(self):        
        u = self.getUsuario()
        return u.email
    
class Usuario(UserMixin,db.Model):
    __tablename__='Usuarios'
    idUsuario=Column(Integer,primary_key=True)
    nombre=Column(String(100), unique=True, nullable= False)
    userName=Column(String(15),nullable=False, unique=True)
    email=Column(String(100),unique=True)
    password=Column(String(20),nullable=False)    
    tipo=Column(String(10),default='cliente')
    estatus=Column(Boolean,default=True)

    def registrar(self):
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self, tipo):        
        usuarios = self.query.filter(Usuario.tipo==tipo)
        return usuarios

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        db.session.delete(objeto)
        db.session.commit()
    
    def validar(self,email,passw):
        usuario=None
        usuario=self.query.filter(Usuario.email==email,Usuario.password==passw,Usuario.estatus==True).first()
        return usuario

    def buscarCliente(self):
        cliente = Clientes()
        cliente = cliente.buscarXusuario(self.idUsuario)
        return cliente.idCliente

    #Metodos relacionados al perfilamiento
    def is_authenticated(self):
        return True

    def is_active(self):
         return self.estatus

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idUsuario

    def is_admin(self):
        if self.tipo=='administrador':
            return True
        else:
            return False

    def is_cliente(self):
        if self.tipo=='cliente':
            return True
        else:
            return False
    
        
class Autos(db.Model):
    __tablename__='Automovil'
    idAutomovil=Column(Integer,primary_key=True)
    idCliente = Column(Integer,nullable= False)
    placa = Column( String(20),nullable= False)
    marca = Column(String(20), nullable= False)
    modelo= Column(String(20), nullable= False)
    color= Column(String (15), nullable= False)
    año= Column(String(4),nullable= False)
    transmicion= Column(String(15), nullable= False)
    
    def registrar (self):
        db.session.add(self)
        db.session.commit()
    
    def consultar (self,id):
       return self.query.get(id)
    
    def consultarAll(self):        
       return self.query.all()
   
    def actualizar(self):
        db.session.merge(self)
        db.session.commit()
   
    def eliminar(self,id):
       objeto=self.consultar(id)
       db.session.delete(objeto)
       db.session.commit()

    def consultarCliente(self):
        cliente = Clientes()
        cliente = cliente.consultar(self.idCliente)
        return cliente.getNombre() + (cliente.empresa)

class Mecanicos(db.Model):
    _tablename_='Mecanicos'
    idEmpleado = Column(Integer, primary_key=True)
    nombre = Column(String(25),nullable=False)
    apellidoPaterno = Column(String(20),nullable=False)    
    apellidoMaterno = Column(String(20),nullable=False)    
    fechaNac = Column(Date, nullable= False)
    sexo = Column(String(1),nullable=False)
    telefono = Column(String(12), nullable= False)
    calle = Column(String(30), nullable= False)
    numExt = Column(Integer, nullable= False)
    numInt = Column(String(2), nullable= False)
    colonia = Column(String(20), nullable= False)   
    municipio = Column(String(20), nullable= False)
    estado = Column(String(20), nullable= False)
    cp = Column(String(5), nullable= False)
    fechaContrato = Column(Date, nullable= False)
    puesto = Column(String(20), nullable= False)   
    numSeguroS = Column(String(18))
    rfc = Column(String(13))

    def registrar(self):
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        db.session.delete(objeto)
        db.session.commit()

class Productos(db.Model):
    _tablename_ = 'productos'
    idProducto = Column(Integer, primary_key=True)
    nombre = Column(String(25), nullable= False)
    marca = Column(String(25), nullable= False)   
    modelo = Column(String(25), nullable= False)   
    tipo = Column(String(25), nullable= False)
    anaquel = Column(Integer, nullable= False)
    estante = Column(Integer, nullable= False)
    costo = Column(Float,nullable= False)
    precio = Column(Float,nullable= False)
    descripcion = Column(String(300),unique=False)    
    unidades = Column(Integer, nullable= False)

    def registrar(self):        
        db.session.add(self)
        db.session.commit()
    
    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultarPrecio(self,id):
        salida={"estatus":"","precio":"","cantidad":""}        
        producto = self.query.get(id)
        if producto!=None:
            salida["estatus"]="OK"
            salida["precio"]= producto.precio
            salida["cantidad"]= producto.unidades
        else:
            salida["estatus"]="ERROR"
            salida["precio"]="Producto no encontrado"
            salida["cantidad"]= 0
        return salida

    def restarUnidades(self,cantidad):
        self.unidades -= cantidad
        db.session.merge(self)
        db.session.commit()
