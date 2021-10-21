from flask import Flask,render_template,request

app=Flask(__name__,template_folder='../pages',static_folder='../static')

@app.route('/')
def incio():    
    return  render_template('inicio/inicio.html')

@app.route('/login')
def login():    
    return  render_template('login/login.html')

@app.route('/servicios')
def servicios():    
    return  render_template('servicios/servicios.html')  

@app.route('/registrarServicio')
def registrarServicio():    
    return  render_template('servicios/servicios-registrar.html') 

@app.route('/editarServicio')
def editarServicio():    
    return  render_template('servicios/servicios-editar.html')    

if __name__=='__main__':
    app.run(debug=True)