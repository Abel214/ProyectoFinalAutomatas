import webbrowser
import os
import re

from .logicaArbol import VisualizadorArbol

class AnalizadorGLC:
    GRAMATICA = [
        # Símbolo inicial
        {"no_terminal": "S", "entrada": "comando", "produccion": 'S → comando'},
        {"no_terminal": "S", "entrada": "ε", "produccion": 'S → ε'},
        
        # Comandos principales
        {"no_terminal": "comando", "entrada": "movimiento", "produccion": 'comando → movimiento'},
        {"no_terminal": "comando", "entrada": "monty", "produccion": 'comando → monty'},
        {"no_terminal": "comando", "entrada": "juego", "produccion": 'comando → juego'},
        
        # Comandos de movimiento
        {"no_terminal": "movimiento", "entrada": "izquierda", "produccion": 'movimiento → "izquierda"'},
        {"no_terminal": "movimiento", "entrada": "derecha", "produccion": 'movimiento → "derecha"'},
        {"no_terminal": "movimiento", "entrada": "arriba", "produccion": 'movimiento → "arriba"'},
        {"no_terminal": "movimiento", "entrada": "abajo", "produccion": 'movimiento → "abajo"'},
        
        # Comandos Monty Hall
        {"no_terminal": "monty", "entrada": "puerta", "produccion": 'monty → puerta'},
        {"no_terminal": "monty", "entrada": "accion", "produccion": 'monty → accion'},
        {"no_terminal": "monty", "entrada": "control", "produccion": 'monty → control'},
        
        # Selección de puertas
        {"no_terminal": "puerta", "entrada": "puerta_a", "produccion": 'puerta → puerta_a'},
        {"no_terminal": "puerta", "entrada": "puerta_b", "produccion": 'puerta → puerta_b'},
        {"no_terminal": "puerta", "entrada": "puerta_c", "produccion": 'puerta → puerta_c'},
        
        {"no_terminal": "puerta_a", "entrada": "puerta a", "produccion": 'puerta_a → "puerta" "a"'},
        {"no_terminal": "puerta_b", "entrada": "puerta b", "produccion": 'puerta_b → "puerta" "b"'},
        {"no_terminal": "puerta_c", "entrada": "puerta c", "produccion": 'puerta_c → "puerta" "c"'},
        
        # Acciones del juego Monty Hall
        {"no_terminal": "accion", "entrada": "cambiar", "produccion": 'accion → "cambiar"'},
        {"no_terminal": "accion", "entrada": "mantener", "produccion": 'accion → "mantener"'},
        
        # Controles del juego
        {"no_terminal": "control", "entrada": "cerrar", "produccion": 'control → "cerrar"'},
        {"no_terminal": "control", "entrada": "reiniciar", "produccion": 'control → "reiniciar"'},
        {"no_terminal": "control", "entrada": "otra_vez", "produccion": 'control → "otra" "vez"'},
        
        # Comandos del juego general
        {"no_terminal": "juego", "entrada": "nueva", "produccion": 'juego → nueva'},
        {"no_terminal": "nueva", "entrada": "nueva partida", "produccion": 'nueva → "nueva" "partida"'},
    ]
    
    def __init__(self):
        self.tokens = []
        self.proceso_arbol = []
        self.arbol = {'symbol': 'S', 'children': []}
        self.posicion = 0
        self.es_cadena_valida = False
        self.reglas_usadas = []  # <-- Agrega esto

    def registrar_regla(self, no_terminal, entrada, produccion):
        self.reglas_usadas.append({
            "no_terminal": no_terminal,
            "entrada": entrada,
            "produccion": produccion
        })
    """
    Gramática de Reconocimiento de Voz para Laberinto y Monty Hall:
    
    S → comando | ε
    
    comando → movimiento | monty | juego
    
    movimiento → "izquierda" | "derecha" | "arriba" | "abajo"
    
    monty → puerta | accion | control
    
    puerta → puerta_a | puerta_b | puerta_c
    puerta_a → "puerta" "a"
    puerta_b → "puerta" "b" 
    puerta_c → "puerta" "c"
    
    accion → "cambiar" | "mantener"
    
    control → "cerrar" | "reiniciar" | "otra" "vez"
    
    juego → nueva
    nueva → "nueva" "partida"
    """

    def tokenizar(self, cadena):
        # Limpiar y normalizar la cadena
        cadena = cadena.strip().lower()
        
        # Patrón para tokenizar comandos de voz
        # Buscar palabras completas separadas por espacios
        palabras = cadena.split()
        
        # Filtrar palabras vacías y normalizar
        tokens = []
        for palabra in palabras:
            palabra_limpia = palabra.strip()
            if palabra_limpia:
                tokens.append(palabra_limpia)
        
        return tokens

    def procesar_cadena(self, cadena):
        self.tokens = self.tokenizar(cadena)
        self.posicion = 0
        print(f"🔍 Tokens extraídos: {self.tokens}")
        return self.tokens is not None

    def peek_token(self):
        """Mira el token actual sin avanzar"""
        if self.posicion < len(self.tokens):
            return self.tokens[self.posicion]
        return None

    def consume_token(self, expected=None):
        """Consume el token actual y opcionalmente verifica si es el esperado"""
        if self.posicion < len(self.tokens):
            token = self.tokens[self.posicion]
            self.posicion += 1
            if expected and token != expected:
                print(f"❌ Se esperaba '{expected}' pero se encontró '{token}'")
                return None
            return token
        return None

    def construir_arbol(self):
        self.posicion = 0
        self.arbol = self._parsear_S()
        # Si el árbol es None, crea un árbol de error
        if self.arbol is None:
            self.arbol = {
                'symbol': '❌ Error de sintaxis',
                'children': [
                    {'symbol': 'Se encontró un token inesperado o falta una producción válida.', 'children': []}
                ]
            }
            self.es_cadena_valida = False
        else:
            # Si hay tokens sin consumir, también es inválido pero muestra el árbol parcial
            self.es_cadena_valida = self.posicion >= len(self.tokens)
            if not self.es_cadena_valida:
                self.arbol = {
                    'symbol': '❌ Error de sintaxis',
                    'children': [
                        self.arbol,
                        {'symbol': f'Token inesperado: {self.tokens[self.posicion]}', 'children': []}
                    ]
                }

    def _parsear_S(self):
        """S → comando | ε"""
        nodo = {'symbol': 'S', 'children': []}
        
        # Verificar si hay tokens
        if self.posicion < len(self.tokens):
            # S → comando
            self.registrar_regla('S', 'comando', 'S → comando')
            comando_nodo = self._parsear_comando()
            if comando_nodo:
                nodo['children'].append(comando_nodo)
                return nodo
            else:
                return None
        else:
            # S → ε (epsilon - cadena vacía)
            self.registrar_regla('S', 'ε', 'S → ε')
            nodo['children'].append({'symbol': 'ε', 'children': []})
            return nodo

    def _parsear_comando(self):
        """comando → movimiento | monty | juego"""
        nodo = {'symbol': 'comando', 'children': []}
        
        # Verificar el primer token para decidir el tipo de comando
        token = self.peek_token()
        
        # Intentar parsear movimiento
        if token in ['izquierda', 'derecha', 'arriba', 'abajo']:
            self.registrar_regla('comando', 'movimiento', 'comando → movimiento')
            mov_nodo = self._parsear_movimiento()
            if mov_nodo:
                nodo['children'].append(mov_nodo)
                return nodo
        
        # Intentar parsear comandos Monty Hall
        elif token in ['puerta', 'cambiar', 'mantener', 'cerrar', 'reiniciar', 'otra']:
            self.registrar_regla('comando', 'monty', 'comando → monty')
            monty_nodo = self._parsear_monty()
            if monty_nodo:
                nodo['children'].append(monty_nodo)
                return nodo
        
        # Intentar parsear comandos de juego
        elif token == 'nueva':
            self.registrar_regla('comando', 'juego', 'comando → juego')
            juego_nodo = self._parsear_juego()
            if juego_nodo:
                nodo['children'].append(juego_nodo)
                return nodo
        
        return None

    def _parsear_movimiento(self):
        """movimiento → "izquierda" | "derecha" | "arriba" | "abajo" """
        nodo = {'symbol': 'movimiento', 'children': []}
        token = self.peek_token()
        
        if token in ['izquierda', 'derecha', 'arriba', 'abajo']:
            self.registrar_regla('movimiento', token, f'movimiento → "{token}"')
            self.consume_token()
            nodo['children'].append({'symbol': token, 'children': []})
            return nodo
        
        return None

    def _parsear_monty(self):
        """monty → puerta | accion | control"""
        nodo = {'symbol': 'monty', 'children': []}
        token = self.peek_token()
        
        # Intentar parsear puerta
        if token == 'puerta':
            self.registrar_regla('monty', 'puerta', 'monty → puerta')
            puerta_nodo = self._parsear_puerta()
            if puerta_nodo:
                nodo['children'].append(puerta_nodo)
                return nodo
        
        # Intentar parsear acción
        elif token in ['cambiar', 'mantener']:
            self.registrar_regla('monty', 'accion', 'monty → accion')
            accion_nodo = self._parsear_accion()
            if accion_nodo:
                nodo['children'].append(accion_nodo)
                return nodo
        
        # Intentar parsear control
        elif token in ['cerrar', 'reiniciar', 'otra']:
            self.registrar_regla('monty', 'control', 'monty → control')
            control_nodo = self._parsear_control()
            if control_nodo:
                nodo['children'].append(control_nodo)
                return nodo
        
        return None

    def _parsear_puerta(self):
        """puerta → puerta_a | puerta_b | puerta_c"""
        nodo = {'symbol': 'puerta', 'children': []}
        
        if self.posicion + 1 < len(self.tokens) and self.peek_token() == 'puerta':
            segunda_palabra = self.tokens[self.posicion + 1]
            
            if segunda_palabra == 'a':
                self.registrar_regla('puerta', 'puerta_a', 'puerta → puerta_a')
                puerta_a_nodo = self._parsear_puerta_a()
                if puerta_a_nodo:
                    nodo['children'].append(puerta_a_nodo)
                    return nodo
                    
            elif segunda_palabra == 'b':
                self.registrar_regla('puerta', 'puerta_b', 'puerta → puerta_b')
                puerta_b_nodo = self._parsear_puerta_b()
                if puerta_b_nodo:
                    nodo['children'].append(puerta_b_nodo)
                    return nodo
                    
            elif segunda_palabra == 'c':
                self.registrar_regla('puerta', 'puerta_c', 'puerta → puerta_c')
                puerta_c_nodo = self._parsear_puerta_c()
                if puerta_c_nodo:
                    nodo['children'].append(puerta_c_nodo)
                    return nodo
        
        return None

    def _parsear_puerta_a(self):
        """puerta_a → "puerta" "a" """
        nodo = {'symbol': 'puerta_a', 'children': []}
        
        if self.consume_token('puerta'):
            self.registrar_regla('puerta_a', 'puerta a', 'puerta_a → "puerta" "a"')
            nodo['children'].append({'symbol': 'puerta', 'children': []})
            if self.consume_token('a'):
                nodo['children'].append({'symbol': 'a', 'children': []})
                return nodo
        
        return None

    def _parsear_puerta_b(self):
        """puerta_b → "puerta" "b" """
        nodo = {'symbol': 'puerta_b', 'children': []}
        
        if self.consume_token('puerta'):
            self.registrar_regla('puerta_b', 'puerta b', 'puerta_b → "puerta" "b"')
            nodo['children'].append({'symbol': 'puerta', 'children': []})
            if self.consume_token('b'):
                nodo['children'].append({'symbol': 'b', 'children': []})
                return nodo
        
        return None

    def _parsear_puerta_c(self):
        """puerta_c → "puerta" "c" """
        nodo = {'symbol': 'puerta_c', 'children': []}
        
        if self.consume_token('puerta'):
            self.registrar_regla('puerta_c', 'puerta c', 'puerta_c → "puerta" "c"')
            nodo['children'].append({'symbol': 'puerta', 'children': []})
            if self.consume_token('c'):
                nodo['children'].append({'symbol': 'c', 'children': []})
                return nodo
        
        return None

    def _parsear_accion(self):
        """accion → "cambiar" | "mantener" """
        nodo = {'symbol': 'accion', 'children': []}
        token = self.peek_token()
        
        if token in ['cambiar', 'mantener']:
            self.registrar_regla('accion', token, f'accion → "{token}"')
            self.consume_token()
            nodo['children'].append({'symbol': token, 'children': []})
            return nodo
        
        return None

    def _parsear_control(self):
        """control → "cerrar" | "reiniciar" | "otra" "vez" """
        nodo = {'symbol': 'control', 'children': []}
        token = self.peek_token()
        
        if token == 'cerrar':
            self.registrar_regla('control', 'cerrar', 'control → "cerrar"')
            self.consume_token()
            nodo['children'].append({'symbol': 'cerrar', 'children': []})
            return nodo
            
        elif token == 'reiniciar':
            self.registrar_regla('control', 'reiniciar', 'control → "reiniciar"')
            self.consume_token()
            nodo['children'].append({'symbol': 'reiniciar', 'children': []})
            return nodo
            
        elif token == 'otra' and self.posicion + 1 < len(self.tokens) and self.tokens[self.posicion + 1] == 'vez':
            self.registrar_regla('control', 'otra vez', 'control → "otra" "vez"')
            self.consume_token('otra')
            nodo['children'].append({'symbol': 'otra', 'children': []})
            self.consume_token('vez')
            nodo['children'].append({'symbol': 'vez', 'children': []})
            return nodo
        
        return None

    def _parsear_juego(self):
        """juego → nueva"""
        nodo = {'symbol': 'juego', 'children': []}
        
        self.registrar_regla('juego', 'nueva', 'juego → nueva')
        nueva_nodo = self._parsear_nueva()
        if nueva_nodo:
            nodo['children'].append(nueva_nodo)
            return nodo
        
        return None

    def _parsear_nueva(self):
        """nueva → "nueva" "partida" """
        nodo = {'symbol': 'nueva', 'children': []}
        
        if self.consume_token('nueva'):
            self.registrar_regla('nueva', 'nueva partida', 'nueva → "nueva" "partida"')
            nodo['children'].append({'symbol': 'nueva', 'children': []})
            if self.consume_token('partida'):
                nodo['children'].append({'symbol': 'partida', 'children': []})
                return nodo
        
        return None

    def es_valido(self):
        return self.es_cadena_valida

    def generar_proceso_desde_arbol(self):
        self.proceso_arbol = []
        forma_sentencial = "S"
        self.proceso_arbol.append(forma_sentencial)
        self._generar_derivaciones_secuenciales(self.arbol, forma_sentencial)

    def _generar_derivaciones_secuenciales(self, nodo, forma_actual):
        if not nodo['children'] or nodo['symbol'] in ['ε', '.', '{', '}', ':', ';', '(', ')', ',']:
            return forma_actual
        
        # Si el nodo tiene hijos, generar derivación
        if len(nodo['children']) == 1:
            hijo = nodo['children'][0]
            nueva_forma = forma_actual.replace(nodo['symbol'], hijo['symbol'], 1)
        else:
            lado_derecho = ' '.join([hijo['symbol'] for hijo in nodo['children']])
            nueva_forma = forma_actual.replace(nodo['symbol'], lado_derecho, 1)
        
        if nueva_forma != forma_actual:
            self.proceso_arbol.append(nueva_forma)
        
        # Procesar hijos recursivamente
        forma_trabajo = nueva_forma
        for hijo in nodo['children']:
            if hijo['symbol'] not in ['ε', '.', '{', '}', ':', ';', '(', ')', ','] and hijo['children']:
                forma_trabajo = self._generar_derivaciones_secuenciales(hijo, forma_trabajo)
        
        return forma_trabajo

    def imprimir_arbol(self, nodo, prefijo='', es_ultimo=True):
        simbolo = nodo['symbol']
        print(prefijo + ('└── ' if es_ultimo else '├── ') + simbolo)
        hijos = nodo['children']
        for i, hijo in enumerate(hijos):
            nuevo_prefijo = prefijo + ('    ' if es_ultimo else '│   ')
            self.imprimir_arbol(hijo, nuevo_prefijo, i == len(hijos) - 1)


class AnalizadorGramaticaVisual(AnalizadorGLC):
    def __init__(self, auto_abrir=True):
        super().__init__()
        self.visualizador = VisualizadorArbol()
        self.auto_abrir = auto_abrir

    def abrir_html(self, archivo_html="arbol.html"):
        try:
            ruta_completa = os.path.join(os.path.dirname(__file__), '..', 'resources', 'templates', archivo_html)
            if os.path.exists(ruta_completa):
                webbrowser.open(f'file://{os.path.abspath(ruta_completa)}')
                return True
            else:
                return False
        except Exception as e:
            print(f"❌ Error al abrir el archivo: {e}")
            return False

    def mostrar_analisis(self, cadena):
        print(f"\n🎨 Analizando código CSS: '{cadena}'")
        print("=" * 50)

        if not self.procesar_cadena(cadena):
            return False

        print(f"🔍 Tokens: {self.tokens}")
        print("📝 Gramática CSS:")
        print("   S → clasenombre S | ε")
        print("   clasenombre → \".\" nombre \"{\" propiedades \"}\"")
        print("   nombre → letra | nombre letra | nombre digito | nombre \"-\" | nombre \"_\"")
        print("   propiedades → propiedad | propiedades propiedad")
        print("   propiedad → \"color:\" valor \";\" | \"background-color:\" valor \";\" | ...")
        print("   valor → color | tamaño | alineacion | numero")
        print("   color → \"red\" | \"yellow\" | \"green\" | \"rgba(...)\"")
        print("   tamaño → numero unidad")
        print("   unidad → \"px\" | \"em\" | \"%\"")

        print("\n🌳 Árbol de Derivación:")
        self.construir_arbol()
        self.imprimir_arbol(self.arbol)

        print("\n🎯 Proceso de Derivación desde Árbol:")
        self.generar_proceso_desde_arbol()
        for i, forma in enumerate(self.proceso_arbol):
            print(f"{i + 1:2}. {forma}")
        
        validez = self.es_valido()
        mensaje_validez = "✅ El código CSS es **VÁLIDO** según la gramática." if validez else "❌ El código CSS es **INVÁLIDO** según la gramática."
        print(f"\n{mensaje_validez}")
        
        if self.visualizador.visualizar_arbol(self.arbol):
            if self.auto_abrir:
                self.abrir_html()
        else:
            print("❌ Error al generar visualización")

        return True

    def configurar_auto_abrir(self, activar=True):
        """Configura la apertura automática del navegador"""
        self.auto_abrir = activar
        estado = "activada" if activar else "desactivada"
        print(f"🔧 Apertura automática {estado}")


if __name__ == "__main__":
    analizador = AnalizadorGramaticaVisual(auto_abrir=True)
    print("🎨 Analizador de Gramática CSS")
    print("=" * 60)

    casos_prueba = [
        """.container {
            color: red;
            font-size: 16px;
        }""",
        
        """.header {
            background-color: rgba(255, 0, 0, 0.5);
            text-align: center;
        }""",
        
        """.button {
            color: blue;
            font-size: 14px;
            line-height: 1.5;
        }"""
    ]
    
    for caso in casos_prueba:
        analizador.mostrar_analisis(caso)
        print("\n" + "-" * 60 + "\n")