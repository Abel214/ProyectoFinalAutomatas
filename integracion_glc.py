#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integración de GLC para Reconocimiento de Voz con el proyecto principal
Proyecto Final - Autómatas y Lenguajes Formales
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

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
    
    @app.route('/glc')
    def glc_index():
        """Página principal del analizador GLC"""
        return render_template('glc/index.html')
    
    @app.route('/glc/arbol')
    def mostrar_arbol_voz():
        """Muestra el árbol de reconocimiento de voz"""
        return render_template('glc/arbol.html', 
                             mensaje_validez="Árbol de ejemplo cargado",
                             reglas_usadas=[])
    
    @app.route('/glc/analizar', methods=['POST'])
    def analizar_comando_voz():
        """
        Analiza un comando de voz y devuelve el resultado
        """
        if not AnalizadorGramaticaVisual:
            return jsonify({
                'error': 'Módulo GLC no disponible',
                'valido': False
            }), 500
            
        try:
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
            
            resultado = {
                'comando': comando,
                'valido': analizador.es_valido(),
                'tokens': analizador.tokens,
                'derivacion': analizador.proceso_arbol,
                'reglas_usadas': analizador.reglas_usadas,
                'arbol': analizador.arbol
            }
            
            return jsonify(resultado)
            
        except Exception as e:
            return jsonify({
                'error': f'Error al procesar comando: {str(e)}',
                'valido': False
            }), 500
    
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

# Solo funciones de integración, sin demo
