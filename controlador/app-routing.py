from flask import Flask,render_template,request

app=Flask(__name__,template_folder='../pages',static_folder='../static')

@app.route('/')
def incio():    
    return  render_template('inicio/inicio.html')

@app.route('/login')
def login():    
    return  render_template('login/login.html')

@app.route('/autos')
def autos():    
    return  render_template('autos/autos.html')    

@app.route('/formularioAutos')
def registrarAuto():    
    return  render_template('autos/autos-formulario.html')  

  

if __name__=='__main__':
    app.run(debug=True)