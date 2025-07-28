from flask import Flask, render_template
import os
import sys
from datetime import datetime

from integracionAutomata import integrar_rutas

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'glc'))
from integracion_glc import integrar_rutas_glc

# Crear la aplicación Flask con rutas personalizadas
app = Flask(__name__,
            template_folder='frontend/templates', 
            static_folder='frontend/static')      

# Configuración básica
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutos

# Ruta principal - conecta con index.html
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el laberinto - conecta con laberinto.html
@app.route('/laberinto')
def laberinto():
    return render_template('laberintoMonty.html')

# Ejemplo de ruta con datos dinámicos

# Integrar las rutas de GLC
integrar_rutas_glc(app)
integrar_rutas(app)
# Manejo de errores 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404

if __name__ == '__main__':
    app.run(debug=True)