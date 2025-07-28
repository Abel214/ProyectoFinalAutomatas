/**
 * JavaScript para la construcción dinámica del autómata basado en comandos válidos de GLC
 * Proyecto Final - Autómatas y Lenguajes Formales
 */

class AutomataDinamico {
    constructor() {
        this.network = null;
        this.nodes = new vis.DataSet();
        this.edges = new vis.DataSet();
        this.comandosValidos = [];
        this.isConstructing = false;
        this.currentStep = 0;
        
        // Configuración de colores por tipo de comando
        this.colores = {
            inicial: '#2ECC71',
            movimiento: '#3498DB',
            puerta: '#9B59B6',
            accion: '#F39C12',
            control: '#E67E22',
            final: '#E74C3C',
            generico: '#95A5A6'
        };
        
        // Configuración de vis.js
        this.opciones = {
            layout: {
                hierarchical: {
                    direction: 'LR',
                    sortMethod: 'directed',
                    levelSeparation: 180,
                    nodeSpacing: 100,
                    treeSpacing: 200
                }
            },
            physics: { 
                enabled: false 
            },
            nodes: {
                borderWidth: 3,
                shadow: {
                    enabled: true,
                    color: 'rgba(0,0,0,0.3)',
                    size: 8,
                    x: 3,
                    y: 3
                },
                font: {
                    size: 14,
                    face: 'Arial Black',
                    strokeWidth: 3,
                    strokeColor: '#ffffff'
                },
                margin: 20,
                chosen: {
                    node: function(values, id, selected, hovering) {
                        values.shadowSize = 15;
                        values.shadowColor = 'rgba(0,0,0,0.5)';
                    }
                }
            },
            edges: {
                smooth: {
                    type: 'cubicBezier',
                    forceDirection: 'horizontal',
                    roundness: 0.4
                },
                arrows: {
                    to: { 
                        enabled: true, 
                        scaleFactor: 1.5,
                        type: 'arrow'
                    }
                },
                font: {
                    size: 12,
                    align: 'middle',
                    strokeWidth: 4,
                    strokeColor: '#ffffff',
                    color: '#2c3e50'
                },
                width: 3,
                chosen: {
                    edge: function(values, id, selected, hovering) {
                        values.width = 5;
                    }
                }
            },
            interaction: {
                hover: true,
                tooltipDelay: 300,
                hideEdgesOnDrag: false,
                selectConnectedEdges: false
            }
        };
    }
    
    // Inicializar el autómata dinámico
    async inicializar(containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('Container no encontrado:', containerId);
            return false;
        }
        
        // Crear la red de visualización
        this.network = new vis.Network(
            container, 
            { nodes: this.nodes, edges: this.edges }, 
            this.opciones
        );
        
        // Configurar eventos
        this.configurarEventos();
        
        // Cargar comandos válidos desde el servidor
        await this.cargarComandosValidos();
        
        return true;
    }
    
    // Configurar eventos de interacción
    configurarEventos() {
        if (!this.network) return;
        
        this.network.on("click", (params) => {
            if (params.nodes.length > 0) {
                const nodeId = params.nodes[0];
                const node = this.nodes.get(nodeId);
                this.mostrarDetalleNodo(node);
            }
        });
        
        this.network.on("hoverNode", (params) => {
            const nodeId = params.node;
            const node = this.nodes.get(nodeId);
            this.resaltarCamino(nodeId);
        });
        
        this.network.on("blurNode", (params) => {
            this.restaurarColores();
        });
        
        this.network.on("doubleClick", (params) => {
            if (params.nodes.length > 0) {
                this.enfocarNodo(params.nodes[0]);
            }
        });
    }
    
    // Cargar comandos válidos desde el servidor
    async cargarComandosValidos() {
        try {
            const response = await fetch('/glc/historial_completo');
            const data = await response.json();
            
            this.comandosValidos = data.historial.filter(cmd => cmd.valido === true);
            console.log('📝 Comandos válidos cargados:', this.comandosValidos.length);
            
            return this.comandosValidos;
        } catch (error) {
            console.error('❌ Error al cargar comandos válidos:', error);
            return [];
        }
    }
    
    // Construir el autómata completo de una vez
    async construirCompleto() {
        if (this.isConstructing) return;
        
        this.isConstructing = true;
        this.limpiarAutomata();
        
        try {
            const response = await fetch('/glc/construir_automata', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.renderizarDatos(data.automata);
                this.actualizarEstadisticas(data.automata.stats);
                return data.automata;
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('❌ Error al construir autómata:', error);
            throw error;
        } finally {
            this.isConstructing = false;
        }
    }
    
    // Construcción paso a paso con animación
    async construirPasoPaso(velocidad = 1000) {
        if (this.isConstructing) return;
        
        this.isConstructing = true;
        this.limpiarAutomata();
        
        try {
            await this.cargarComandosValidos();
            
            if (this.comandosValidos.length === 0) {
                throw new Error('No hay comandos válidos para construir el autómata');
            }
            
            // Crear estado inicial
            await this.agregarEstadoInicial();
            await this.pausa(velocidad);
            
            // Procesar cada comando válido
            for (let i = 0; i < this.comandosValidos.length; i++) {
                const comando = this.comandosValidos[i];
                await this.procesarComandoPaso(comando, i);
                await this.pausa(velocidad);
                
                // Actualizar progreso
                this.actualizarProgreso(i + 1, this.comandosValidos.length);
            }
            
            // Agregar estado final si hay comandos
            if (this.comandosValidos.length > 0) {
                await this.agregarEstadoFinal();
            }
            
            this.enfocarAutomataCompleto();
            
        } catch (error) {
            console.error('❌ Error en construcción paso a paso:', error);
            throw error;
        } finally {
            this.isConstructing = false;
        }
    }
    
    // Agregar estado inicial
    async agregarEstadoInicial() {
        const nodoInicial = {
            id: 0,
            label: 'q₀\n(Inicio)',
            color: this.colores.inicial,
            font: { size: 16, color: '#1A1A1A' },
            shape: 'circle',
            title: 'Estado inicial del autómata dinámico',
            tipo: 'inicial',
            x: 0,
            y: 0
        };
        
        this.nodes.add(nodoInicial);
        this.network.focus(0, { animation: true });
    }
    
    // Procesar un comando en la construcción paso a paso
    async procesarComandoPaso(comandoInfo, indice) {
        const comando = comandoInfo.comando.toLowerCase().trim();
        const nodeId = indice + 1;
        
        // Crear nodo para el comando
        const nuevoNodo = this.crearNodoPorComando(comando, comandoInfo, nodeId);
        this.nodes.add(nuevoNodo);
        
        // Crear transición desde el nodo anterior
        const transicion = {
            from: indice,
            to: nodeId,
            label: this.truncarTexto(comando, 15),
            arrows: 'to',
            color: { color: this.obtenerColorPorComando(comando) },
            width: 3,
            title: `Transición ${indice + 1}: "${comando}" (${comandoInfo.timestamp})`
        };
        
        this.edges.add(transicion);
        
        // Enfocar el nuevo nodo
        this.network.focus(nodeId, { 
            animation: { duration: 800, easingFunction: 'easeInOutQuad' } 
        });
        
        // Efecto de resaltado temporal
        setTimeout(() => {
            this.resaltarNodoTemporal(nodeId);
        }, 400);
    }
    
    // Agregar estado final
    async agregarEstadoFinal() {
        const nodeId = this.comandosValidos.length + 1;
        
        const nodoFinal = {
            id: nodeId,
            label: `q${nodeId}\n(Final)`,
            color: this.colores.final,
            font: { size: 16, color: '#1A1A1A' },
            shape: 'doublecircle',
            title: `Estado final - Procesados ${this.comandosValidos.length} comandos válidos`,
            tipo: 'final'
        };
        
        this.nodes.add(nodoFinal);
        
        // Transición lambda al estado final
        const transicionFinal = {
            from: this.comandosValidos.length,
            to: nodeId,
            label: 'λ (fin)',
            arrows: 'to',
            color: { color: '#BDC3C7' },
            width: 2,
            dashes: true,
            title: 'Transición lambda al estado de aceptación'
        };
        
        this.edges.add(transicionFinal);
        this.network.focus(nodeId, { animation: true });
    }
    
    // Crear nodo específico por tipo de comando
    crearNodoPorComando(comando, comandoInfo, nodeId) {
        const timestamp = comandoInfo.timestamp || '';
        const tokens = comandoInfo.tokens || [];
        
        if (['izquierda', 'derecha', 'arriba', 'abajo'].includes(comando)) {
            return {
                id: nodeId,
                label: `q${nodeId}\n(${comando})`,
                color: this.colores.movimiento,
                font: { size: 14, color: '#1A1A1A' },
                shape: 'circle',
                title: `🧭 Movimiento: ${comando}\n🕐 Tiempo: ${timestamp}\n🏷️ Tokens: ${tokens.join(', ')}`,
                tipo: 'movimiento',
                comando: comando
            };
        } else if (comando.includes('puerta')) {
            const puerta = tokens.find(t => ['a', 'b', 'c'].includes(t.toLowerCase())) || 'X';
            return {
                id: nodeId,
                label: `q${nodeId}\n(Puerta ${puerta.toUpperCase()})`,
                color: this.colores.puerta,
                font: { size: 14, color: '#1A1A1A' },
                shape: 'hexagon',
                title: `🚪 Puerta seleccionada: ${puerta.toUpperCase()}\n🕐 Tiempo: ${timestamp}\n🏷️ Tokens: ${tokens.join(', ')}`,
                tipo: 'puerta',
                comando: comando
            };
        } else if (['cambiar', 'mantener'].includes(comando)) {
            return {
                id: nodeId,
                label: `q${nodeId}\n(${comando})`,
                color: this.colores.accion,
                font: { size: 14, color: '#1A1A1A' },
                shape: 'diamond',
                title: `🎯 Acción Monty Hall: ${comando}\n🕐 Tiempo: ${timestamp}\n🏷️ Tokens: ${tokens.join(', ')}`,
                tipo: 'accion',
                comando: comando
            };
        } else if (comando.includes('nueva') || comando.includes('partida')) {
            return {
                id: nodeId,
                label: `q${nodeId}\n(Reset)`,
                color: this.colores.control,
                font: { size: 14, color: '#1A1A1A' },
                shape: 'star',
                title: `🔄 Nueva partida\n🕐 Tiempo: ${timestamp}\n🏷️ Tokens: ${tokens.join(', ')}`,
                tipo: 'control',
                comando: comando
            };
        } else {
            return {
                id: nodeId,
                label: `q${nodeId}\n(${this.truncarTexto(comando, 8)})`,
                color: this.colores.generico,
                font: { size: 12, color: '#1A1A1A' },
                shape: 'ellipse',
                title: `⚙️ Comando: ${comando}\n🕐 Tiempo: ${timestamp}\n🏷️ Tokens: ${tokens.join(', ')}`,
                tipo: 'generico',
                comando: comando
            };
        }
    }
    
    // Obtener color de transición por comando
    obtenerColorPorComando(comando) {
        if (['izquierda', 'derecha', 'arriba', 'abajo'].includes(comando)) {
            return '#1ABC9C';
        } else if (comando.includes('puerta')) {
            return '#9B59B6';
        } else if (['cambiar', 'mantener'].includes(comando)) {
            return '#F39C12';
        } else if (comando.includes('nueva')) {
            return '#E67E22';
        } else {
            return '#2B7CE9';
        }
    }
    
    // Renderizar datos completos del autómata
    renderizarDatos(data) {
        this.nodes.clear();
        this.edges.clear();
        
        if (data.nodes && data.nodes.length > 0) {
            this.nodes.add(data.nodes);
        }
        
        if (data.edges && data.edges.length > 0) {
            this.edges.add(data.edges);
        }
        
        // Ajustar vista para mostrar todo el autómata
        setTimeout(() => {
            this.network.fit({ animation: true });
        }, 500);
    }
    
    // Limpiar el autómata
    limpiarAutomata() {
        this.nodes.clear();
        this.edges.clear();
        this.currentStep = 0;
    }
    
    // Mostrar detalles de un nodo
    mostrarDetalleNodo(node) {
        const modal = document.createElement('div');
        modal.className = 'automata-modal';
        modal.style.cssText = `
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8); z-index: 1000; display: flex;
            justify-content: center; align-items: center; animation: fadeIn 0.3s;
        `;
        
        const content = document.createElement('div');
        content.style.cssText = `
            background: white; padding: 30px; border-radius: 15px;
            max-width: 500px; box-shadow: 0 15px 35px rgba(0,0,0,0.4);
            transform: scale(0.9); animation: scaleIn 0.3s forwards;
        `;
        
        const tipoIconos = {
            inicial: '🟢',
            movimiento: '🧭',
            puerta: '🚪',
            accion: '🎯',
            control: '🔄',
            final: '🔴',
            generico: '⚙️'
        };
        
        const icono = tipoIconos[node.tipo] || '📍';
        
        content.innerHTML = `
            <h3 style="margin-top: 0; color: #667eea; display: flex; align-items: center; gap: 10px;">
                ${icono} Detalles del Estado
            </h3>
            <div style="line-height: 1.8;">
                <p><strong>🆔 ID:</strong> ${node.id}</p>
                <p><strong>🏷️ Etiqueta:</strong> ${node.label}</p>
                <p><strong>📂 Tipo:</strong> ${node.tipo || 'N/A'}</p>
                <p><strong>💬 Comando:</strong> ${node.comando || 'N/A'}</p>
                <p><strong>📝 Descripción:</strong> ${node.title}</p>
                <p><strong>🎨 Forma:</strong> ${node.shape}</p>
            </div>
            <div style="text-align: center; margin-top: 25px;">
                <button onclick="this.parentElement.parentElement.remove()" 
                        style="padding: 12px 24px; background: linear-gradient(45deg, #667eea, #764ba2); 
                               color: white; border: none; border-radius: 25px; cursor: pointer;
                               font-weight: 500; transition: transform 0.2s;">
                    Cerrar
                </button>
            </div>
        `;
        
        // Agregar estilos CSS para animaciones
        if (!document.getElementById('automata-modal-styles')) {
            const styles = document.createElement('style');
            styles.id = 'automata-modal-styles';
            styles.textContent = `
                @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
                @keyframes scaleIn { from { transform: scale(0.9); } to { transform: scale(1); } }
                .automata-modal button:hover { transform: scale(1.05) !important; }
            `;
            document.head.appendChild(styles);
        }
        
        modal.appendChild(content);
        document.body.appendChild(modal);
        
        // Cerrar modal al hacer clic fuera
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }
    
    // Resaltar camino hacia un nodo
    resaltarCamino(nodeId) {
        // Obtener todos los edges que llegan al nodo
        const edgesHaciaNodo = this.edges.get({
            filter: edge => edge.to === nodeId
        });
        
        // Resaltar edges del camino
        edgesHaciaNodo.forEach(edge => {
            this.edges.update({
                id: edge.id,
                width: 5,
                color: { color: '#e74c3c' }
            });
        });
    }
    
    // Restaurar colores originales
    restaurarColores() {
        const allEdges = this.edges.get();
        allEdges.forEach(edge => {
            this.edges.update({
                id: edge.id,
                width: 3,
                color: { color: edge.originalColor || this.obtenerColorPorComando(edge.label) }
            });
        });
    }
    
    // Resaltar nodo temporalmente
    resaltarNodoTemporal(nodeId) {
        const node = this.nodes.get(nodeId);
        if (!node) return;
        
        const colorOriginal = node.color;
        
        // Cambiar a color de resaltado
        this.nodes.update({
            id: nodeId,
            color: '#ff6b6b',
            borderWidth: 5
        });
        
        // Restaurar color original después de un tiempo
        setTimeout(() => {
            this.nodes.update({
                id: nodeId,
                color: colorOriginal,
                borderWidth: 3
            });
        }, 1500);
    }
    
    // Enfocar un nodo específico
    enfocarNodo(nodeId) {
        this.network.focus(nodeId, {
            scale: 1.5,
            animation: {
                duration: 1000,
                easingFunction: 'easeInOutQuad'
            }
        });
    }
    
    // Enfocar todo el autómata
    enfocarAutomataCompleto() {
        this.network.fit({
            animation: {
                duration: 1500,
                easingFunction: 'easeInOutQuad'
            }
        });
    }
    
    // Actualizar estadísticas en la interfaz
    actualizarEstadisticas(stats) {
        const elementos = {
            'total-estados': stats.total_nodos,
            'total-transiciones': stats.total_transiciones,
            'total-comandos': stats.comandos_procesados
        };
        
        Object.entries(elementos).forEach(([id, valor]) => {
            const elemento = document.getElementById(id);
            if (elemento) {
                elemento.textContent = valor;
                elemento.parentElement.classList.add('loading');
                setTimeout(() => {
                    elemento.parentElement.classList.remove('loading');
                }, 1000);
            }
        });
    }
    
    // Actualizar progreso de construcción
    actualizarProgreso(actual, total) {
        const porcentaje = Math.round((actual / total) * 100);
        const status = document.getElementById('status-construccion');
        if (status) {
            status.innerHTML = `🏗️ Construyendo... ${actual}/${total} (${porcentaje}%)`;
            status.style.background = `linear-gradient(90deg, #28a745 ${porcentaje}%, #20c997 ${porcentaje}%)`;
        }
    }
    
    // Exportar autómata como imagen
    exportarImagen(nombre = 'automata_dinamico') {
        if (!this.network) return false;
        
        const canvas = document.querySelector('#automata-dinamico canvas');
        if (canvas) {
            const link = document.createElement('a');
            link.download = `${nombre}_${new Date().getTime()}.png`;
            link.href = canvas.toDataURL('image/png', 1.0);
            link.click();
            return true;
        }
        return false;
    }
    
    // Obtener estadísticas del autómata
    obtenerEstadisticas() {
        return {
            totalNodos: this.nodes.length,
            totalTransiciones: this.edges.length,
            comandosValidos: this.comandosValidos.length,
            tiposNodos: this.obtenerDistribucionTipos()
        };
    }
    
    // Obtener distribución de tipos de nodos
    obtenerDistribucionTipos() {
        const distribucion = {};
        this.nodes.get().forEach(node => {
            const tipo = node.tipo || 'desconocido';
            distribucion[tipo] = (distribucion[tipo] || 0) + 1;
        });
        return distribucion;
    }
    
    // Funciones auxiliares
    truncarTexto(texto, longitud) {
        return texto.length > longitud ? texto.substring(0, longitud) + '...' : texto;
    }
    
    pausa(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Instancia global del autómata dinámico
let automataDinamico = null;

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    automataDinamico = new AutomataDinamico();
});

// Funciones globales para usar desde HTML
window.construirAutomata = async function() {
    if (!automataDinamico) {
        console.error('Autómata dinámico no inicializado');
        return;
    }
    
    try {
        await automataDinamico.inicializar('automata-dinamico');
        await automataDinamico.construirCompleto();
        
        const status = document.getElementById('status-construccion');
        if (status) {
            status.innerHTML = '✅ Autómata construido exitosamente';
            status.style.background = 'linear-gradient(45deg, #28a745, #20c997)';
        }
    } catch (error) {
        console.error('Error al construir autómata:', error);
        const status = document.getElementById('status-construccion');
        if (status) {
            status.innerHTML = `❌ Error: ${error.message}`;
            status.style.background = 'linear-gradient(45deg, #dc3545, #c82333)';
        }
    }
};

window.animarConstruccion = async function() {
    if (!automataDinamico) {
        console.error('Autómata dinámico no inicializado');
        return;
    }
    
    try {
        await automataDinamico.inicializar('automata-dinamico');
        await automataDinamico.construirPasoPaso(1200);
        
        const status = document.getElementById('status-construccion');
        if (status) {
            status.innerHTML = '🎬 Animación completada';
            status.style.background = 'linear-gradient(45deg, #6f42c1, #6610f2)';
        }
    } catch (error) {
        console.error('Error en animación:', error);
        const status = document.getElementById('status-construccion');
        if (status) {
            status.innerHTML = `❌ Error en animación: ${error.message}`;
            status.style.background = 'linear-gradient(45deg, #dc3545, #c82333)';
        }
    }
};

window.exportarAutomata = function() {
    if (automataDinamico && automataDinamico.exportarImagen()) {
        const status = document.getElementById('status-construccion');
        if (status) {
            status.innerHTML = '💾 Imagen exportada correctamente';
            setTimeout(() => {
                status.innerHTML = '🎯 Autómata construido y listo para interacción';
            }, 3000);
        }
    } else {
        alert('❌ No se pudo exportar la imagen. Asegúrate de que el autómata esté construido.');
    }
};
