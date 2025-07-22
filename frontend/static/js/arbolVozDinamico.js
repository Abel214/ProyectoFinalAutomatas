// Árbol dinámico de reconocimiento de voz
// Se actualiza según los comandos del usuario

class ArbolVozDinamico {
    constructor() {
        this.network = null;
        this.nodes = new vis.DataSet([]);
        this.edges = new vis.DataSet([]);
        this.comandoActual = 'puerta a'; // Por defecto
        this.historial = [];
    }

    // Inicializar el árbol
    inicializar(ultimoComando = null, historial = []) {
        this.comandoActual = ultimoComando || 'puerta a';
        this.historial = historial || [];
        
        this.generarArbolComando(this.comandoActual);
        this.crearVisualizacion();
        this.actualizarEstadisticas();
    }

    // Método para mostrar un comando específico
    mostrarComando(comando) {
        console.log(`🎯 Mostrando comando específico: "${comando}"`);
        this.comandoActual = comando;
        this.generarArbolComando(comando);
        this.actualizarEstadisticas();
        
        // Actualizar la visualización sin recrear la red
        if (this.network) {
            this.network.setData({
                nodes: this.nodes,
                edges: this.edges
            });
        }
    }

    // Generar árbol para un comando específico siguiendo la gramática exacta
    generarArbolComando(comando) {
        this.nodes.clear();
        this.edges.clear();
        
        // Limpiar el comando de espacios extra, caracteres especiales, etc.
        const comandoLimpio = comando.toLowerCase().trim().replace(/[^\w\s]/g, '');
        const tokens = comandoLimpio.split(/\s+/).filter(token => token.length > 0);
        
        console.log(`🔧 Comando original: "${comando}"`);
        console.log(`🔧 Comando limpio: "${comandoLimpio}"`);
        console.log(`🔧 Tokens: [${tokens.join(', ')}]`);
        
        let nodos = [];
        let aristas = [];
        let idCounter = 0;

        // Nodo raíz S
        nodos.push({
            id: idCounter++,
            label: 'S',
            color: '#E74C3C',
            font: { size: 18, color: 'white', bold: true },
            shape: 'circle',
            size: 30
        });

        // Nodo comando (S → comando)
        nodos.push({
            id: idCounter++,
            label: 'comando',
            color: '#3498DB',
            font: { size: 16, color: 'white' },
            shape: 'circle',
            size: 25
        });

        aristas.push({ from: 0, to: 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 });

        // Determinar el tipo y generar el árbol específico
        const tipoComando = this.determinarTipoComando(comandoLimpio);
        console.log(`🔍 Analizando comando: "${comandoLimpio}" -> Tipo: ${tipoComando}`);
        
        if (tipoComando === 'movimiento') {
            this.generarArbolMovimiento(comandoLimpio, nodos, aristas, idCounter);
        } else if (tipoComando === 'monty') {
            if (comandoLimpio.includes('puerta')) {
                this.generarArbolPuerta(tokens, nodos, aristas, idCounter);
            } else if (['cambiar', 'mantener'].includes(comandoLimpio)) {
                this.generarArbolAccion(comandoLimpio, nodos, aristas, idCounter);
            } else if (['cerrar', 'reiniciar'].includes(comandoLimpio) || comandoLimpio.includes('otra vez')) {
                this.generarArbolControl(tokens, nodos, aristas, idCounter);
            }
        } else if (tipoComando === 'juego') {
            this.generarArbolJuego(tokens, nodos, aristas, idCounter);
        } else {
            console.log(`⚠️ Comando "${comandoLimpio}" no reconocido como ningún tipo válido`);
            this.generarArbolDesconocido(comandoLimpio, nodos, aristas, idCounter);
        }

        this.nodes.add(nodos);
        this.edges.add(aristas);
    }

    // Determinar tipo de comando
    determinarTipoComando(comando) {
        const comandoLower = comando.toLowerCase().trim();
        console.log(`🔍 Determinando tipo para: "${comandoLower}"`);
        
        // Comandos de movimiento
        if (['izquierda', 'derecha', 'arriba', 'abajo'].includes(comandoLower)) {
            console.log(`✅ Reconocido como movimiento: ${comandoLower}`);
            return 'movimiento';
        }
        
        // Comandos Monty Hall - puertas
        if (comandoLower.startsWith('puerta') || 
            comandoLower.includes('puerta a') || 
            comandoLower.includes('puerta b') || 
            comandoLower.includes('puerta c')) {
            console.log(`✅ Reconocido como monty (puerta): ${comandoLower}`);
            return 'monty';
        }
        
        // Comandos Monty Hall - acciones
        if (['cambiar', 'mantener'].includes(comandoLower)) {
            console.log(`✅ Reconocido como monty (acción): ${comandoLower}`);
            return 'monty';
        }
        
        // Comandos Monty Hall - control
        if (['cerrar', 'reiniciar'].includes(comandoLower) || 
            comandoLower.includes('otra vez')) {
            console.log(`✅ Reconocido como monty (control): ${comandoLower}`);
            return 'monty';
        }
        
        // Comandos del juego
        if (comandoLower.includes('nueva partida') || comandoLower === 'nueva') {
            console.log(`✅ Reconocido como juego: ${comandoLower}`);
            return 'juego';
        }
        
        console.log(`⚠️ Comando no reconocido: "${comando}" (procesado como: "${comandoLower}")`);
        return 'comando_desconocido';
    }

    // Generar árbol para comandos de movimiento
    // comando → movimiento → "izquierda" | "derecha" | "arriba" | "abajo"
    generarArbolMovimiento(comando, nodos, aristas, idCounter) {
        // Nodo movimiento (comando → movimiento)
        nodos.push({
            id: idCounter++,
            label: 'movimiento',
            color: '#2ECC71',
            font: { size: 16, color: 'white' },
            shape: 'circle',
            size: 25
        });
        aristas.push({ from: 1, to: idCounter - 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 });

        // Nodo terminal (movimiento → "comando")
        nodos.push({
            id: idCounter++,
            label: `"${comando}"`,
            color: '#BDC3C7',
            font: { size: 14, color: 'black', bold: true },
            shape: 'box',
            size: 20
        });
        aristas.push({ from: idCounter - 2, to: idCounter - 1, arrows: 'to', color: { color: '#27AE60' }, width: 2 });
    }

    // Generar árbol para comandos de puerta
    // comando → monty → puerta → puerta_a/b/c → "puerta" "a/b/c"
    generarArbolPuerta(tokens, nodos, aristas, idCounter) {
        // Nodo monty (comando → monty)
        nodos.push({
            id: idCounter++,
            label: 'monty',
            color: '#F39C12',
            font: { size: 16, color: 'white' },
            shape: 'circle',
            size: 25
        });
        aristas.push({ from: 1, to: idCounter - 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 });

        // Nodo puerta (monty → puerta)
        nodos.push({
            id: idCounter++,
            label: 'puerta',
            color: '#E67E22',
            font: { size: 16, color: 'white' },
            shape: 'circle',
            size: 25
        });
        aristas.push({ from: idCounter - 2, to: idCounter - 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 });

        // Determinar qué puerta específica
        const letra = tokens.length > 1 ? tokens[1] : 'a';
        
        // Nodo puerta específica (puerta → puerta_a/b/c)
        nodos.push({
            id: idCounter++,
            label: `puerta_${letra}`,
            color: '#34495E',
            font: { size: 16, color: 'white' },
            shape: 'circle',
            size: 25
        });
        aristas.push({ from: idCounter - 2, to: idCounter - 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 });

        // Nodos terminales (puerta_x → "puerta" "x")
        nodos.push({
            id: idCounter++,
            label: '"puerta"',
            color: '#BDC3C7',
            font: { size: 14, color: 'black', bold: true },
            shape: 'box',
            size: 20
        });
        nodos.push({
            id: idCounter++,
            label: `"${letra}"`,
            color: '#BDC3C7',
            font: { size: 14, color: 'black', bold: true },
            shape: 'box',
            size: 20
        });
        
        aristas.push({ from: idCounter - 3, to: idCounter - 2, arrows: 'to', color: { color: '#E67E22' }, width: 2 });
        aristas.push({ from: idCounter - 3, to: idCounter - 1, arrows: 'to', color: { color: '#E67E22' }, width: 2 });
    }

    // Generar árbol para acciones Monty Hall
    // comando → monty → accion → "cambiar" | "mantener"
    generarArbolAccion(comando, nodos, aristas, idCounter) {
        // Nodo monty (comando → monty)
        nodos.push({
            id: idCounter++,
            label: 'monty',
            color: '#F39C12',
            font: { size: 16, color: 'white' },
            shape: 'circle',
            size: 25
        });
        aristas.push({ from: 1, to: idCounter - 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 });

        // Nodo accion (monty → accion)
        nodos.push({
            id: idCounter++,
            label: 'accion',
            color: '#E74C3C',
            font: { size: 16, color: 'white' },
            shape: 'circle',
            size: 25
        });
        aristas.push({ from: idCounter - 2, to: idCounter - 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 });

        // Nodo terminal (accion → "comando")
        nodos.push({
            id: idCounter++,
            label: `"${comando}"`,
            color: '#BDC3C7',
            font: { size: 14, color: 'black', bold: true },
            shape: 'box',
            size: 20
        });
        aristas.push({ from: idCounter - 2, to: idCounter - 1, arrows: 'to', color: { color: '#E74C3C' }, width: 2 });
    }

    // Generar árbol para comandos de control
    // comando → monty → control → "cerrar" | "reiniciar" | "otra" "vez"
    generarArbolControl(tokens, nodos, aristas, idCounter) {
        // Nodo monty (comando → monty)
        nodos.push({
            id: idCounter++,
            label: 'monty',
            color: '#F39C12',
            font: { size: 16, color: 'white' },
            shape: 'circle',
            size: 25
        });
        aristas.push({ from: 1, to: idCounter - 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 });

        // Nodo control (monty → control)
        nodos.push({
            id: idCounter++,
            label: 'control',
            color: '#8E44AD',
            font: { size: 16, color: 'white' },
            shape: 'circle',
            size: 25
        });
        aristas.push({ from: idCounter - 2, to: idCounter - 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 });

        // Verificar si es "otra vez" (dos tokens)
        if (tokens.length === 2 && tokens[0] === 'otra' && tokens[1] === 'vez') {
            // Dos nodos terminales para "otra vez"
            nodos.push({
                id: idCounter++,
                label: '"otra"',
                color: '#BDC3C7',
                font: { size: 14, color: 'black', bold: true },
                shape: 'box',
                size: 20
            });
            nodos.push({
                id: idCounter++,
                label: '"vez"',
                color: '#BDC3C7',
                font: { size: 14, color: 'black', bold: true },
                shape: 'box',
                size: 20
            });
            
            aristas.push({ from: idCounter - 3, to: idCounter - 2, arrows: 'to', color: { color: '#8E44AD' }, width: 2 });
            aristas.push({ from: idCounter - 3, to: idCounter - 1, arrows: 'to', color: { color: '#8E44AD' }, width: 2 });
        } else {
            // Un solo nodo terminal
            nodos.push({
                id: idCounter++,
                label: `"${tokens[0]}"`,
                color: '#BDC3C7',
                font: { size: 14, color: 'black', bold: true },
                shape: 'box',
                size: 20
            });
            aristas.push({ from: idCounter - 2, to: idCounter - 1, arrows: 'to', color: { color: '#8E44AD' }, width: 2 });
        }
    }

    // Generar árbol para comandos del juego
    // comando → juego → nueva → "nueva" "partida"
    generarArbolJuego(tokens, nodos, aristas, idCounter) {
        // Nodo juego (comando → juego)
        nodos.push({
            id: idCounter++,
            label: 'juego',
            color: '#9B59B6',
            font: { size: 16, color: 'white' },
            shape: 'circle',
            size: 25
        });
        aristas.push({ from: 1, to: idCounter - 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 });

        // Nodo nueva (juego → nueva)
        nodos.push({
            id: idCounter++,
            label: 'nueva',
            color: '#27AE60',
            font: { size: 16, color: 'white' },
            shape: 'circle',
            size: 25
        });
        aristas.push({ from: idCounter - 2, to: idCounter - 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 });

        // Nodos terminales (nueva → "nueva" "partida")
        nodos.push({
            id: idCounter++,
            label: '"nueva"',
            color: '#BDC3C7',
            font: { size: 14, color: 'black', bold: true },
            shape: 'box',
            size: 20
        });
        nodos.push({
            id: idCounter++,
            label: '"partida"',
            color: '#BDC3C7',
            font: { size: 14, color: 'black', bold: true },
            shape: 'box',
            size: 20
        });
        
        aristas.push({ from: idCounter - 3, to: idCounter - 2, arrows: 'to', color: { color: '#27AE60' }, width: 2 });
        aristas.push({ from: idCounter - 3, to: idCounter - 1, arrows: 'to', color: { color: '#27AE60' }, width: 2 });
    }

    // Generar árbol para comandos desconocidos
    generarArbolDesconocido(comando, nodos, aristas, idCounter) {
        // Nodo desconocido
        nodos.push({
            id: idCounter++,
            label: 'comando_desconocido',
            color: '#95A5A6',
            font: { size: 16, color: 'white' },
            shape: 'circle',
            size: 25
        });
        aristas.push({ from: 1, to: idCounter - 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 });

        // Nodo terminal
        nodos.push({
            id: idCounter++,
            label: `"${comando}"`,
            color: '#BDC3C7',
            font: { size: 14, color: 'black', bold: true },
            shape: 'box',
            size: 20
        });
        aristas.push({ from: idCounter - 2, to: idCounter - 1, arrows: 'to', color: { color: '#95A5A6' }, width: 2 });
    }

    // Obtener color según tipo
    obtenerColorTipo(tipo) {
        const colores = {
            'movimiento': '#2ECC71',
            'monty': '#F39C12',
            'juego': '#9B59B6',
            'comando_desconocido': '#95A5A6'
        };
        return colores[tipo] || '#95A5A6';
    }

    // Crear visualización
    crearVisualizacion() {
        const container = document.getElementById('mynetworkid');
        const data = {
            nodes: this.nodes,
            edges: this.edges
        };

        const options = {
            layout: {
                hierarchical: {
                    direction: 'UD',
                    sortMethod: 'directed'
                }
            },
            interaction: {
                dragNodes: true,
                dragView: true,
                zoomView: true
            },
            physics: {
                enabled: false
            },
            nodes: {
                borderWidth: 2,
                shadow: true,
                font: {
                    size: 16,
                    face: 'Arial'
                }
            },
            edges: {
                shadow: true,
                smooth: {
                    type: 'cubicBezier',
                    forceDirection: 'vertical',
                    roundness: 0.4
                }
            }
        };

        this.network = new vis.Network(container, data, options);

        // Configuración adicional
        this.network.on("stabilizationIterationsDone", function () {
            this.setOptions({ physics: false });
        });
    }

    // Método para mostrar historial completo
    mostrarHistorialCompleto(historial) {
        this.nodes.clear();
        this.edges.clear();
        
        if (!historial || historial.length === 0) {
            console.log('❌ No hay historial para mostrar');
            return;
        }
        
        let nodos = [];
        let aristas = [];
        let idCounter = 0;
        
        // Nodo raíz del historial
        nodos.push({
            id: idCounter++,
            label: `Historial\n(${historial.length} comandos)`,
            color: '#E74C3C',
            font: { size: 18, color: 'white' },
            shape: 'circle',
            size: 40
        });
        
        // Crear rama para cada comando en el historial
        historial.forEach((entrada, index) => {
            const comando = entrada.comando;
            const tokens = entrada.tokens || comando.split(' ');
            const tipoComando = this.determinarTipoComando(comando);
            const colorTipo = this.obtenerColorTipo(tipoComando);
            
            // Nodo principal del comando
            const nodoComando = {
                id: idCounter++,
                label: `Cmd ${index + 1}\n"${comando}"`,
                color: colorTipo,
                font: { size: 14, color: 'white' },
                shape: 'circle',
                title: `Comando: ${comando}\nHora: ${entrada.timestamp}\nTipo: ${tipoComando}`
            };
            nodos.push(nodoComando);
            
            // Conectar con el nodo raíz
            aristas.push({
                from: 0,
                to: nodoComando.id,
                label: entrada.timestamp,
                font: { size: 10 }
            });
            
            // Agregar nodos de tokens para este comando
            tokens.forEach((token, tokenIndex) => {
                const nodoToken = {
                    id: idCounter++,
                    label: token,
                    color: '#BDC3C7',
                    font: { size: 12, color: 'black' },
                    shape: 'box',
                    size: 20
                };
                nodos.push(nodoToken);
                
                aristas.push({
                    from: nodoComando.id,
                    to: nodoToken.id
                });
            });
        });
        
        // Actualizar los datasets
        this.nodes.update(nodos);
        this.edges.update(aristas);
        
        console.log(`🌳 Historial completo generado: ${historial.length} comandos, ${nodos.length} nodos`);
    }

    // Función de prueba para debug
    probarComando(comando) {
        console.log(`🧪 === PROBANDO COMANDO: "${comando}" ===`);
        const comandoLimpio = comando.toLowerCase().trim().replace(/[^\w\s]/g, '');
        console.log(`🔧 Comando limpio: "${comandoLimpio}"`);
        
        const tipo = this.determinarTipoComando(comandoLimpio);
        console.log(`🎯 Tipo determinado: ${tipo}`);
        
        if (tipo !== 'comando_desconocido') {
            console.log(`✅ Comando reconocido correctamente`);
        } else {
            console.log(`❌ Comando NO reconocido`);
        }
        
        console.log(`🧪 === FIN DE PRUEBA ===`);
        return tipo;
    }

    // Actualizar estadísticas
    actualizarEstadisticas() {
        // Actualizar información en el HTML
        const statusDiv = document.getElementById('network-status');
        if (statusDiv) {
            statusDiv.innerHTML = `
                🎯 Comando actual: "${this.comandoActual}" 
                | 📊 Total de comandos: ${this.historial.length}
            `;
        }

        // Actualizar info del comando
        const infoDiv = document.querySelector('.info-card');
        if (infoDiv) {
            const comandoInfo = infoDiv.querySelector('p:first-child');
            if (comandoInfo) {
                comandoInfo.innerHTML = `<strong>Comando analizado:</strong> "${this.comandoActual}"`;
            }
        }
    }

    // Cambiar a otro comando del historial
    mostrarComando(comando) {
        this.comandoActual = comando;
        this.generarArbolComando(comando);
        this.crearVisualizacion();
        this.actualizarEstadisticas();
    }
}

// Instancia global
let arbolDinamico = new ArbolVozDinamico();

// Funciones para exportar y estadísticas (compatibilidad)
function exportarArbol() {
    if (arbolDinamico.network) {
        const canvas = document.querySelector('#mynetworkid canvas');
        if (canvas) {
            const link = document.createElement('a');
            link.download = `arbol_${arbolDinamico.comandoActual.replace(/\s+/g, '_')}.png`;
            link.href = canvas.toDataURL();
            link.click();
        }
    } else {
        alert('❌ No hay árbol cargado para exportar');
    }
}

function mostrarEstadisticas() {
    const totalNodos = arbolDinamico.nodes.length;
    const totalAristas = arbolDinamico.edges.length;
    const noTerminales = arbolDinamico.nodes.get().filter(n => n.shape === 'circle').length;
    const terminales = arbolDinamico.nodes.get().filter(n => n.shape === 'box').length;
    
    alert(`
    📊 Estadísticas del Árbol de Reconocimiento de Voz:
    
    • Comando actual: "${arbolDinamico.comandoActual}"
    • Total de nodos: ${totalNodos}
    • Total de aristas: ${totalAristas}
    • No terminales: ${noTerminales}
    • Terminales: ${terminales}
    • Comandos en historial: ${arbolDinamico.historial.length}
    
    🔄 Tipo: ${arbolDinamico.determinarTipoComando(arbolDinamico.comandoActual)}
    `);
}

// Función para cargar historial y mostrar selector
function mostrarSelectorHistorial() {
    fetch('/glc/historial')
        .then(response => response.json())
        .then(data => {
            console.log('📝 Datos del historial recibidos:', data);
            
            if (data.historial && data.historial.length > 0) {
                // Crear modal o ventana flotante para mejor visualización
                const modalHTML = `
                <div id="historial-modal" style="
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: rgba(0,0,0,0.7); z-index: 1000; display: flex; 
                    justify-content: center; align-items: center;
                ">
                    <div style="
                        background: white; padding: 30px; border-radius: 15px; 
                        max-width: 800px; max-height: 80vh; overflow-y: auto;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    ">
                        <h2 style="text-align: center; color: #667eea; margin-top: 0;">
                            📝 Historial de Comandos (${data.historial.length} comandos)
                        </h2>
                        <div id="lista-comandos" style="margin: 20px 0;">
                            ${data.historial.map((entrada, index) => `
                                <div class="comando-item" style="
                                    padding: 15px; margin: 10px 0; border: 2px solid #e9ecef; 
                                    border-radius: 10px; cursor: pointer; transition: all 0.3s;
                                    background: linear-gradient(45deg, #f8f9fa, #e9ecef);
                                " onclick="seleccionarComandoHistorial('${entrada.comando}', ${index})">
                                    <div style="font-weight: bold; color: #667eea;">
                                        🎯 Comando ${index + 1}: "${entrada.comando}"
                                    </div>
                                    <div style="font-size: 14px; color: #666; margin-top: 5px;">
                                        🕐 Hora: ${entrada.timestamp} | 🔤 Tokens: ${entrada.tokens ? entrada.tokens.length : 0}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                        <div style="text-align: center; margin-top: 20px;">
                            <button onclick="mostrarTodosLosComandos()" style="
                                background: linear-gradient(45deg, #28a745, #20c997); 
                                color: white; padding: 12px 25px; border: none; 
                                border-radius: 25px; margin: 5px; cursor: pointer;
                                font-size: 16px;
                            ">🌳 Mostrar Todos los Árboles</button>
                            <button onclick="cerrarModalHistorial()" style="
                                background: linear-gradient(45deg, #dc3545, #c82333); 
                                color: white; padding: 12px 25px; border: none; 
                                border-radius: 25px; margin: 5px; cursor: pointer;
                                font-size: 16px;
                            ">❌ Cerrar</button>
                        </div>
                    </div>
                </div>`;
                
                // Agregar al DOM
                document.body.insertAdjacentHTML('beforeend', modalHTML);
                
            } else {
                alert('📝 No hay comandos en el historial. Usa los comandos de voz en el laberinto primero.');
            }
        })
        .catch(error => {
            console.error('❌ Error al obtener historial:', error);
            alert('❌ Error al cargar el historial. Verifica que el servidor esté funcionando.');
        });
}

function cambiarComandoArbol() {
    const selector = document.getElementById('selector-comando');
    if (selector && selector.value) {
        arbolDinamico.mostrarComando(selector.value);
    }
}

// Función para seleccionar un comando específico del historial
function seleccionarComandoHistorial(comando, index) {
    console.log(`🎯 Seleccionando comando: "${comando}" (índice: ${index})`);
    
    // Actualizar el árbol con el comando seleccionado
    arbolDinamico.mostrarComando(comando);
    
    // Actualizar información en pantalla
    document.getElementById('comando-actual').textContent = comando;
    document.getElementById('network-status').innerHTML = 
        `🎯 Comando: "${comando}" | 📊 Posición en historial: ${index + 1}`;
    
    // Cerrar modal
    cerrarModalHistorial();
    
    // Mensaje de confirmación
    setTimeout(() => {
        alert(`✅ Árbol actualizado para el comando: "${comando}"`);
    }, 500);
}

// Función para mostrar todos los comandos como un árbol compuesto
function mostrarTodosLosComandos() {
    fetch('/glc/historial')
        .then(response => response.json())
        .then(data => {
            if (data.historial && data.historial.length > 0) {
                // Crear un árbol que muestre todos los comandos
                arbolDinamico.mostrarHistorialCompleto(data.historial);
                cerrarModalHistorial();
                
                // Actualizar información
                document.getElementById('comando-actual').textContent = 
                    `Historial completo (${data.historial.length} comandos)`;
                document.getElementById('network-status').innerHTML = 
                    `🌳 Mostrando todos los comandos del historial | 📊 Total: ${data.historial.length}`;
                    
                setTimeout(() => {
                    alert(`🌳 Árbol actualizado con todos los ${data.historial.length} comandos del historial`);
                }, 500);
            }
        })
        .catch(error => {
            console.error('❌ Error al cargar historial completo:', error);
        });
}

// Función para cerrar el modal del historial
function cerrarModalHistorial() {
    const modal = document.getElementById('historial-modal');
    if (modal) {
        modal.remove();
    }
}

// Función global para pruebas desde la consola del navegador
function probarComandoDesdeConsola(comando) {
    console.log('🧪 === PRUEBA DESDE CONSOLA ===');
    if (typeof arbolDinamico !== 'undefined') {
        return arbolDinamico.probarComando(comando);
    } else {
        console.log('❌ arbolDinamico no está disponible, creando instancia temporal');
        
        // Crear una instancia temporal para prueba
        const tester = new ArbolVozDinamico();
        return tester.probarComando(comando);
    }
}
