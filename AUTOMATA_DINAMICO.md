# 🤖 Autómata Dinámico - Documentación

## Descripción General

El **Autómata Dinámico** es una nueva funcionalidad que permite visualizar la construcción de un autómata finito en tiempo real, basándose en los comandos válidos reconocidos por la gramática libre de contexto (GLC) del proyecto.

## Características Principales

### 🏗️ Construcción Dinámica
- Se construye automáticamente basado en comandos válidos del usuario
- Cada comando válido se convierte en un estado y transición del autómata
- Visualización interactiva usando vis.js

### 🎨 Clasificación Visual por Tipos
- **🟢 Estado Inicial**: Punto de partida del autómata
- **🧭 Movimientos** (Azul): izquierda, derecha, arriba, abajo
- **🚪 Puertas** (Púrpura): puerta a, puerta b, puerta c
- **🎯 Acciones** (Naranja): cambiar, mantener
- **🔄 Control** (Naranja): nueva partida, reiniciar
- **🔴 Estado Final**: Estado de aceptación

### ⚡ Funcionalidades Interactivas
- **Construcción Instantánea**: Genera el autómata completo de una vez
- **Animación Paso a Paso**: Muestra la construcción gradual con efectos visuales
- **Detalles de Nodos**: Click en cualquier estado para ver información detallada
- **Exportación**: Guarda el autómata como imagen PNG
- **Actualización en Tiempo Real**: Se sincroniza con nuevos comandos válidos

## Cómo Usar

### 1. Acceso a la Funcionalidad
```
Navega a: http://localhost:5000/glc/automata_dinamico
```

### 2. Flujo de Trabajo Recomendado

1. **Primero**: Ve a la sección GLC (`/glc/arbol`) y prueba comandos de voz válidos
2. **Luego**: Navega al Autómata Dinámico
3. **Construye**: Presiona "Construir Autómata" para ver la visualización
4. **Explora**: Usa la animación paso a paso para entender la construcción
5. **Interactúa**: Click en nodos para ver detalles específicos

### 3. Comandos Válidos Soportados

#### Movimientos
```
- "izquierda"
- "derecha" 
- "arriba"
- "abajo"
```

#### Selección de Puertas
```
- "puerta a"
- "puerta b"
- "puerta c"
```

#### Acciones Monty Hall
```
- "cambiar"
- "mantener"
```

#### Control de Juego
```
- "nueva partida"
- "nueva"
```

## Integración con el Sistema

### Backend (Python)
- **Archivo**: `integracion_glc.py`
- **Rutas Nuevas**:
  - `/glc/automata_dinamico` - Página principal
  - `/glc/construir_automata` - API para construcción
- **Funciones Principales**:
  - `_construir_estructura_automata()` - Lógica de construcción
  - `_crear_nodo_por_comando()` - Clasificación de nodos
  - `_obtener_color_por_comando()` - Asignación de colores

### Frontend (JavaScript)
- **Archivo**: `automataDinamicoGLC.js`
- **Clase Principal**: `AutomataDinamico`
- **Funcionalidades**:
  - Construcción instantánea y paso a paso
  - Interacciones con nodos y transiciones
  - Efectos visuales y animaciones
  - Exportación de imágenes

### Template (HTML)
- **Archivo**: `automata_dinamico.html`
- **Características**:
  - Diseño responsivo
  - Estadísticas en tiempo real
  - Controles interactivos
  - Modal para comandos válidos

## Arquitectura Técnica

### 1. Flujo de Datos
```
Comandos de Voz → GLC Validation → Historial → Automata Builder → Visualization
```

### 2. Estructura del Autómata
```json
{
  "nodes": [
    {
      "id": 0,
      "label": "q₀\\n(Inicio)",
      "color": "#2ECC71",
      "tipo": "inicial",
      "comando": null
    }
  ],
  "edges": [
    {
      "from": 0,
      "to": 1,
      "label": "comando",
      "color": "#1ABC9C"
    }
  ]
}
```

### 3. Sincronización con GLC
- Se conecta automáticamente con el historial de comandos válidos
- Actualización en tiempo real cuando se agregan nuevos comandos
- Filtrado automático de comandos inválidos

## Casos de Uso

### 1. Educativo
- **Visualización**: Ver cómo los comandos se traducen a estados
- **Comprensión**: Entender la relación entre GLC y autómatas
- **Análisis**: Estudiar patrones de comandos válidos

### 2. Debugging
- **Validación**: Verificar que comandos están siendo reconocidos
- **Patrones**: Identificar secuencias comunes de comandos
- **Errores**: Detectar problemas en la gramática

### 3. Demostración
- **Presentaciones**: Mostrar el funcionamiento del sistema
- **Interactividad**: Permitir exploración visual del autómata
- **Exportación**: Generar diagramas para documentación

## Personalización

### Colores por Tipo
```javascript
this.colores = {
    inicial: '#2ECC71',    // Verde
    movimiento: '#3498DB', // Azul
    puerta: '#9B59B6',     // Púrpura
    accion: '#F39C12',     // Naranja
    control: '#E67E22',    // Naranja oscuro
    final: '#E74C3C',      // Rojo
    generico: '#95A5A6'    // Gris
};
```

### Configuración de Visualización
```javascript
// Modificar en automataDinamicoGLC.js
this.opciones = {
    layout: {
        hierarchical: {
            direction: 'LR',        // Left to Right
            levelSeparation: 180,   // Separación entre niveles
            nodeSpacing: 100        // Espaciado entre nodos
        }
    }
};
```

## Troubleshooting

### Problemas Comunes

1. **"No hay comandos válidos"**
   - Solución: Ve a `/glc/arbol` y prueba comandos de voz válidos primero

2. **"Error al construir autómata"**
   - Solución: Verifica que el backend esté funcionando y refresh la página

3. **"Visualización no aparece"**
   - Solución: Asegúrate de que vis.js esté cargado correctamente

4. **"Exportación no funciona"**
   - Solución: El autómata debe estar construido antes de exportar

### Logs de Debug
```javascript
// Activar en consola del navegador
console.log('Debug automata:', automataDinamico.obtenerEstadisticas());
```

## Roadmap Futuro

### Próximas Funcionalidades
- [ ] **Zoom y Pan**: Navegación mejorada para autómatas grandes
- [ ] **Filtros**: Mostrar solo tipos específicos de nodos
- [ ] **Búsqueda**: Encontrar comandos específicos en el autómata
- [ ] **Exportación Avanzada**: SVG, PDF, datos JSON
- [ ] **Animaciones Personalizadas**: Velocidad y efectos configurables
- [ ] **Modo Comparación**: Comparar diferentes sesiones de comandos

### Mejoras Técnicas
- [ ] **Optimización**: Manejo eficiente de autómatas muy grandes
- [ ] **Persistencia**: Guardar configuraciones del usuario
- [ ] **API REST**: Endpoints para integración externa
- [ ] **WebSockets**: Actualizaciones en tiempo real
- [ ] **Tests**: Suite completa de pruebas automatizadas

## Contribución

Para contribuir al desarrollo:

1. Fork del proyecto
2. Crea una rama para tu feature
3. Implementa cambios siguiendo las convenciones del código
4. Prueba exhaustivamente
5. Envía Pull Request con descripción detallada

## Licencia

Este proyecto es parte del Proyecto Final de Autómatas y Lenguajes Formales.

---

**Desarrollado con ❤️ para la visualización interactiva de autómatas dinámicos**
