#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integración de GLC para Reconocimiento de Voz con el proyecto principal
Proyecto Final - Autómatas y Lenguajes Formales
"""

from flask import render_template, request, jsonify, session
import sys
import os
from datetime import datetime

# Añadir el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'glc'))

try:
    from backend.glc.logicaGLC import AnalizadorGramaticaVisual
except ImportError:
    # Fallback si no se puede importar
    print("⚠️ No se pudo importar el módulo GLC")
    AnalizadorGramaticaVisual = None

def integrar_rutas_glc(app):
    """
    Integra las rutas de GLC al app principal de Flask

    Args:
        app: Instancia de Flask
    """

    # Inicializar historial de comandos en la sesión
    def inicializar_historial():
        if 'historial_comandos' not in session:
            session['historial_comandos'] = []
        if 'ultimo_comando' not in session:
            session['ultimo_comando'] = None

    @app.route('/glc/arbol')
    def mostrar_arbol_voz():
        """Muestra el árbol de reconocimiento de voz con el último comando"""
        inicializar_historial()

        # Obtener último comando o usar ejemplo por defecto
        ultimo_comando = session.get('ultimo_comando', 'puerta a')
        historial = session.get('historial_comandos', [])

        return render_template('glc/arbol.html',
                             mensaje_validez="",
                             ultimo_comando=ultimo_comando,
                             historial_comandos=historial,
                             total_comandos=len(historial),
                             reglas_usadas=[])

    @app.route('/glc/arbol/<comando>')
    def mostrar_arbol_comando_especifico(comando):
        """Muestra el árbol para un comando específico"""
        return render_template('glc/arbol.html',
                             mensaje_validez="",
                             ultimo_comando=comando,
                             historial_comandos=session.get('historial_comandos', []),
                             total_comandos=len(session.get('historial_comandos', [])),
                             reglas_usadas=[])

    @app.route('/glc/analizar', methods=['POST'])
    def analizar_comando_voz():
        """
        Analiza un comando de voz y devuelve el resultado
        También guarda el comando en el historial de la sesión
        """
        if not AnalizadorGramaticaVisual:
            return jsonify({
                'error': 'Módulo GLC no disponible',
                'valido': False
            }), 500

        try:
            inicializar_historial()
            datos = request.get_json()
            comando = datos.get('comando', '').strip().lower()

            if not comando:
                return jsonify({
                    'error': 'Comando vacío',
                    'valido': False
                })

            # Crear analizador
            analizador = AnalizadorGramaticaVisual(auto_abrir=False)

            # Procesar comando
            analizador.procesar_cadena(comando)
            analizador.construir_arbol()

            # Generar derivación
            analizador.generar_proceso_desde_arbol()

            es_valido = analizador.es_valido()

            # Guardar en historial TODOS los comandos (válidos e inválidos)
            historial = session.get('historial_comandos', [])

            # Verificar si es comando "nueva partida" para resetear historial DESPUÉS de procesarlo
            comando_limpio = comando.lower().strip()
            if comando_limpio in ['nueva partida', 'nueva']:
                # Resetear historial completamente DESPUÉS de procesar
                historial = []
                session['historial_comandos'] = []
                session['ultimo_comando'] = None

            # Agregar comando con timestamp
            entrada_historial = {
                'comando': comando,
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'derivacion': analizador.proceso_arbol if es_valido else [],
                'tokens': analizador.tokens if es_valido else comando.split(' '),
                'reglas_usadas': analizador.reglas_usadas if es_valido else [],
                'valido': es_valido
            }

            historial.append(entrada_historial)

            # Mantener solo los últimos 20 comandos
            if len(historial) > 20:
                historial = historial[-20:]

            session['historial_comandos'] = historial
            session['ultimo_comando'] = comando
            session.permanent = True

            resultado = {
                'comando': comando,
                'valido': es_valido,
                'tokens': analizador.tokens,
                'derivacion': analizador.proceso_arbol,
                'reglas_usadas': analizador.reglas_usadas,
                'arbol': analizador.arbol,
                'total_comandos_sesion': len(session.get('historial_comandos', []))
            }

            return jsonify(resultado)

        except Exception as e:
            return jsonify({
                'error': f'Error al procesar comando: {str(e)}',
                'valido': False
            }), 500

    @app.route('/glc/historial')
    def obtener_historial():
        """Obtiene el historial de comandos de la sesión"""
        inicializar_historial()
        return jsonify({
            'historial': session.get('historial_comandos', []),
            'ultimo_comando': session.get('ultimo_comando', None),
            'total': len(session.get('historial_comandos', []))
        })

    @app.route('/glc/limpiar_historial', methods=['POST'])
    def limpiar_historial():
        """Limpia el historial de comandos"""
        session['historial_comandos'] = []
        session['ultimo_comando'] = None
        return jsonify({'mensaje': 'Historial limpiado', 'exito': True})

    @app.route('/glc/comandos')
    def listar_comandos():
        """Lista todos los comandos reconocidos"""
        comandos = {
            'movimiento': ['izquierda', 'derecha', 'arriba', 'abajo'],
            'monty_hall': {
                'puertas': ['puerta a', 'puerta b', 'puerta c'],
                'acciones': ['cambiar', 'mantener'],
                'control': ['cerrar', 'reiniciar', 'otra vez']
            },
            'juego': ['nueva partida']
        }

        return jsonify(comandos)

    @app.route('/glc/gramatica')
    def mostrar_gramatica():
        """Devuelve la gramática utilizada"""
        if not AnalizadorGramaticaVisual:
            return jsonify({'error': 'Módulo GLC no disponible'}), 500

        # Crear instancia temporal para obtener la gramática
        analizador = AnalizadorGramaticaVisual(auto_abrir=False)

        gramatica = {
            'reglas': analizador.GRAMATICA,
            'descripcion': 'Gramática Libre de Contexto para Reconocimiento de Voz',
            'simbolo_inicial': 'S',
            'no_terminales': [
                'S', 'comando', 'movimiento', 'monty', 'juego',
                'puerta', 'puerta_a', 'puerta_b', 'puerta_c',
                'accion', 'control', 'nueva'
            ],
            'terminales': [
                'izquierda', 'derecha', 'arriba', 'abajo',
                'puerta', 'a', 'b', 'c', 'cambiar', 'mantener',
                'cerrar', 'reiniciar', 'otra', 'vez', 'nueva', 'partida'
            ]
        }

        return jsonify(gramatica)

    @app.route('/glc/reset_nueva_partida', methods=['POST'])
    def reset_nueva_partida():
        """Resetea el historial cuando inicia una nueva partida"""
        try:
            session['historial_comandos'] = []
            session['ultimo_comando'] = None
            session.permanent = True
            
            return jsonify({
                'success': True,
                'mensaje': 'Historial reseteado para nueva partida'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'mensaje': f'Error al resetear historial: {str(e)}'
            })
