from flask import Flask, render_template, jsonify, request
import os

# Importar la integración GLC
from integracion_glc import integrar_rutas_glc

# Importar la integración AFND
from integracion_afnd import IntegracionAFND

# Crear la aplicación Flask con rutas personalizadas
app = Flask(__name__,
            template_folder='frontend/templates',  # Especifica la carpeta de templates
            static_folder='frontend/static')       # También para archivos estáticos si los tienes

# Configuración básica
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutos

# Instancia global del AFND
afnd_integracion = IntegracionAFND()

# Ruta principal - conecta con index.html
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el laberinto - conecta con laberinto.html
@app.route('/laberinto')
def laberinto():
    return render_template('laberintoMonty.html')

# Rutas para el AFND
@app.route('/automata')
def mostrar_automata():
    """Muestra la visualización del autómata"""
    ruta_automata = afnd_integracion.generar_automata_html()
    if ruta_automata:
        return render_template('automata_juego.html')
    else:
        return "Error al generar el autómata", 500

@app.route('/api/procesar_comando', methods=['POST'])
def procesar_comando_api():
    """API para procesar comandos de voz y actualizar el AFND"""
    try:
        data = request.get_json()
        comando = data.get('comando', '')
        
        if not comando:
            return jsonify({'error': 'Comando vacío'}), 400
        
        resultado = afnd_integracion.procesar_comando_voz(comando)
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/automata/datos')
def obtener_datos_automata_api():
    """API para obtener los datos del autómata"""
    try:
        datos = afnd_integracion.obtener_datos_automata()
        return jsonify(datos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/automata/historial')
def obtener_historial_automata():
    """API para obtener el historial de comandos del autómata"""
    try:
        historial = afnd_integracion.obtener_historial_sesion()
        return jsonify(historial)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/automata/reiniciar', methods=['POST'])
def reiniciar_automata_api():
    """API para reiniciar el autómata"""
    try:
        afnd_integracion.reiniciar_sesion()
        return jsonify({'mensaje': 'Autómata reiniciado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ejemplo de ruta con datos dinámicos

# Integrar las rutas de GLC
integrar_rutas_glc(app)


# Manejo de errores 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404

if __name__ == '__main__':
    app.run(debug=True)