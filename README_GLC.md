# 🎤 GLC para Reconocimiento de Voz - Proyecto Final

Este módulo implementa una **Gramática Libre de Contexto (GLC)** para analizar y procesar comandos de voz utilizados en el proyecto del laberinto y Monty Hall.

## 📁 Estructura de Archivos

```
backend/glc/
├── logicaGLC.py         # Analizador principal con gramática de voz
├── logicaArbol.py       # Generador de árboles sintácticos

frontend/static/js/
├── arbolVoz.js         # Visualización del árbol (ejemplo)

frontend/templates/glc/
├── arbol.html          # Página de visualización del árbol

Archivos de integración:
├── demo_glc_voz.py     # Demostración standalone
├── integracion_glc.py  # Integración con Flask
```

## 🎯 Gramática Implementada

### Producción Principal
```
S → comando | ε
comando → movimiento | monty | juego
```

### Comandos de Movimiento
```
movimiento → "izquierda" | "derecha" | "arriba" | "abajo"
```

### Comandos Monty Hall
```
monty → puerta | accion | control

puerta → puerta_a | puerta_b | puerta_c
puerta_a → "puerta" "a"
puerta_b → "puerta" "b"
puerta_c → "puerta" "c"

accion → "cambiar" | "mantener"

control → "cerrar" | "reiniciar" | "otra" "vez"
```

### Comandos del Juego
```
juego → nueva
nueva → "nueva" "partida"
```

## 🗣️ Comandos Reconocidos

| Categoría | Comandos |
|-----------|----------|
| **Movimiento** | izquierda, derecha, arriba, abajo |
| **Puertas Monty Hall** | puerta a, puerta b, puerta c |
| **Acciones Monty Hall** | cambiar, mantener |
| **Control Monty Hall** | cerrar, reiniciar, otra vez |
| **Juego** | nueva partida |

## 🚀 Uso e Integración

### Integración con Flask (tu app.py)
```python
from flask import Flask
from integracion_glc import integrar_rutas_glc

app = Flask(__name__)
# ... tus configuraciones ...

# Integrar las rutas GLC
integrar_rutas_glc(app)

app.run(debug=True)
```

### Acceso desde el Laberinto
- **Botón "🌳 Ver Árbol GLC"** disponible en ambos laberintos:
  - `laberinto.html`
  - `laberintoMonty.html`
- El botón abre `/glc/arbol` en una nueva pestaña

### Rutas Disponibles
| Ruta | Descripción |
|------|-------------|
| `/glc/arbol` | Visualización del árbol sintáctico |
| `/glc/analizar` (POST) | API para analizar comandos |
| `/glc/comandos` | Lista de comandos disponibles |
| `/glc/gramatica` | Información sobre la gramática |

## 🌳 Visualización del Árbol

El árbol sintáctico se visualiza usando vis.js con:

- **Círculos**: No terminales (S, comando, movimiento, etc.)
- **Cajas**: Terminales (palabras específicas)
- **Colores**: Diferentes para cada tipo de nodo

### Ejemplo de Derivación para "puerta a":
```
S → comando → monty → puerta → puerta_a → "puerta" "a"
```

## 🔗 Integración con el Proyecto Principal

### Rutas Flask Disponibles:

| Ruta | Descripción |
|------|-------------|
| `/glc/arbol` | Visualización del árbol sintáctico |
| `/glc/analizar` (POST) | API para analizar comandos |
| `/glc/comandos` | Lista de comandos disponibles |
| `/glc/gramatica` | Información sobre la gramática |

### API JSON Example:
```javascript
// POST /glc/analizar
{
    "comando": "puerta a"
}

// Respuesta
{
    "comando": "puerta a",
    "valido": true,
    "tokens": ["puerta", "a"],
    "derivacion": ["S", "comando", "monty", "puerta", "puerta_a", "puerta a"],
    "arbol": {...}
}
```

## 🎮 Conexión con el Reconocimiento de Voz

### En el código JavaScript del laberinto:
```javascript
recognition.onresult = function (event) {
    const transcript = event.results[i][0].transcript.trim().toLowerCase();
    
    // Enviar comando al analizador GLC
    fetch('/glc/analizar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({comando: transcript})
    })
    .then(response => response.json())
    .then(data => {
        if (data.valido) {
            // Ejecutar comando válido
            ejecutarComando(data.comando);
        } else {
            console.log("Comando no reconocido por la gramática");
        }
    });
};
```

## 📊 Ejemplos de Análisis

### ✅ Comandos Válidos:
- `izquierda` → S → comando → movimiento → "izquierda"
- `puerta a` → S → comando → monty → puerta → puerta_a → "puerta" "a"
- `cambiar` → S → comando → monty → accion → "cambiar"
- `nueva partida` → S → comando → juego → nueva → "nueva" "partida"

### ❌ Comandos Inválidos:
- `puerta x` (no existe puerta x)
- `mover izquierda` (estructura incorrecta)
- `puerta` (incompleto)

## 🛠️ Configuración del Entorno

### Dependencias Python:
```bash
pip install flask
```

### Dependencias Frontend:
- vis.js (cargado desde CDN)

## 📝 Notas Técnicas

1. **Tokenización**: Los comandos se dividen por espacios y se normalizan a minúsculas
2. **Análisis**: Utiliza descenso recursivo para construir el árbol sintáctico  
3. **Validación**: Verifica que todos los tokens sean consumidos correctamente
4. **Derivación**: Genera la secuencia de reglas aplicadas paso a paso

## 🎯 Casos de Uso

### En el Laberinto:
- Detectar comandos de movimiento válidos
- Filtrar ruido en el reconocimiento de voz
- Proporcionar retroalimentación sobre comandos mal pronunciados

### En Monty Hall:
- Validar selecciones de puerta
- Confirmar decisiones de cambio/mantener
- Controlar el flujo del juego por voz

## 🔧 Extensibilidad

Para añadir nuevos comandos:

1. **Actualizar la gramática** en `logicaGLC.py`
2. **Añadir colores** en `logicaArbol.py` 
3. **Actualizar la documentación** en este README

### Ejemplo - Añadir comando "salir":
```python
# En GRAMATICA
{"no_terminal": "control", "entrada": "salir", "produccion": 'control → "salir"'},

# En _parsear_control()
elif token == 'salir':
    # ... implementar lógica
```

## 📈 Estadísticas del Proyecto

- **Símbolos no terminales**: 12
- **Símbolos terminales**: 16  
- **Reglas de producción**: 27
- **Comandos reconocidos**: ~15
- **Archivo principal**: logicaGLC.py (~537 líneas)

---

*Proyecto desarrollado para la materia de Autómatas y Lenguajes Formales*
