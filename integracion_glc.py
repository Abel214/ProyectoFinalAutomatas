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

    @app.route('/glc/automata_dinamico')
    def mostrar_automata_dinamico():
        """Muestra el autómata dinámico construido por comandos válidos"""
        inicializar_historial()
        
        # Obtener comandos válidos del historial
        historial = session.get('historial_comandos', [])
        comandos_validos = [cmd for cmd in historial if cmd.get('valido', False)]
        
        return render_template('glc/automata_dinamico.html',
                             comandos_validos=comandos_validos,
                             total_comandos_validos=len(comandos_validos),
                             ultimo_comando=session.get('ultimo_comando', None))
    
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
        """Obtiene el historial de comandos válidos e inválidos de la sesión"""
        inicializar_historial()
        historial = session.get('historial_comandos', [])
        
        # Filtrar solo comandos válidos para el endpoint /glc/historial
        historial_valido = [cmd for cmd in historial if cmd.get('valido', False)]
        
        return jsonify({
            'historial': historial_valido,
            'ultimo_comando': session.get('ultimo_comando', None),
            'total': len(historial_valido),
            'mensaje': f'Mostrando {len(historial_valido)} comandos válidos'
        })

    @app.route('/glc/historial_completo')
    def obtener_historial_completo():
        """Obtiene el historial completo de comandos (válidos e inválidos) de la sesión"""
        inicializar_historial()
        historial = session.get('historial_comandos', [])
        
        return jsonify({
            'historial': historial,
            'ultimo_comando': session.get('ultimo_comando', None),
            'total': len(historial),
            'validos': len([cmd for cmd in historial if cmd.get('valido', False)]),
            'invalidos': len([cmd for cmd in historial if not cmd.get('valido', False)]),
            'mensaje': f'Mostrando {len(historial)} comandos totales'
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

    @app.route('/glc/construir_automata', methods=['POST'])
    def construir_automata():
        """Construye el autómata dinámicamente basado en comandos válidos"""
        try:
            inicializar_historial()
            
            # Obtener comandos válidos del historial
            historial = session.get('historial_comandos', [])
            comandos_validos = [cmd for cmd in historial if cmd.get('valido', False)]
            
            # Construir estructura del autómata dinámico
            automata_dinamico = _construir_estructura_automata(comandos_validos)
            
            return jsonify({
                'success': True,
                'automata': automata_dinamico,
                'total_comandos': len(comandos_validos),
                'mensaje': f'Autómata construido con {len(comandos_validos)} comandos válidos'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error al construir autómata: {str(e)}'
            }), 500

    def _construir_estructura_automata(comandos_validos):
        """Construye la estructura del autómata basado en comandos válidos"""
        nodes = []
        edges = []
        node_id = 0
        
        # Estado inicial
        nodes.append({
            'id': node_id,
            'label': 'q₀\n(Inicio)',
            'color': '#2ECC71',
            'font': {'size': 16, 'color': '#1A1A1A'},
            'shape': 'circle',
            'title': 'Estado inicial del autómata',
            'tipo': 'inicial'
        })
        
        estado_actual = node_id
        node_id += 1
        
        # Procesar cada comando válido secuencialmente
        for i, comando_info in enumerate(comandos_validos):
            comando = comando_info.get('comando', '').lower().strip()
            tokens = comando_info.get('tokens', [])
            timestamp = comando_info.get('timestamp', '')
            
            # Determinar tipo de comando y crear nodo correspondiente
            nuevo_estado = _crear_nodo_por_comando(comando, tokens, node_id, timestamp)
            nodes.append(nuevo_estado)
            
            # Crear transición desde el estado actual
            edge = {
                'from': estado_actual,
                'to': node_id,
                'label': comando,
                'arrows': 'to',
                'color': {'color': _obtener_color_por_comando(comando)},
                'width': 2,
                'font': {'size': 12, 'align': 'middle'},
                'title': f'Transición #{i+1}: {comando} ({timestamp})'
            }
            edges.append(edge)
            
            estado_actual = node_id
            node_id += 1
        
        # Si hay comandos, crear estado final
        if comandos_validos:
            estado_final = {
                'id': node_id,
                'label': f'q{node_id}\n(Final)',
                'color': '#E74C3C',
                'font': {'size': 16, 'color': '#1A1A1A'},
                'shape': 'doublecircle',
                'title': f'Estado final - Procesados {len(comandos_validos)} comandos',
                'tipo': 'final'
            }
            nodes.append(estado_final)
            
            # Transición al estado final
            edges.append({
                'from': estado_actual,
                'to': node_id,
                'label': 'λ (fin)',
                'arrows': 'to',
                'color': {'color': '#BDC3C7'},
                'width': 1,
                'dashes': True,
                'font': {'size': 10, 'align': 'middle'}
            })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'stats': {
                'total_nodos': len(nodes),
                'total_transiciones': len(edges),
                'comandos_procesados': len(comandos_validos)
            }
        }

    def _crear_nodo_por_comando(comando, tokens, node_id, timestamp):
        """Crea un nodo específico según el tipo de comando"""
        # Clasificar comando por categoría
        if comando in ['izquierda', 'derecha', 'arriba', 'abajo']:
            return {
                'id': node_id,
                'label': f'q{node_id}\n({comando})',
                'color': '#3498DB',
                'font': {'size': 14, 'color': '#1A1A1A'},
                'shape': 'circle',
                'title': f'Movimiento: {comando}\nTiempo: {timestamp}',
                'tipo': 'movimiento',
                'comando': comando
            }
        elif 'puerta' in comando:
            puerta = comando.split()[-1] if len(comando.split()) > 1 else 'X'
            return {
                'id': node_id,
                'label': f'q{node_id}\n(Puerta {puerta.upper()})',
                'color': '#9B59B6',
                'font': {'size': 14, 'color': '#1A1A1A'},
                'shape': 'hexagon',
                'title': f'Selección de puerta: {puerta.upper()}\nTiempo: {timestamp}',
                'tipo': 'puerta',
                'comando': comando
            }
        elif comando in ['cambiar', 'mantener']:
            return {
                'id': node_id,
                'label': f'q{node_id}\n({comando})',
                'color': '#F39C12',
                'font': {'size': 14, 'color': '#1A1A1A'},
                'shape': 'diamond',
                'title': f'Acción Monty Hall: {comando}\nTiempo: {timestamp}',
                'tipo': 'accion',
                'comando': comando
            }
        elif 'nueva' in comando or 'partida' in comando:
            return {
                'id': node_id,
                'label': f'q{node_id}\n(Reset)',
                'color': '#E67E22',
                'font': {'size': 14, 'color': '#1A1A1A'},
                'shape': 'star',
                'title': f'Nueva partida\nTiempo: {timestamp}',
                'tipo': 'control',
                'comando': comando
            }
        else:
            return {
                'id': node_id,
                'label': f'q{node_id}\n({comando[:8]}...)',
                'color': '#95A5A6',
                'font': {'size': 12, 'color': '#1A1A1A'},
                'shape': 'ellipse',
                'title': f'Comando: {comando}\nTiempo: {timestamp}',
                'tipo': 'generico',
                'comando': comando
            }

    def _obtener_color_por_comando(comando):
        """Obtiene color de transición según el comando"""
        colores = {
            'izquierda': '#1ABC9C',
            'derecha': '#1ABC9C', 
            'arriba': '#1ABC9C',
            'abajo': '#1ABC9C',
            'puerta a': '#9B59B6',
            'puerta b': '#9B59B6',
            'puerta c': '#9B59B6',
            'cambiar': '#F39C12',
            'mantener': '#F39C12',
            'nueva partida': '#E67E22',
            'nueva': '#E67E22'
        }
        return colores.get(comando, '#2B7CE9')

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
