from flask import Flask,render_template,request

app=Flask(__name__,template_folder='../pages',static_folder='../static')

@app.route('/')
def incio():    
    return  render_template('inicio/inicio.html')


if __name__=='__main__':
    app.run(debug=True)