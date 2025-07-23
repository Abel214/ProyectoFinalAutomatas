from flask import render_template, request, jsonify, session
from datetime import datetime
import os
import sys

# Añadir rutas al sys.path si es necesario
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'glc'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'automata'))

# Intentar importar módulos
try:
    from backend.glc.logicaGLC import AnalizadorGramaticaVisual
    from backend.automata.automataLogica import JuegoLaberintoMontyHall
except ImportError:
    AnalizadorGramaticaVisual = None
    JuegoLaberintoMontyHall = None

# Instancia del juego
juego = JuegoLaberintoMontyHall() if JuegoLaberintoMontyHall else None


def inicializar_historial_Automata():
    if 'historial_comandos' not in session:
        session['historial_comandos'] = []
    if 'ultimo_comando' not in session:
        session['ultimo_comando'] = ''


def integrar_rutas(app):
    @app.route('/automata/arbol')
    def mostrar_arbol_voz_Automata():
        inicializar_historial_Automata()
        ultimo_comando = session.get('ultimo_comando', 'puerta a')
        historial = session.get('historial_comandos', [])

        return render_template('glc/automata.html',
                               mensaje_validez="",
                               ultimo_comando=ultimo_comando,
                               historial_comandos=historial,
                               total_comandos=len(historial),
                               reglas_usadas=[])

    @app.route('/automata/analizar', methods=['POST'])
    def analizar_comando_voz_Automata():
        if not AnalizadorGramaticaVisual or not juego:
            return jsonify({'error': 'Módulos requeridos no disponibles', 'valido': False}), 500

        try:
            inicializar_historial_Automata()
            datos = request.get_json()
            comando = datos.get('comando', '').strip().lower()

            if not comando:
                return jsonify({'error': 'Comando vacío', 'valido': False})

            analizador = AnalizadorGramaticaVisual(auto_abrir=False)
            analizador.procesar_cadena(comando)
            es_valido_gramatical = analizador.es_valido()

            resultado_juego = None
            if es_valido_gramatical:
                exito, mensaje = juego.procesar_comando(comando)
                resultado_juego = {
                    'exito': exito,
                    'mensaje': mensaje,
                    'estado_actual': list(juego.afn.estado_actual),
                    'puerta_premiada': juego.afn.puerta_premiada,
                    'puerta_seleccionada': juego.afn.puerta_seleccionada,
                    'estadisticas': juego.afn.estadisticas
                }

            entrada_historial = {
                'comando': comando,
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'valido_gramatical': es_valido_gramatical,
                'procesado_juego': es_valido_gramatical,
                'resultado_juego': resultado_juego if es_valido_gramatical else None,
                'derivacion': analizador.proceso_arbol if es_valido_gramatical else [],
                'tokens': analizador.tokens if es_valido_gramatical else comando.split(' '),
                'reglas_usadas': analizador.reglas_usadas if es_valido_gramatical else []
            }

            historial = session.get('historial_comandos', [])
            historial.append(entrada_historial)
            session['historial_comandos'] = historial[-20:]
            session['ultimo_comando'] = comando
            session.permanent = True

            respuesta = {
                'analisis_gramatical': {
                    'comando': comando,
                    'valido': es_valido_gramatical,
                    'tokens': analizador.tokens,
                    'derivacion': analizador.proceso_arbol,
                    'reglas_usadas': analizador.reglas_usadas,
                    'arbol': analizador.arbol
                },
                'estado_juego': resultado_juego,
                'historial': {
                    'total_comandos': len(historial),
                    'ultimo_comando': comando
                }
            }

            return jsonify(respuesta)

        except Exception as e:
            return jsonify({'error': f'Error al procesar comando: {str(e)}', 'valido': False}), 500

    @app.route('/automata/estado_juego')
    def obtener_estado_juego_Automata():
        historial = session.get('historial_comandos', [])
        return jsonify({
            'historial': historial,
            'total_entradas': len(historial),
            'estadisticas': juego.afn.estadisticas if juego else {},
            'puerta_premiada': juego.afn.puerta_premiada if juego else None,
            'puerta_seleccionada': juego.afn.puerta_seleccionada if juego else None,
        })

    @app.route('/automata/estado', methods=['GET'])
    def obtener_historial_y_estado():
        if not juego:
            return jsonify({'error': 'Juego no inicializado'}), 500

        historial = session.get('historial_comandos', [])
        historial_transformado = []

        for i, entrada in enumerate(historial):
            # Debugging: imprimir la estructura de cada entrada
            print(f"Entrada {i}: {entrada}")

            resultado = entrada.get('resultado_juego', {})

            # Mejorar la obtención del comando
            comando = entrada.get('comando')
            if comando is None or comando == '':
                comando = f"Comando #{i + 1} (sin datos)"

            # Obtener estado de manera más robusta
            estado_actual = []
            if resultado and 'estado_actual' in resultado:
                estado_actual = resultado['estado_actual']
            elif 'estado_actual' in entrada:
                estado_actual = entrada['estado_actual']

            # Determinar resultado de manera más precisa
            resultado_final = None
            if resultado:
                if resultado.get('exito') is True:
                    resultado_final = 'éxito'
                elif resultado.get('exito') is False:
                    resultado_final = 'fracaso'
                elif entrada.get('valido_gramatical') is False:
                    resultado_final = 'error gramatical'

            historial_transformado.append({
                'entrada': comando,
                'estado': estado_actual,
                'resultado': resultado_final,
                'timestamp': entrada.get('timestamp', 'N/A'),
                'valido_gramatical': entrada.get('valido_gramatical', False),
                'mensaje': resultado.get('mensaje', '') if resultado else ''
            })

        return jsonify({
            'historial': historial_transformado,
            'estadisticas': juego.afn.estadisticas,
            'puerta_premiada': juego.afn.puerta_premiada,
            'puerta_seleccionada': juego.afn.puerta_seleccionada,
            'total_entradas': len(historial)
        })

    @app.route('/automata/reiniciar', methods=['POST'])
    def reiniciar_juego_automata():
        if not juego:
            return jsonify({'error': 'Juego no inicializado'}), 500

        juego.reiniciar()  # Asegúrate que tu clase JuegoLaberintoMontyHall tenga este método
        session['historial_comandos'] = []
        session['ultimo_comando'] = ''
        return jsonify({'exito': True})
