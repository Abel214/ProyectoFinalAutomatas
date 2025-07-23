import os
import json
from datetime import datetime

class AutomataFinito:
    def __init__(self):
        self.estados = []
        self.transiciones = []
        self.estado_inicial = None
        self.estados_finales = []
        self.alfabeto = set()
        self.contador_estados = 0
        self.historial_comandos = []
        self.estado_actual = None
        self.juego_activo = False
        self.monty_hall_activo = False
        self.puerta_seleccionada = None
        self.resultado_monty = None
        
        # Inicializar el autómata con el estado inicial
        self._inicializar_automata()
    
    def _inicializar_automata(self):
        """Inicializa el autómata con el estado inicial del juego"""
        estado_inicio = {
            'id': self.contador_estados,
            'nombre': 'INICIO',
            'descripcion': 'Estado inicial del juego',
            'tipo': 'inicial',
            'es_final': False,
            'posicion': {'x': 100, 'y': 100}
        }
        
        self.estados.append(estado_inicio)
        self.estado_inicial = estado_inicio['id']
        self.estado_actual = estado_inicio['id']
        self.contador_estados += 1
    
    def procesar_comando(self, comando_texto, es_valido=True):
        """Procesa un comando de voz y actualiza el autómata"""
        if not es_valido:
            return self._crear_estado_error(comando_texto)
        
        comando_info = {
            'comando': comando_texto,
            'timestamp': datetime.now().isoformat(),
            'estado_origen': self.estado_actual
        }
        
        # Determinar el tipo de comando
        tokens = comando_texto.lower().split()
        
        if any(mov in tokens for mov in ['izquierda', 'derecha', 'arriba', 'abajo']):
            nuevo_estado = self._procesar_movimiento(tokens)
        elif 'puerta' in tokens:
            nuevo_estado = self._procesar_seleccion_puerta(tokens)
        elif any(accion in tokens for accion in ['cambiar', 'mantener']):
            nuevo_estado = self._procesar_accion_monty(tokens)
        elif any(control in tokens for control in ['cerrar', 'reiniciar']):
            nuevo_estado = self._procesar_control(tokens)
        elif 'nueva' in tokens and 'partida' in tokens:
            nuevo_estado = self._reiniciar_juego()
        else:
            nuevo_estado = self._crear_estado_error(comando_texto)
        
        # Crear transición
        if nuevo_estado:
            self._crear_transicion(self.estado_actual, nuevo_estado['id'], comando_texto)
            self.estado_actual = nuevo_estado['id']
            comando_info['estado_destino'] = nuevo_estado['id']
            comando_info['resultado'] = 'exitoso'
        else:
            comando_info['resultado'] = 'error'
        
        self.historial_comandos.append(comando_info)
        return nuevo_estado
    
    def _procesar_movimiento(self, tokens):
        """Procesa comandos de movimiento"""
        direccion = None
        for token in tokens:
            if token in ['izquierda', 'derecha', 'arriba', 'abajo']:
                direccion = token
                break
        
        if not direccion:
            return None
        
        # Calcular nueva posición basada en la dirección
        estado_origen = self._obtener_estado_por_id(self.estado_actual)
        nueva_pos = self._calcular_nueva_posicion(estado_origen['posicion'], direccion)
        
        # Verificar si llegamos a una zona especial (Monty Hall)
        es_zona_monty = self._es_zona_monty_hall(nueva_pos)
        
        nombre_estado = f"POS_{direccion.upper()}"
        descripcion = f"Movimiento hacia {direccion}"
        
        if es_zona_monty:
            nombre_estado = "ZONA_MONTY"
            descripcion = "Entrada a zona Monty Hall"
            self.monty_hall_activo = True
        
        nuevo_estado = {
            'id': self.contador_estados,
            'nombre': nombre_estado,
            'descripcion': descripcion,
            'tipo': 'movimiento',
            'es_final': False,
            'posicion': nueva_pos,
            'direccion': direccion,
            'es_zona_monty': es_zona_monty
        }
        
        self.estados.append(nuevo_estado)
        self.alfabeto.add(direccion)
        self.contador_estados += 1
        
        return nuevo_estado
    
    def _procesar_seleccion_puerta(self, tokens):
        """Procesa la selección de puertas en Monty Hall"""
        if not self.monty_hall_activo:
            return None
        
        puerta = None
        for token in tokens:
            if token in ['a', 'b', 'c']:
                puerta = token.upper()
                break
        
        if not puerta:
            return None
        
        self.puerta_seleccionada = puerta
        
        nuevo_estado = {
            'id': self.contador_estados,
            'nombre': f"PUERTA_{puerta}",
            'descripcion': f"Seleccionó puerta {puerta}",
            'tipo': 'seleccion_puerta',
            'es_final': False,
            'posicion': self._calcular_posicion_puerta(puerta),
            'puerta': puerta
        }
        
        self.estados.append(nuevo_estado)
        self.alfabeto.add(f"puerta_{puerta.lower()}")
        self.contador_estados += 1
        
        return nuevo_estado
    
    def _procesar_accion_monty(self, tokens):
        """Procesa las acciones de cambiar o mantener en Monty Hall"""
        if not self.puerta_seleccionada:
            return None
        
        accion = None
        for token in tokens:
            if token in ['cambiar', 'mantener']:
                accion = token
                break
        
        if not accion:
            return None
        
        # Simular resultado del juego Monty Hall
        resultado = self._simular_resultado_monty(accion)
        self.resultado_monty = resultado
        
        nombre_estado = f"ACCION_{accion.upper()}"
        if resultado == 'ganador':
            nombre_estado += "_GANADOR"
            descripcion = f"Acción: {accion} - ¡GANASTE!"
            es_final = True
            tipo_estado = 'victoria'
        else:
            nombre_estado += "_PERDEDOR"
            descripcion = f"Acción: {accion} - Perdiste"
            es_final = False
            tipo_estado = 'derrota'
        
        nuevo_estado = {
            'id': self.contador_estados,
            'nombre': nombre_estado,
            'descripcion': descripcion,
            'tipo': tipo_estado,
            'es_final': es_final,
            'posicion': self._calcular_posicion_resultado(resultado),
            'accion': accion,
            'resultado': resultado
        }
        
        self.estados.append(nuevo_estado)
        self.alfabeto.add(accion)
        self.contador_estados += 1
        
        if es_final:
            self.estados_finales.append(nuevo_estado['id'])
        
        return nuevo_estado
    
    def _procesar_control(self, tokens):
        """Procesa comandos de control como cerrar o reiniciar"""
        control = None
        for token in tokens:
            if token in ['cerrar', 'reiniciar']:
                control = token
                break
        
        if not control:
            return None
        
        if control == 'cerrar':
            nuevo_estado = {
                'id': self.contador_estados,
                'nombre': 'JUEGO_CERRADO',
                'descripcion': 'Juego terminado por el usuario',
                'tipo': 'control',
                'es_final': True,
                'posicion': {'x': 500, 'y': 500}
            }
            self.estados_finales.append(self.contador_estados)
        else:  # reiniciar
            # Si perdió en Monty Hall, puede reiniciar desde la zona Monty
            if self.resultado_monty == 'perdedor':
                nuevo_estado = {
                    'id': self.contador_estados,
                    'nombre': 'REINICIO_MONTY',
                    'descripcion': 'Reinicio desde zona Monty Hall',
                    'tipo': 'control',
                    'es_final': False,
                    'posicion': {'x': 300, 'y': 200}
                }
                self.monty_hall_activo = True
                self.puerta_seleccionada = None
                self.resultado_monty = None
            else:
                nuevo_estado = {
                    'id': self.contador_estados,
                    'nombre': 'REINICIO_COMPLETO',
                    'descripcion': 'Reinicio del juego completo',
                    'tipo': 'control',
                    'es_final': False,
                    'posicion': {'x': 100, 'y': 100}
                }
        
        self.estados.append(nuevo_estado)
        self.alfabeto.add(control)
        self.contador_estados += 1
        
        return nuevo_estado
    
    def _reiniciar_juego(self):
        """Reinicia completamente el juego"""
        nuevo_estado = {
            'id': self.contador_estados,
            'nombre': 'NUEVA_PARTIDA',
            'descripcion': 'Nueva partida iniciada',
            'tipo': 'control',
            'es_final': False,
            'posicion': {'x': 100, 'y': 100}
        }
        
        self.estados.append(nuevo_estado)
        self.alfabeto.add('nueva_partida')
        self.contador_estados += 1
        
        # Reset del estado del juego
        self.monty_hall_activo = False
        self.puerta_seleccionada = None
        self.resultado_monty = None
        
        return nuevo_estado
    
    def _crear_estado_error(self, comando):
        """Crea un estado de error para comandos inválidos"""
        nuevo_estado = {
            'id': self.contador_estados,
            'nombre': 'ERROR',
            'descripcion': f'Comando inválido: {comando}',
            'tipo': 'error',
            'es_final': False,
            'posicion': {'x': 50, 'y': 50},
            'comando_error': comando
        }
        
        self.estados.append(nuevo_estado)
        self.contador_estados += 1
        
        return nuevo_estado
    
    def _crear_transicion(self, estado_origen, estado_destino, simbolo):
        """Crea una transición entre dos estados"""
        transicion = {
            'origen': estado_origen,
            'destino': estado_destino,
            'simbolo': simbolo,
            'timestamp': datetime.now().isoformat()
        }
        
        self.transiciones.append(transicion)
    
    def _obtener_estado_por_id(self, estado_id):
        """Obtiene un estado por su ID"""
        for estado in self.estados:
            if estado['id'] == estado_id:
                return estado
        return None
    
    def _calcular_nueva_posicion(self, pos_actual, direccion):
        """Calcula la nueva posición basada en la dirección"""
        x, y = pos_actual['x'], pos_actual['y']
        
        if direccion == 'derecha':
            x += 150
        elif direccion == 'izquierda':
            x -= 150
        elif direccion == 'arriba':
            y -= 100
        elif direccion == 'abajo':
            y += 100
        
        return {'x': x, 'y': y}
    
    def _es_zona_monty_hall(self, posicion):
        """Determina si una posición está en la zona Monty Hall"""
        # Zona Monty Hall está en el cuadrante superior derecho
        return posicion['x'] >= 400 and posicion['y'] <= 200
    
    def _calcular_posicion_puerta(self, puerta):
        """Calcula la posición para una puerta específica"""
        base_x = 400
        base_y = 150
        
        if puerta == 'A':
            return {'x': base_x, 'y': base_y}
        elif puerta == 'B':
            return {'x': base_x + 100, 'y': base_y}
        else:  # puerta C
            return {'x': base_x + 200, 'y': base_y}
    
    def _calcular_posicion_resultado(self, resultado):
        """Calcula la posición para el resultado del juego"""
        if resultado == 'ganador':
            return {'x': 500, 'y': 100}  # Posición de victoria
        else:
            return {'x': 300, 'y': 300}  # Posición de derrota
    
    def _simular_resultado_monty(self, accion):
        """Simula el resultado del juego Monty Hall"""
        import random
        # Probabilidad real del Monty Hall
        if accion == 'cambiar':
            return 'ganador' if random.random() < 0.67 else 'perdedor'
        else:  # mantener
            return 'ganador' if random.random() < 0.33 else 'perdedor'
    
    def obtener_automata_para_visualizacion(self):
        """Retorna el autómata en formato para visualización"""
        nodos = []
        edges = []
        
        # Convertir estados a nodos
        for estado in self.estados:
            color = self._obtener_color_estado(estado)
            nodo = {
                'id': estado['id'],
                'label': estado['nombre'],
                'title': estado['descripcion'],
                'color': color,
                'x': estado['posicion']['x'],
                'y': estado['posicion']['y'],
                'font': {'size': 12},
                'shape': self._obtener_forma_estado(estado)
            }
            
            # Marcar estado actual
            if estado['id'] == self.estado_actual:
                nodo['borderWidth'] = 4
                nodo['borderColor'] = '#FF0000'
            
            # Marcar estados finales
            if estado['es_final']:
                nodo['borderWidth'] = 3
                nodo['borderColor'] = '#00FF00'
            
            nodos.append(nodo)
        
        # Convertir transiciones a edges
        for transicion in self.transiciones:
            edge = {
                'from': transicion['origen'],
                'to': transicion['destino'],
                'label': transicion['simbolo'],
                'arrows': 'to',
                'color': {'color': '#2B7CE9'},
                'width': 2
            }
            edges.append(edge)
        
        return {
            'nodes': nodos,
            'edges': edges,
            'estado_actual': self.estado_actual,
            'estados_finales': self.estados_finales,
            'historial': self.historial_comandos,
            'estadisticas': self._obtener_estadisticas()
        }
    
    def _obtener_color_estado(self, estado):
        """Obtiene el color para un estado según su tipo"""
        colores = {
            'inicial': '#4CAF50',      # Verde
            'movimiento': '#2196F3',    # Azul
            'seleccion_puerta': '#FF9800',  # Naranja
            'victoria': '#4CAF50',      # Verde
            'derrota': '#F44336',       # Rojo
            'control': '#9C27B0',       # Púrpura
            'error': '#FF5722'          # Rojo oscuro
        }
        return colores.get(estado['tipo'], '#757575')  # Gris por defecto
    
    def _obtener_forma_estado(self, estado):
        """Obtiene la forma para un estado según su tipo"""
        formas = {
            'inicial': 'circle',
            'movimiento': 'box',
            'seleccion_puerta': 'diamond',
            'victoria': 'star',
            'derrota': 'triangle',
            'control': 'hexagon',
            'error': 'box'
        }
        return formas.get(estado['tipo'], 'circle')
    
    def _obtener_estadisticas(self):
        """Obtiene estadísticas del autómata"""
        return {
            'total_estados': len(self.estados),
            'total_transiciones': len(self.transiciones),
            'comandos_procesados': len(self.historial_comandos),
            'alfabeto_size': len(self.alfabeto),
            'juego_activo': self.juego_activo,
            'monty_hall_activo': self.monty_hall_activo
        }
    
    def exportar_json(self):
        """Exporta el autómata a formato JSON"""
        return {
            'estados': self.estados,
            'transiciones': self.transiciones,
            'estado_inicial': self.estado_inicial,
            'estados_finales': self.estados_finales,
            'alfabeto': list(self.alfabeto),
            'estado_actual': self.estado_actual,
            'historial_comandos': self.historial_comandos,
            'timestamp': datetime.now().isoformat()
        }


class VisualizadorAFND:
    def __init__(self):
        self.automata = AutomataFinito()
    
    def procesar_comando_y_actualizar(self, comando, es_valido=True):
        """Procesa un comando y actualiza el autómata"""
        return self.automata.procesar_comando(comando, es_valido)
    
    def generar_html_automata(self, archivo_salida="automata.html"):
        """Genera el archivo HTML para visualizar el autómata"""
        data_automata = self.automata.obtener_automata_para_visualizacion()
        
        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Autómata Finito - Reconocimiento de Voz</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" />
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            color: #333;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}

        .info-panel {{
            display: flex;
            padding: 20px;
            gap: 20px;
            background: #f8f9fa;
        }}

        .stats-card {{
            flex: 1;
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}

        .stats-card h3 {{
            margin: 0 0 10px 0;
            color: #667eea;
        }}

        .automata-container {{
            padding: 20px;
        }}

        #automata-network {{
            width: 100%;
            height: 600px;
            background: #ffffff;
            border: 2px solid #ddd;
            border-radius: 10px;
        }}

        .legend {{
            display: flex;
            justify-content: space-around;
            padding: 15px;
            background: #f8f9fa;
            margin: 20px;
            border-radius: 10px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
        }}

        .controls {{
            padding: 20px;
            text-align: center;
        }}

        .btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 10px;
            font-size: 16px;
        }}

        .btn:hover {{
            background: #5a6fd8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Autómata Finito No Determinista</h1>
            <p>Reconocimiento de Voz - Laberinto y Monty Hall</p>
        </div>

        <div class="info-panel">
            <div class="stats-card">
                <h3>📊 Estadísticas</h3>
                <p><strong>Estados:</strong> {data_automata['estadisticas']['total_estados']}</p>
                <p><strong>Transiciones:</strong> {data_automata['estadisticas']['total_transiciones']}</p>
                <p><strong>Comandos:</strong> {data_automata['estadisticas']['comandos_procesados']}</p>
            </div>
            
            <div class="stats-card">
                <h3>🎮 Estado del Juego</h3>
                <p><strong>Estado Actual:</strong> {data_automata['estado_actual']}</p>
                <p><strong>Monty Hall:</strong> {'🟢 Activo' if data_automata['estadisticas']['monty_hall_activo'] else '🔴 Inactivo'}</p>
            </div>
            
            <div class="stats-card">
                <h3>🎯 Alfabeto</h3>
                <p><strong>Símbolos:</strong> {data_automata['estadisticas']['alfabeto_size']}</p>
                <p><small>Comandos reconocidos por el autómata</small></p>
            </div>
        </div>

        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: #4CAF50;"></div>
                <span>Estado Inicial/Victoria</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #2196F3;"></div>
                <span>Movimiento</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #FF9800;"></div>
                <span>Selección Puerta</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #F44336;"></div>
                <span>Derrota</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #9C27B0;"></div>
                <span>Control</span>
            </div>
        </div>

        <div class="automata-container">
            <div id="automata-network"></div>
        </div>

        <div class="controls">
            <button class="btn" onclick="resetZoom()">🔍 Centrar Vista</button>
            <button class="btn" onclick="exportarDatos()">💾 Exportar Datos</button>
            <button class="btn" onclick="window.close()">❌ Cerrar</button>
        </div>
    </div>

    <script>
        // Datos del autómata
        const automataData = {json.dumps(data_automata, indent=4)};
        
        // Crear la red del autómata
        const container = document.getElementById('automata-network');
        const data = {{
            nodes: new vis.DataSet(automataData.nodes),
            edges: new vis.DataSet(automataData.edges)
        }};
        
        const options = {{
            layout: {{
                improvedLayout: false
            }},
            physics: {{
                enabled: false
            }},
            interaction: {{
                dragNodes: true,
                zoomView: true,
                dragView: true
            }},
            nodes: {{
                font: {{
                    size: 14,
                    color: '#ffffff'
                }},
                borderWidth: 2,
                shadow: true
            }},
            edges: {{
                font: {{
                    size: 12,
                    color: '#333333',
                    background: 'rgba(255,255,255,0.8)'
                }},
                smooth: {{
                    type: 'continuous'
                }},
                arrows: {{
                    to: {{
                        enabled: true,
                        scaleFactor: 1.2
                    }}
                }}
            }}
        }};
        
        const network = new vis.Network(container, data, options);
        
        // Funciones de control
        function resetZoom() {{
            network.fit();
        }}
        
        function exportarDatos() {{
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(automataData, null, 2));
            const downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href", dataStr);
            downloadAnchorNode.setAttribute("download", "automata_data.json");
            document.body.appendChild(downloadAnchorNode);
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
        }}
        
        // Resaltar estado actual
        network.on("afterDrawing", function (ctx) {{
            const nodeId = automataData.estado_actual;
            const nodePosition = network.getPositions([nodeId]);
            if (nodePosition[nodeId]) {{
                ctx.strokeStyle = '#FF0000';
                ctx.lineWidth = 4;
                ctx.setLineDash([5, 5]);
                ctx.beginPath();
                ctx.arc(nodePosition[nodeId].x, nodePosition[nodeId].y, 40, 0, 2 * Math.PI);
                ctx.stroke();
                ctx.setLineDash([]);
            }}
        }});
        
        console.log('Autómata cargado:', automataData);
    </script>
</body>
</html>
"""
        
        # Guardar el archivo HTML
        ruta_completa = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'templates', archivo_salida)
        
        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
        
        try:
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True, ruta_completa
        except Exception as e:
            print(f"Error al generar HTML: {e}")
            return False, None
    
    def obtener_automata(self):
        """Retorna la instancia del autómata"""
        return self.automata
