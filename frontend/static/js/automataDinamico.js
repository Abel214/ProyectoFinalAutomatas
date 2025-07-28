

function mostrarSelectorHistorialAFN() {
    fetch('/automata/estado')
        .then(response => {
            if (!response.ok) throw new Error('Error en la respuesta del servidor');
            return response.json();
        })
        .then(data => {
            console.log('📝 Datos del historial AFN recibidos:', data);
             const limpiarComando = (comando) => {
                if (!comando) return comando;
                // Eliminar signos de puntuación al inicio/final y espacios extra
                return comando.replace(/^[¿¡\s]+|[?!.,;]\s*$/g, '').trim();
            };
            if (data.historial && data.historial.length > 0) {
                // Crear modal para el historial del AFN
                const modalHTML = `
                <div id="historial-modal-afn" style="
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
                            🎮 Historial del Autómata (${data.historial.length} transiciones)
                        </h2>

                        <div style="margin: 15px 0; padding: 10px; background: #f8f9fa; border-radius: 8px;">
                            <div style="display: flex; justify-content: space-around; margin-bottom: 10px;">
                                <span style="color: #28a745;">✅ Ganadas: ${data.estadisticas?.ganadas || 0}</span>
                                <span style="color: #dc3545;">❌ Perdidas: ${data.estadisticas?.perdidas || 0}</span>
                            </div>
                            <div style="text-align: center; color: #6c757d; font-size: 14px;">
                                Puerta premiada actual: <strong>${data.puerta_premiada || '?'}</strong>
                                ${data.puerta_seleccionada ? `| Seleccionada: <strong>${data.puerta_seleccionada}</strong>` : ''}
                            </div>
                            <!-- NUEVO: Información adicional -->
                            <div style="text-align: center; color: #6c757d; font-size: 12px; margin-top: 5px;">
                                Total de entradas procesadas: ${data.total_entradas || data.historial.length}
                            </div>
                        </div>

                        <div id="lista-comandos-afn" style="margin: 20px 0;">
                            ${data.historial.map((entrada, index) => {
                    // CORRECCIÓN: Manejo robusto de la entrada
                                const comandoMostrar = limpiarComando(entrada.comando || entrada.entrada || `Comando #${index + 1}`);
                            const comandoOriginal = entrada.comando || entrada.entrada || `Comando #${index + 1}`;
                            const timestamp = entrada.timestamp || 'N/A';
                            const estado = Array.isArray(entrada.estado_anterior) ? 
                                entrada.estado_anterior.join(', ') : 
                                (entrada.estado_anterior || 'N/A');
                            
                            // Usar valido del backend como fuente de verdad
                            const valido = entrada.valido !== false; // Considerar undefined como true
                            const resultado = entrada.resultado || 
                                (valido ? 'procesado' : 'error gramatical');

                            // Determinar color y emoji basado en el resultado
                            let colorFondo, emoji, colorTexto;
                            if (resultado === 'éxito') {
                                colorFondo = 'linear-gradient(45deg, #d4edda, #c3e6cb)';
                                emoji = '✅';
                                colorTexto = '#28a745';
                            } else if (resultado === 'fracaso') {
                                colorFondo = 'linear-gradient(45deg, #f8d7da, #f5c6cb)';
                                emoji = '❌';
                                colorTexto = '#dc3545';
                            } else if (!valido) {
                                colorFondo = 'linear-gradient(45deg, #fff3cd, #ffeaa7)';
                                emoji = '⚠️';
                                colorTexto = '#856404';
                            } else {
                                colorFondo = 'linear-gradient(45deg, #f8f9fa, #e9ecef)';
                                emoji = '➡️';
                                colorTexto = '#667eea';
                            }
                                 return `
                                <div class="comando-item-afn" style="
                                    padding: 15px; margin: 10px 0; border: 2px solid #e9ecef;
                                    border-radius: 10px; cursor: pointer; transition: all 0.3s;
                                    background: ${colorFondo};
                                    ${!valido ? 'border-color: #ffc107; border-width: 3px;' : ''}
                                " onclick="seleccionarTransicionAFN(${index})">
                                    <div style="font-weight: bold; color: ${colorTexto};">
                                        ${emoji} Paso ${index + 1}: "${comandoMostrar}"
                                        ${!valido ? ' 🚫' : ''}
                                    </div>
                                    <div style="font-size: 14px; color: #666; margin-top: 5px;">
                                        🕐 ${timestamp} | 🏁 Estado: ${estado}
                                        ${resultado !== 'procesado' ? `| 🏆 Resultado: ${resultado}` : ''}
                                    </div>
                                    ${!valido ? `
                                        <div style="font-size: 12px; color: #856404; margin-top: 3px; background: rgba(255,193,7,0.2); padding: 3px 6px; border-radius: 3px;">
                                            ⚠️ ${entrada.error || 'Error gramatical detectado'}
                                        </div>
                                        ` : ''}
                                    
                                    </div>
                                `;
                            }).join('')}
                        </div>

                        <div style="text-align: center; margin-top: 20px;">
                            <button onclick="mostrarTodosLosComandosAFN()" style="
                                background: linear-gradient(45deg, #28a745, #20c997);
                                color: white; padding: 12px 25px; border: none;
                                border-radius: 25px; margin: 5px; cursor: pointer;
                                font-size: 16px; transition: transform 0.2s;
                            " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                                🌳 Mostrar Todos los Árboles
                            </button>
                            <button onclick="cerrarModalHistorialAFN()" style="
                                background: linear-gradient(45deg, #6c757d, #5a6268);
                                color: white; padding: 12px 25px; border: none;
                                border-radius: 25px; margin: 5px; cursor: pointer;
                                font-size: 16px; transition: transform 0.2s;
                            " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                                ❌ Cerrar
                            </button>
                        </div>
                    </div>
                </div>
                `;

                // Insertar modal en el DOM
                document.body.insertAdjacentHTML('beforeend', modalHTML);
            } else {
                alert('📝 No hay historial disponible para mostrar');
            }
        })
        .catch(error => {
            console.error('❌ Error al obtener historial AFN:', error);
            alert('Error al cargar el historial del autómata: ' + error.message);
        });
}

// NUEVA FUNCIÓN: Para debugging del historial
function mostrarDebugHistorial() {
    fetch('/automata/debug_historial')
        .then(response => response.json())
        .then(data => {
            console.log('🔍 Debug historial:', data);

            const debugInfo = `
                📊 INFORMACIÓN DE DEBUG:

                • Total de entradas: ${data.total_entradas}
                • Claves disponibles: ${data.todas_claves?.join(', ') || 'N/A'}

                📝 Estructura de ejemplo:
                ${JSON.stringify(data.estructura_ejemplo, null, 2)}

                🔍 Detalles de entradas:
                ${data.entradas_detalladas?.map((entrada, i) =>
                    `  Entrada ${i}: comando="${entrada.comando_raw}", válido=${entrada.valido_gramatical}`
                ).join('\n') || 'Sin detalles'}
            `;

            alert(debugInfo);
        })
        .catch(error => {
            console.error('Error en debug:', error);
            alert('Error al obtener información de debug');
        });
}


        // Función para seleccionar una transición específica
        function seleccionarTransicionAFN(index) {
    fetch('/automata/estado')
        .then(response => response.json())
        .then(data => {
            if (data.historial && data.historial[index]) {
                const transicion = data.historial[index];
                const info = `
                    🎯 DETALLES DE LA TRANSICIÓN ${index + 1}:

                    📝 Comando: "${transicion.entrada || transicion.comando || 'N/A'}"
                    🕐 Timestamp: ${transicion.timestamp || 'N/A'}
                    🏁 Estado: ${Array.isArray(transicion.estado) ? transicion.estado.join(', ') : transicion.estado || 'N/A'}
                    🏆 Resultado: ${transicion.resultado || 'N/A'}
                    ✅ Válido gramaticalmente: ${transicion.valido_gramatical ? 'Sí' : 'No'}
                    ${transicion.mensaje ? `💬 Mensaje: ${transicion.mensaje}` : ''}
                `;
                alert(info);
            } else {
                alert('❌ No se encontró información para esta transición');
            }
        })
        .catch(error => {
            console.error('Error al obtener detalles de transición:', error);
            alert('Error al cargar detalles de la transición');
        });
}

        // Función para reiniciar el autómata
        function reiniciarAutomata() {
            fetch('/automata/reiniciar', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.mensaje === 'Juego reiniciado') {
                    alert('🔄 Autómata reiniciado correctamente');
                    cerrarModalHistorialAFN();
                    // Recargar la visualización actual
                    location.reload();
                } else {
                    alert('❌ Error al reiniciar el autómata');
                }
            });
        }
        function mostrarTodosLosComandosAFN() {
    fetch('/automata/estado')
        .then(response => response.json())
        .then(data => {
            if (data.historial && data.historial.length > 0) {
                arbolDinamico.mostrarHistorialCompleto(data.historial);  // Usa el mismo sistema de árboles
                cerrarModalHistorialAFN();

                document.getElementById('comando-actual').textContent =
                    `🌳 Historial AFN completo (${data.historial.length} comandos)`;

                document.getElementById('network-status').innerHTML =
                    `📘 Mostrando historial completo del AFN | Total: ${data.historial.length}`;

                setTimeout(() => {
                    alert(`🌳 Árbol del AFN generado con ${data.historial.length} comandos`);
                }, 500);
            } else {
                alert("ℹ️ El historial del AFN está vacío.");
            }
        })
        .catch(error => {
            console.error('❌ Error al cargar historial completo del AFN:', error);
            alert('❌ No se pudo cargar el historial del autómata.');
        });
}

        function mostrarModalInformacion(html) {
            const modal = document.createElement('div');
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(0,0,0,0.7)';
            modal.style.zIndex = '1000';
            modal.style.display = 'flex';
            modal.style.justifyContent = 'center';
            modal.style.alignItems = 'center';

            const content = document.createElement('div');
            content.style.backgroundColor = 'white';
            content.style.padding = '30px';
            content.style.borderRadius = '15px';
            content.style.maxWidth = '600px';
            content.style.maxHeight = '80vh';
            content.style.overflowY = 'auto';
            content.style.boxShadow = '0 10px 30px rgba(0,0,0,0.3)';
            content.innerHTML = html;

            const closeButton = document.createElement('button');
            closeButton.textContent = 'Cerrar';
            closeButton.style.marginTop = '20px';
            closeButton.style.padding = '10px 20px';
            closeButton.style.backgroundColor = '#6c757d';
            closeButton.style.color = 'white';
            closeButton.style.border = 'none';
            closeButton.style.borderRadius = '5px';
            closeButton.style.cursor = 'pointer';
            closeButton.onclick = function() {
                document.body.removeChild(modal);
            };

            content.appendChild(closeButton);
            modal.appendChild(content);
            document.body.appendChild(modal);
        }

        // Función para cerrar el modal del historial AFN
        function cerrarModalHistorialAFN() {
    const modal = document.getElementById('historial-modal-afn');
    if (modal) {
        modal.style.opacity = '0';
        setTimeout(() => modal.remove(), 300);
    }
}

