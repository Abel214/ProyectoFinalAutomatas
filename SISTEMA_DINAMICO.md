# 🎤 Sistema Dinámico de Árbol GLC - Documentación

## ✨ Respuesta a tu pregunta

**El árbol GLC ahora es completamente dinámico y cambia según el avance de la partida.**

### 📊 Cómo funciona:

1. **Registro automático**: Cada comando de voz que dices se envía automáticamente al sistema GLC
2. **Validación**: Solo los comandos válidos según la gramática se guardan en el historial
3. **Sesión persistente**: Tu historial se mantiene durante 30 minutos
4. **Árbol dinámico**: Al hacer clic en "🌳 Ver Árbol GLC" se muestra el último comando válido

### 🎯 Estados del árbol:

#### **Estado inicial** (sin comandos):
- Muestra árbol de ejemplo: "puerta a"

#### **Durante la partida**:
- Si dices "izquierda" → El árbol muestra la derivación de "izquierda"  
- Si dices "derecha" → El árbol cambia para mostrar "derecha"
- Si dices "puerta b" → El árbol muestra "puerta b" completo
- etc.

#### **Al finalizar la partida**:
- El botón "📝 Historial" te permite ver todos los comandos de la sesión
- Puedes seleccionar cualquier comando previo para ver su árbol específico

## 🔧 Funcionalidades implementadas:

### 📈 Integración completa:
- ✅ **Captura automática** de todos los comandos de voz
- ✅ **Validación GLC** en tiempo real  
- ✅ **Historial de sesión** persistente
- ✅ **Notificaciones visuales** (opcional)
- ✅ **Árbol dinámico** que cambia con cada comando

### 🎮 Experiencia del usuario:
1. **Juega normalmente** usando comandos de voz
2. **Haz clic en "🌳 Ver Árbol GLC"** en cualquier momento
3. **Ve el árbol del último comando válido** que dijiste
4. **Usa "📝 Historial"** para ver comandos anteriores
5. **Selecciona cualquier comando** para ver su árbol específico

### 📋 Ejemplo de flujo:

```
Usuario dice: "izquierda"     → Árbol muestra: S → comando → movimiento → "izquierda"
Usuario dice: "puerta a"     → Árbol muestra: S → comando → monty → puerta → puerta_a → "puerta" "a"  
Usuario dice: "cambiar"      → Árbol muestra: S → comando → monty → accion → "cambiar"
Usuario dice: "cerrar"       → Árbol muestra: S → comando → monty → control → "cerrar"
```

### 🗂️ Historial completo:
Al final de la partida, el historial incluye:
- ✅ **Todos los movimientos**: izquierda, derecha, arriba, abajo
- ✅ **Comandos Monty Hall**: puerta a/b/c, cambiar, mantener, cerrar, reiniciar
- ✅ **Timestamp**: Hora exacta de cada comando
- ✅ **Derivación completa**: Pasos de la gramática para cada comando

## 📱 Interfaz visual:

### Información mostrada:
- **Comando actual**: El último comando válido
- **Total de comandos**: Contador de comandos en la sesión
- **Historial**: Lista completa navegable
- **Estadísticas**: Nodos, aristas, tipo de comando

### Controles disponibles:
- 🔄 **Recargar**: Actualiza la vista
- 💾 **Exportar**: Guarda el árbol como imagen
- 📊 **Estadísticas**: Información detallada del árbol
- 📝 **Historial**: Navegador de comandos previos

## 🚀 Para probar:

1. Ejecuta: `python app.py`
2. Ve a: `http://localhost:5000/laberinto`
3. Usa comandos de voz: "izquierda", "puerta a", etc.
4. Haz clic en "🌳 Ver Árbol GLC" en cualquier momento
5. Verás el árbol del último comando válido
6. Usa "📝 Historial" para explorar comandos anteriores

---

**¡Ahora el árbol GLC es completamente dinámico y refleja exactamente lo que has dicho durante tu partida!** 🎯
