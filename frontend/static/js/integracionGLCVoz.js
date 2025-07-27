// Integración del reconocimiento de voz con el sistema GLC
// Este archivo se debe incluir en laberinto.html y laberintoMonty.html

// Función para enviar comando al analizador GLC
function enviarComandoGLC(comando) {
    // Verificar si es comando "nueva partida" para resetear historial
    const comandoLimpio = comando.toLowerCase().trim();
    if (comandoLimpio === 'nueva partida' || comandoLimpio === 'nueva') {
        // Resetear historial antes de procesar el comando
        fetch('/glc/reset_nueva_partida', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('🔄 Historial reseteado para nueva partida');
            }
        })
        .catch(error => {
            console.error('Error al resetear historial:', error);
        });
    }

    fetch('/glc/analizar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ comando: comando })
    })
    .then(response => response.json())
    .then(data => {
        if (data.valido) {
            console.log('✅ Comando válido procesado por GLC:', comando);
            console.log('📊 Total de comandos en sesión:', data.total_comandos_sesion);
            
            // Mostrar notificación visual opcional
            if (typeof mostrarNotificacionComando === 'function') {
                mostrarNotificacionComando(comando, true);
            }
        } else {
            console.log('❌ Comando no válido:', comando);
            
            // Mostrar notificación visual opcional
            if (typeof mostrarNotificacionComando === 'function') {
                mostrarNotificacionComando(comando, false);
            }
        }
    })
    .catch(error => {
        console.error('Error al enviar comando a GLC:', error);
    });
}

// Función opcional para mostrar notificaciones visuales
function mostrarNotificacionComando(comando, valido) {
    const mensaje = valido ? 
        `✅ Comando "${comando}" registrado en GLC` : 
        `❌ Comando "${comando}" no válido`;
    
    // Crear elemento de notificación
    const notificacion = document.createElement('div');
    notificacion.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${valido ? '#d4edda' : '#f8d7da'};
        color: ${valido ? '#155724' : '#721c24'};
        padding: 10px 20px;
        border-radius: 5px;
        border: 1px solid ${valido ? '#c3e6cb' : '#f5c6cb'};
        z-index: 9999;
        font-size: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: opacity 0.5s;
    `;
    notificacion.textContent = mensaje;
    
    document.body.appendChild(notificacion);
    
    // Eliminar después de 3 segundos
    setTimeout(() => {
        notificacion.style.opacity = '0';
        setTimeout(() => {
            if (notificacion.parentNode) {
                notificacion.parentNode.removeChild(notificacion);
            }
        }, 500);
    }, 3000);
}

// Función para obtener estadísticas del historial
function obtenerEstadisticasGLC() {
    return fetch('/glc/historial')
        .then(response => response.json())
        .then(data => {
            return {
                totalComandos: data.total,
                ultimoComando: data.ultimo_comando,
                historial: data.historial
            };
        });
}

// Función para limpiar el historial
function limpiarHistorialGLC() {
    return fetch('/glc/limpiar_historial', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('🧹 Historial GLC limpiado');
        return data;
    });
}

// Exportar funciones para uso global
window.enviarComandoGLC = enviarComandoGLC;
window.mostrarNotificacionComando = mostrarNotificacionComando;
window.obtenerEstadisticasGLC = obtenerEstadisticasGLC;
window.limpiarHistorialGLC = limpiarHistorialGLC;
