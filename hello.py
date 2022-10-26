from flask import Flask

app =Flask(__name__)

#crear una url base para nuestros servicios
@app.route('/')
def inicio():
    return '<h1> hola desde Flask 2</h1>' 