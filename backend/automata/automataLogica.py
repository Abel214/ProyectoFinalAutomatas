import re
from datetime import datetime

from backend.automata.automataDibujo import VisualizadorAFN
from backend.automata.nodo import NodoDecision
from backend.glc.logicaGLC import AnalizadorGLC



class AFNMontyHall:
    def __init__(self):
        # Estados del autómata
        self.estados = {
            'inicio': {'tipo': 'inicial', 'descripcion': 'Estado inicial del juego'},
            'esperando_movimiento': {'tipo': 'normal', 'descripcion': 'Esperando que el jugador se mueva'},
            'frente_puertas': {'tipo': 'decision', 'descripcion': 'Jugador frente a las puertas'},
            'puerta_seleccionada': {'tipo': 'decision', 'descripcion': 'Jugador ha seleccionado una puerta'},
            'opcion_cambiar': {'tipo': 'decision', 'descripcion': 'Jugador puede cambiar o mantener su elección'},
            'ganar': {'tipo': 'final', 'resultado': 'éxito', 'descripcion': 'Jugador ha ganado el premio'},
            'perder': {'tipo': 'final', 'resultado': 'fracaso', 'descripcion': 'Jugador no ha ganado el premio'},
            'juego_terminado': {'tipo': 'final', 'descripcion': 'El juego ha terminado'}
        }

        # Transiciones mejoradas
        self.transiciones = {
            'inicio': {
                'comenzar': ['esperando_movimiento']
            },
            'esperando_movimiento': {
                'derecha': ['frente_puertas'],
                'izquierda': ['frente_puertas'],
                'arriba': ['frente_puertas'],
                'abajo': ['frente_puertas']
            },
            'frente_puertas': {
                'seleccionar_puerta': ['puerta_seleccionada']
            },
            'puerta_seleccionada': {
                'cambiar': ['opcion_cambiar'],
                'mantener': ['ganar', 'perder']  # No determinista
            },
            'opcion_cambiar': {
                'confirmar': ['ganar', 'perder']  # No determinista
            },
            'ganar': {
                'continuar': ['juego_terminado']
            },
            'perder': {
                'continuar': ['juego_terminado']
            },
            'juego_terminado': {
                'reiniciar': ['inicio']
            }
        }

        # Estado actual
        self.estado_actual = {'inicio'}
        self.historial = []
        self.puerta_premiada = None
        self.puerta_seleccionada = None
        self.estadisticas = {'ganadas': 0, 'perdidas': 0}
        self.arbol_decisiones = NodoDecision('inicio')
        self.nodo_actual = self.arbol_decisiones
        self.visualizador = VisualizadorAFN()

    def comenzar_juego(self):
        """Inicia el juego desde el estado inicial"""
        self.estado_actual = {'inicio'}
        self.asignar_puerta_premiada()
        return self.procesar_entrada('comenzar')
    def reset(self):
        """Reinicia el autómata al estado inicial"""
        self.estado_actual = {'inicio'}
        self.historial = []
        self.asignar_puerta_premiada()

        # Creamos un nuevo árbol manteniendo referencia al anterior
        self.arbol_decisiones = NodoDecision('inicio')
        self.nodo_actual = self.arbol_decisiones

    def asignar_puerta_premiada(self):
        """Asigna aleatoriamente la puerta premiada"""
        import random
        self.puerta_premiada = random.choice(['A', 'B', 'C'])

    def procesar_entrada(self, entrada):
        """Versión mejorada con más información de depuración"""
        nuevos_estados = set()
        entrada_valida = False

        print(f"\n🔍 Intentando procesar '{entrada}' desde estados: {self.estado_actual}")

        for estado in self.estado_actual:
            if estado in self.transiciones and entrada in self.transiciones[estado]:
                nuevos_estados.update(self.transiciones[estado][entrada])
                entrada_valida = True
                print(f"  ✓ Transición válida: {estado} --{entrada}--> {self.transiciones[estado][entrada]}")

        if not entrada_valida:
            print(f"  ✖ No hay transición para '{entrada}' desde {self.estado_actual}")
            return False

        # Registrar en historial con más detalles
        transicion = {
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'estado_anterior': self.estado_actual.copy(),
            'entrada': entrada,
            'nuevo_estado': nuevos_estados.copy(),
            'puerta_premiada': self.puerta_premiada,
            'puerta_seleccionada': self.puerta_seleccionada
        }
        self.historial.append(transicion)

        # Actualizar árbol de decisiones
        self._actualizar_arbol_decisiones(entrada, nuevos_estados)

        self.estado_actual = nuevos_estados
        return True

    def _actualizar_arbol_decisiones(self, entrada, nuevos_estados):
        """Versión corregida para inicializar correctamente los nodos"""
        for estado in nuevos_estados:
            # Creamos el nodo con los parámetros básicos
            nuevo_nodo = NodoDecision(
                estado=estado,
                entrada=entrada,
                padre=self.nodo_actual
            )

            # Asignamos los atributos adicionales después
            nuevo_nodo.puerta_premiada = self.puerta_premiada
            nuevo_nodo.puerta_seleccionada = self.puerta_seleccionada

            # Determinar resultado si es estado final
            if estado in ['ganar', 'perder']:
                nuevo_nodo.resultado = 'éxito' if estado == 'ganar' else 'fracaso'
                if estado == 'ganar':
                    self.estadisticas['ganadas'] += 1
                else:
                    self.estadisticas['perdidas'] += 1

            self.nodo_actual.agregar_hijo(nuevo_nodo)

        # Para simplificar, seguimos solo el primer camino
        if self.nodo_actual.hijos:
            self.nodo_actual = self.nodo_actual.hijos[0]

    def resolver_decision(self):
        """Resuelve la no determinación cuando el usuario selecciona una puerta."""
        nuevos_estados = set()

        for estado in self.estado_actual:
            if estado.startswith('puerta_'):
                puerta = estado.split('_')[1]

                # Creamos nodos para ambos resultados posibles
                nodo_ganar = NodoDecision('ganar', 'resultado', self.nodo_actual)
                nodo_ganar.resultado = 'éxito' if puerta == self.puerta_premiada else 'fracaso'
                nodo_ganar.puerta_premiada = self.puerta_premiada

                nodo_perder = NodoDecision('perder', 'resultado', self.nodo_actual)
                nodo_perder.resultado = 'fracaso' if puerta == self.puerta_premiada else 'éxito'
                nodo_perder.puerta_premiada = self.puerta_premiada

                # Añadimos ambos como hijos (representando el no determinismo)
                self.nodo_actual.agregar_hijo(nodo_ganar)
                self.nodo_actual.agregar_hijo(nodo_perder)

                # Actualizamos estados según el resultado real
                if puerta == self.puerta_premiada:
                    nuevos_estados.add('ganar')
                    self.estadisticas['ganadas'] += 1
                    self.nodo_actual = nodo_ganar
                else:
                    nuevos_estados.add('perder')
                    self.estadisticas['perdidas'] += 1
                    self.nodo_actual = nodo_perder
            else:
                nuevos_estados.add(estado)

        self.estado_actual = nuevos_estados

    def imprimir_arbol(self, nodo=None, nivel=0, prefijo=""):
        """Imprime el árbol de decisiones de forma jerárquica"""
        if nodo is None:
            nodo = self.arbol_decisiones

        espacio = "    " * nivel
        resultado = f" ({nodo.resultado})" if nodo.resultado else ""
        premio = f" [Premio: {nodo.puerta_premiada}]" if nodo.puerta_premiada else ""
        print(f"{prefijo}{espacio}{nodo.estado}{resultado}{premio}")

        for i, hijo in enumerate(nodo.hijos):
            es_ultimo = i == len(nodo.hijos) - 1
            nuevo_prefijo = "└── " if es_ultimo else "├── "
            self.imprimir_arbol(hijo, nivel + 1, nuevo_prefijo)

    def en_estado_final(self):
        """Verifica si el autómata está en un estado final"""
        return any(self.estados[e]['tipo'] == 'final' for e in self.estado_actual)

    def get_resultado(self):
        """Obtiene el resultado actual si está en estado final"""
        return self.nodo_actual.resultado if self.nodo_actual.resultado else None



    def __str__(self):
        """Representación del estado actual del autómata"""
        estado_str = f"Estados actuales: {self.estado_actual}\n"
        estado_str += f"Puerta premiada: {self.puerta_premiada}\n"
        estado_str += f"Estadísticas: {self.estadisticas}\n"
        estado_str += "Historial:\n"
        for i, (estado, entrada) in enumerate(self.historial):
            estado_str += f"  Paso {i}: {estado} --{entrada}--> \n"
        estado_str += "\nÁrbol de decisiones:\n"
        return estado_str
    def mostrar_arbol_decisiones(self):
        """Muestra la visualización del árbol de decisiones"""
        return self.visualizador.visualizar_arbol(self.arbol_decisiones)


class JuegoLaberintoMontyHall:
    def __init__(self):
        self.afn = AFNMontyHall()
        self.analizador = AnalizadorGLC()
        self.afn.comenzar_juego()

        # Mapeo extendido de comandos a transiciones
        self.mapeo_transiciones = {
            # Movimientos
            'izquierda': lambda: self.afn.procesar_entrada('izquierda'),
            'derecha': lambda: self.afn.procesar_entrada('derecha'),
            'arriba': lambda: self.afn.procesar_entrada('arriba'),
            'abajo': lambda: self.afn.procesar_entrada('abajo'),

            # Puertas
            'puerta a': lambda: self._procesar_puerta('A'),
            'puerta b': lambda: self._procesar_puerta('B'),
            'puerta c': lambda: self._procesar_puerta('C'),

            # Acciones Monty Hall
            'cambiar': lambda: self.afn.procesar_entrada('cambiar'),
            'mantener': lambda: self.afn.procesar_entrada('mantener'),

            # Control
            'reiniciar': self._reiniciar_juego,
            'nueva partida': self._reiniciar_juego
        }

    def _procesar_puerta(self, puerta):
        """Procesa la selección de una puerta específica"""
        self.afn.puerta_seleccionada = puerta
        return self.afn.procesar_entrada('seleccionar_puerta')

    def _reiniciar_juego(self):
        """Reinicia completamente el juego"""
        self.afn.reset()
        return self.afn.comenzar_juego()



    def procesar_comando(self, comando_voz):
        """Procesa un comando de voz completo y gestiona el estado del autómata

        Args:
            comando_voz (str): Comando de voz recibido del usuario

        Returns:
            tuple: (bool indicando éxito, str mensaje descriptivo)
        """
        try:
            # 1. Validación y limpieza inicial
            if not comando_voz or not isinstance(comando_voz, str):
                return False, "Comando vacío o inválido"

            comando_voz = comando_voz.strip().lower()

            # 2. Validación gramatical
            if not self.analizador.procesar_cadena(comando_voz):
                error_msg = f"Comando no válido: '{comando_voz}'"
                print(f"❌ {error_msg}")
                self._registrar_error(comando_voz, error_msg)
                return False, error_msg

            # 3. Normalización del comando
            comando = self._normalizar_comando(comando_voz)
            print(f"🔍 Procesando comando normalizado: '{comando}'")

            # 4. Verificación de estado actual
            if not self._validar_estado_para_comando(comando):
                error_msg = f"Comando '{comando}' no permitido en estado actual '{self.estado_actual}'"
                print(f"⚠️ {error_msg}")
                self._registrar_error(comando, error_msg)
                return False, error_msg

            # 5. Ejecución de la transición
            if comando in self.mapeo_transiciones:
                # Registrar comando antes de ejecutar (para historial)
                self._registrar_comando(comando_voz, comando)

                resultado = self.mapeo_transiciones[comando]()

                # Actualizar visualización y estado
                self.actualizar_visualizacion()

                # Notificar a componentes externos
                self._notificar_cambio_estado()

                return True, f"Comando '{comando}' procesado correctamente"

            # 6. Comando no reconocido
            error_msg = f"Comando no reconocido: '{comando}'"
            print(f"⚠️ {error_msg}")
            self._registrar_error(comando, error_msg)
            return False, error_msg

        except Exception as e:
            error_msg = f"Error procesando comando: {str(e)}"
            print(f"🔥 Error crítico: {error_msg}")
            self._registrar_error(comando_voz, error_msg)
            return False, error_msg


    def actualizar_visualizacion(self):
        """Actualiza todas las visualizaciones del juego"""
        print("\n" + "=" * 50)
        print(f"ESTADO ACTUAL: {self.afn.estado_actual}")
        print(f"PUERTA PREMIADA: {self.afn.puerta_premiada}")
        print(f"ESTADÍSTICAS: {self.afn.estadisticas}")
        print("\nÁRBOL DE DECISIONES:")
        self.afn.imprimir_arbol()
        self.afn.mostrar_arbol_decisiones()

    def _normalizar_comando(self, comando_voz):
        """Normaliza el comando de voz para su procesamiento"""
        # Eliminar signos de puntuación al final
        comando = re.sub(r'^[^\w]+|[^\w]+$', '', comando_voz).strip().lower()

        # Mapeo de sinónimos o variantes
        normalizaciones = {
            'derecha.': 'derecha',
            'izquierda.': 'izquierda',
            'arriba.': 'arriba',
            'abajo.': 'abajo',
            'puerta b': 'puerta_b',
            'puerta a': 'puerta_a',
            'puerta c': 'puerta_c',
            'cerrar': 'salir'
        }

        return normalizaciones.get(comando, comando)

    def _validar_estado_para_comando(self, comando):
        """Valida si el comando es permitido en el estado actual"""
        estados_permitidos = {
            'inicio': ['comenzar', 'iniciar', 'empezar'],
            'esperando_movimiento': ['izquierda', 'derecha', 'arriba', 'abajo', 'puerta_a', 'puerta_b', 'puerta_c'],
            'en_movimiento': ['detener', 'pausa'],
            'en_puertas': ['elegir', 'cambiar', 'mantener']
        }

        return comando in estados_permitidos.get(self.estado_actual, [])

    def _registrar_comando(self, comando_original, comando_normalizado):
        """Registra el comando en el historial"""
        entrada = {
            'timestamp': datetime.now().isoformat(),
            'comando_original': comando_original,
            'comando_normalizado': comando_normalizado,
            'estado_previo': self.estado_actual,
            'valido': True
        }
        self.historial.append(entrada)

    def _registrar_error(self, comando, mensaje):
        """Registra un comando fallido"""
        entrada = {
            'timestamp': datetime.now().isoformat(),
            'comando': comando,
            'error': mensaje,
            'estado_actual': self.estado_actual,
            'valido': False
        }
        self.historial.append(entrada)

    def _notificar_cambio_estado(self):
        """Notifica a otros componentes sobre cambios de estado"""
        if hasattr(self, 'on_estado_cambiado') and callable(self.on_estado_cambiado):
            self.on_estado_cambiado(self.estado_actual)
# Ejemplo de uso mejorado
if __name__ == "__main__":
    # Test de integración
    juego = JuegoLaberintoMontyHall()

    # Secuencia de comandos válidos
    comandos = [
        "derecha",
        "puerta B",
        "mantener",
        "nueva partida",
        "arriba",
        "puerta A",
        "cambiar"
    ]

    for cmd in comandos:
        print(f"\n>>> Procesando: '{cmd}'")
        juego.procesar_comando(cmd)