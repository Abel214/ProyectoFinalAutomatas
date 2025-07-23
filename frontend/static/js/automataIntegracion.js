class AutomataIntegracion {
    constructor() {
        this.automataActivo = false;
        this.comandosEnviados = [];
        this.estadoActual = null;
    }

    /**
     * Procesa un comando de voz y actualiza el autómata
     */
    async procesarComando(comando) {
        try {
            const response = await fetch('/api/procesar_comando', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    comando: comando
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const resultado = await response.json();
            
            // Actualizar estado local
            this.comandosEnviados.push({
                comando: comando,
                timestamp: new Date().toISOString(),
                resultado: resultado
            });

            this.estadoActual = resultado.estado_automata;

            // Notificar a la interfaz
            this.notificarCambioEstado(resultado);

            return resultado;
        } catch (error) {
            console.error('Error al procesar comando:', error);
            throw error;
        }
    }

    /**
     * Obtiene los datos actuales del autómata
     */
    async obtenerDatosAutomata() {
        try {
            const response = await fetch('/api/automata/datos');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error al obtener datos del autómata:', error);
            throw error;
        }
    }

    /**
     * Obtiene el historial completo de comandos
     */
    async obtenerHistorial() {
        try {
            const response = await fetch('/api/automata/historial');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error al obtener historial:', error);
            throw error;
        }
    }

    /**
     * Reinicia el autómata
     */
    async reiniciarAutomata() {
        try {
            const response = await fetch('/api/automata/reiniciar', {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const resultado = await response.json();
            
            // Limpiar estado local
            this.comandosEnviados = [];
            this.estadoActual = null;

            // Notificar reinicio
            this.notificarReinicio();

            return resultado;
        } catch (error) {
            console.error('Error al reiniciar autómata:', error);
            throw error;
        }
    }

    /**
     * Abre la visualización del autómata en una nueva ventana
     */
    abrirVisualizacionAutomata() {
        const url = '/automata';
        const ventana = window.open(url, 'automata_window', 
            'width=1200,height=800,scrollbars=yes,resizable=yes');
        
        if (ventana) {
            ventana.focus();
        } else {
            alert('Por favor, permite ventanas emergentes para ver el autómata');
        }
    }

    /**
     * Agrega un botón del autómata a la interfaz
     */
    agregarBotonAutomata(contenedor = 'body') {
        const container = document.querySelector(contenedor);
        if (!container) {
            console.error('Contenedor no encontrado:', contenedor);
            return;
        }

        // Crear botón del autómata
        const botonAutomata = document.createElement('button');
        botonAutomata.id = 'btn-automata';
        botonAutomata.innerHTML = '🤖 Ver Autómata';
        botonAutomata.className = 'btn btn-automata';
        botonAutomata.style.cssText = `
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        `;

        // Agregar efectos hover
        botonAutomata.addEventListener('mouseenter', () => {
            botonAutomata.style.transform = 'translateY(-2px)';
            botonAutomata.style.boxShadow = '0 6px 12px rgba(0,0,0,0.3)';
        });

        botonAutomata.addEventListener('mouseleave', () => {
            botonAutomata.style.transform = 'translateY(0)';
            botonAutomata.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
        });

        // Agregar evento click
        botonAutomata.addEventListener('click', () => {
            this.abrirVisualizacionAutomata();
        });

        container.appendChild(botonAutomata);

        // Crear panel de estado
        this.crearPanelEstado(container);
    }

    /**
     * Crea un panel de estado del autómata
     */
    crearPanelEstado(container) {
        const panel = document.createElement('div');
        panel.id = 'panel-estado-automata';
        panel.style.cssText = `
            background: rgba(255,255,255,0.9);
            border: 2px solid #667eea;
            border-radius: 8px;
            padding: 15px;
            margin: 10px;
            max-width: 300px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        `;

        panel.innerHTML = `
            <h4 style="margin: 0 0 10px 0; color: #667eea;">🤖 Estado del Autómata</h4>
            <div id="automata-info">
                <p><strong>Estados:</strong> <span id="total-estados">1</span></p>
                <p><strong>Transiciones:</strong> <span id="total-transiciones">0</span></p>
                <p><strong>Comandos:</strong> <span id="total-comandos">0</span></p>
                <p><strong>Estado actual:</strong> <span id="estado-actual">INICIO</span></p>
            </div>
            <button id="btn-reiniciar-automata" style="
                background: #dc3545;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                margin-top: 10px;
            ">🔄 Reiniciar</button>
        `;

        container.appendChild(panel);

        // Agregar evento al botón de reinicio
        const btnReiniciar = panel.querySelector('#btn-reiniciar-automata');
        btnReiniciar.addEventListener('click', async () => {
            try {
                await this.reiniciarAutomata();
                this.actualizarPanelEstado();
                alert('Autómata reiniciado exitosamente');
            } catch (error) {
                alert('Error al reiniciar el autómata');
            }
        });

        // Actualizar panel inicialmente
        this.actualizarPanelEstado();
    }

    /**
     * Actualiza el panel de estado con información actual
     */
    async actualizarPanelEstado() {
        try {
            const datos = await this.obtenerDatosAutomata();
            
            document.getElementById('total-estados').textContent = datos.estadisticas.total_estados;
            document.getElementById('total-transiciones').textContent = datos.estadisticas.total_transiciones;
            document.getElementById('total-comandos').textContent = datos.estadisticas.comandos_procesados;
            document.getElementById('estado-actual').textContent = datos.estado_actual;
            
            // Actualizar también en el panel principal si existe
            const elementos = {
                'automata-estados': datos.estadisticas.total_estados,
                'automata-transiciones': datos.estadisticas.total_transiciones,
                'automata-comandos': datos.estadisticas.comandos_procesados,
                'automata-estado-actual': datos.estado_actual
            };
            
            for (const [id, valor] of Object.entries(elementos)) {
                const elemento = document.getElementById(id);
                if (elemento) {
                    elemento.textContent = valor;
                }
            }
        } catch (error) {
            console.error('Error al actualizar panel:', error);
        }
    }

    /**
     * Notifica cambios de estado a la interfaz
     */
    notificarCambioEstado(resultado) {
        // Actualizar panel si existe
        this.actualizarPanelEstado();

        // Disparar evento personalizado
        const evento = new CustomEvent('automataActualizado', {
            detail: {
                comando: resultado,
                estado: this.estadoActual
            }
        });
        document.dispatchEvent(evento);

        console.log('🤖 Autómata actualizado:', resultado);
    }

    /**
     * Notifica reinicio del autómata
     */
    notificarReinicio() {
        // Actualizar panel
        this.actualizarPanelEstado();

        // Disparar evento personalizado
        const evento = new CustomEvent('automataReiniciado');
        document.dispatchEvent(evento);

        console.log('🔄 Autómata reiniciado');
    }

    /**
     * Integra el autómata con el reconocimiento de voz existente
     */
    integrarConReconocimientoVoz() {
        // Buscar función existente de reconocimiento de voz
        if (typeof window.procesarComandoVoz === 'function') {
            const procesarOriginal = window.procesarComandoVoz;
            
            // Sobrescribir la función para incluir el autómata
            window.procesarComandoVoz = async (comando) => {
                // Ejecutar función original
                const resultado = await procesarOriginal(comando);
                
                // Procesar en el autómata
                try {
                    await this.procesarComando(comando);
                } catch (error) {
                    console.warn('Error al procesar comando en autómata:', error);
                }
                
                return resultado;
            };
        }
    }
}

// Instancia global del autómata
const automataGlobal = new AutomataIntegracion();

// Función de inicialización
function inicializarAutomata(contenedor = '.controls, body') {
    // Agregar botón y panel
    automataGlobal.agregarBotonAutomata(contenedor);
    
    // Integrar con reconocimiento de voz si existe
    automataGlobal.integrarConReconocimientoVoz();
    
    console.log('🤖 Sistema de autómata inicializado');
}

// Función para uso directo desde consola o scripts
function procesarComandoAutomata(comando) {
    return automataGlobal.procesarComando(comando);
}

function abrirAutomata() {
    automataGlobal.abrirVisualizacionAutomata();
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Pequeño delay para asegurar que otros scripts se carguen
    setTimeout(() => {
        inicializarAutomata();
    }, 1000);
});

// Exportar para uso en otros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AutomataIntegracion,
        automataGlobal,
        inicializarAutomata,
        procesarComandoAutomata,
        abrirAutomata
    };
}
