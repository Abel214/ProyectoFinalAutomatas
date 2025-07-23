# 🤖 Sistema de Autómata Finito No Determinista (AFND)

## Descripción

Este sistema implementa un **Autómata Finito No Determinista** que se construye dinámicamente basándose en los comandos de voz del usuario durante el juego del laberinto y Monty Hall.

## 🎯 Características Principales

### 1. Construcción Dinámica del Autómata
- **Estado Inicial**: El autómata comienza con un estado "INICIO"
- **Estados de Movimiento**: Se crean nuevos estados para cada comando de movimiento (derecha, izquierda, arriba, abajo)
- **Estados de Monty Hall**: Estados específicos para la selección de puertas, acciones (cambiar/mantener) y controles
- **Estados de Victoria/Derrota**: Estados finales basados en el resultado del juego Monty Hall

### 2. Tipos de Estados

#### Estados de Movimiento
- **INICIO**: Estado inicial del juego
- **POS_DERECHA/IZQUIERDA/ARRIBA/ABAJO**: Estados creados por comandos de movimiento
- **ZONA_MONTY**: Estado especial cuando el usuario entra a la zona Monty Hall

#### Estados de Monty Hall
- **PUERTA_A/B/C**: Estados para la selección de puertas
- **ACCION_CAMBIAR/MANTENER**: Estados para las decisiones del usuario
- **VICTORIA/DERROTA**: Estados finales del juego Monty Hall

#### Estados de Control
- **REINICIO_MONTY**: Reinicio desde la zona Monty Hall
- **NUEVA_PARTIDA**: Reinicio completo del juego
- **JUEGO_CERRADO**: Terminación del juego

### 3. Lógica del Autómata

```
INICIO → Movimientos → ZONA_MONTY → Selección de Puerta → Acción → Resultado
   ↑                                        ↓
   └────────── REINICIO ←──────────────────┘
```

#### Flujo Principal:
1. **Inicio**: Usuario comienza en estado INICIO
2. **Movimiento**: Comandos como "derecha", "izquierda" crean estados de posición
3. **Zona Monty**: Al llegar a coordenadas específicas, se activa Monty Hall
4. **Selección**: Usuario dice "puerta a/b/c" para seleccionar
5. **Decisión**: Usuario dice "cambiar" o "mantener"
6. **Resultado**: Sistema determina victoria o derrota
7. **Continuación**: Usuario puede reiniciar o terminar

### 4. Probabilidades del Monty Hall
- **Mantener**: 33% probabilidad de ganar
- **Cambiar**: 67% probabilidad de ganar (estrategia matemáticamente óptima)

## 🔧 Arquitectura Técnica

### Archivos Principales

1. **`logicaAFND.py`**: Lógica principal del autómata
   - `AutomataFinito`: Clase principal que maneja estados y transiciones
   - `VisualizadorAFND`: Generador de visualizaciones HTML

2. **`integracion_afnd.py`**: Integración con el sistema existente
   - `IntegracionAFND`: Interfaz para conectar con Flask y frontend

3. **`automataIntegracion.js`**: Cliente JavaScript
   - Comunicación con APIs REST
   - Actualización de interfaz en tiempo real

### APIs REST

- **`POST /api/procesar_comando`**: Procesa comandos de voz
- **`GET /api/automata/datos`**: Obtiene estado actual del autómata
- **`GET /api/automata/historial`**: Historial completo de comandos
- **`POST /api/automata/reiniciar`**: Reinicia el autómata
- **`GET /automata`**: Página de visualización del autómata

## 🎮 Uso del Sistema

### 1. Comandos de Voz Reconocidos

#### Movimiento
- "derecha" / "izquierda" / "arriba" / "abajo"

#### Monty Hall
- "puerta a" / "puerta b" / "puerta c"
- "cambiar" / "mantener"
- "reiniciar" / "otra vez"
- "cerrar"

#### Juego General
- "nueva partida"

### 2. Interfaz de Usuario

#### Panel de Estado
- **Estados**: Número total de estados en el autómata
- **Transiciones**: Número de transiciones creadas
- **Comandos**: Comandos procesados en la sesión
- **Estado Actual**: ID del estado actual

#### Botones
- **🤖 Ver Autómata**: Abre la visualización del autómata
- **🔄 Reiniciar**: Reinicia el autómata
- **💾 Exportar**: Descarga datos en JSON

### 3. Visualización del Autómata

#### Colores de Estados
- 🟢 **Verde**: Estados iniciales y de victoria
- 🔵 **Azul**: Estados de movimiento
- 🟠 **Naranja**: Selección de puertas
- 🔴 **Rojo**: Estados de derrota
- 🟣 **Púrpura**: Estados de control
- 🟤 **Marrón**: Estados de error

#### Formas de Estados
- **Círculo**: Estados iniciales
- **Caja**: Estados de movimiento
- **Diamante**: Selección de puertas
- **Estrella**: Estados de victoria
- **Triángulo**: Estados de derrota
- **Hexágono**: Estados de control

## 📊 Ejemplo de Sesión

```
Comando: "derecha"        → Estado: POS_DERECHA
Comando: "derecha"        → Estado: ZONA_MONTY (Monty Hall activado)
Comando: "puerta a"       → Estado: PUERTA_A
Comando: "mantener"       → Estado: ACCION_MANTENER_PERDEDOR
Comando: "reiniciar"      → Estado: REINICIO_MONTY
Comando: "puerta b"       → Estado: PUERTA_B
Comando: "cambiar"        → Estado: ACCION_CAMBIAR_GANADOR ⭐
```

## 🔬 Análisis Matemático

### Propiedades del Autómata
- **Determinista en transiciones**: Cada comando produce una transición específica
- **No determinista en resultados**: El resultado de Monty Hall tiene probabilidad
- **Estados finales**: Victoria, derrota, y cierre de juego
- **Ciclos controlados**: Reinicio permite volver a estados anteriores

### Métricas
- **Complejidad de estados**: O(n) donde n = número de comandos únicos
- **Memoria**: Estados almacenan posición, tipo, y metadata
- **Rendimiento**: Construcción en tiempo real sin pérdida de performance

## 🚀 Instalación y Configuración

### Dependencias
```bash
pip install flask
```

### Ejecución
```bash
python app.py
```

### Pruebas
```bash
python test_automata.py
```

## 📈 Estadísticas y Exportación

### Formato JSON de Exportación
```json
{
  "estados": [...],
  "transiciones": [...],
  "estado_inicial": 0,
  "estados_finales": [5, 8],
  "alfabeto": ["derecha", "puerta_a", "cambiar"],
  "historial_comandos": [...],
  "timestamp": "2025-01-23T..."
}
```

### Métricas Disponibles
- Total de estados creados
- Número de transiciones
- Comandos procesados
- Tasa de éxito en reconocimiento
- Tiempo de sesión
- Resultados de Monty Hall

## 🎯 Casos de Uso Educativos

### 1. Enseñanza de Autómatas
- Visualización en tiempo real de construcción de autómatas
- Comprensión de estados y transiciones
- Análisis de no determinismo

### 2. Teoría de Probabilidades
- Demostración práctica del problema Monty Hall
- Análisis de estrategias óptimas
- Verificación experimental de probabilidades

### 3. Reconocimiento de Voz
- Gramática libre de contexto aplicada
- Procesamiento de lenguaje natural
- Análisis sintáctico de comandos

## 🔮 Extensiones Futuras

1. **Análisis de Patrones**: Detección de patrones en comandos del usuario
2. **IA Predictiva**: Predicción de próximos comandos basado en historial
3. **Optimización de Rutas**: Sugerencias de movimientos óptimos
4. **Modo Competitivo**: Comparación de eficiencia entre usuarios
5. **Análisis Estadístico**: Reportes detallados de performance

## 👥 Créditos

Desarrollado como parte del proyecto final de Autómatas y Lenguajes Formales.

**Características destacadas:**
- Integración perfecta con reconocimiento de voz
- Visualización interactiva en tiempo real
- Análisis matemático del problema Monty Hall
- Arquitectura escalable y modular
