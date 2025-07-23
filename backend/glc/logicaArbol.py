import os

class VisualizadorArbol:
    def __init__(self):
        self.url_js = os.path.join("frontend", "resources", "static", "js", "arbol.js")
        self.contador_nodos = 0
        self.nodos_js = [],
        self.edges_js = []

    def generar_nodos_edges(self, nodo, padre_id=None):
        nodo_id = self.contador_nodos
        self.contador_nodos += 1
        simbolo = nodo['symbol']
        color = self._obtener_color_nodo(simbolo)

        nodo_js = {
            'id': nodo_id,
            'label': simbolo,
            'color': color,
            'font': {'size': 16, 'color': self._obtener_color_texto(simbolo)},
            'shape': self._obtener_forma_nodo(simbolo)
        }
        self.nodos_js.append(nodo_js)

        if padre_id is not None:
            edge_js = {
                'from': padre_id,
                'to': nodo_id,
                'arrows': 'to',
                'color': {'color': '#2B7CE9'},
                'width': 2
            }
            self.edges_js.append(edge_js)

        for hijo in nodo.get('children', []):
            self.generar_nodos_edges(hijo, nodo_id)

    def _obtener_color_nodo(self, simbolo):
        colores = {
            # Símbolos principales
            'S': '#E74C3C',
            'comando': '#3498DB',
            
            # Tipos de comandos
            'movimiento': '#2ECC71',
            'monty': '#F39C12',
            'juego': '#9B59B6',
            
            # Comandos de movimiento
            'izquierda': '#1ABC9C',
            'derecha': '#1ABC9C', 
            'arriba': '#1ABC9C',
            'abajo': '#1ABC9C',
            
            # Comandos Monty Hall
            'puerta': '#E67E22',
            'puerta_a': '#34495E',
            'puerta_b': '#34495E',
            'puerta_c': '#34495E',
            'accion': '#95A5A6',
            'control': '#8E44AD',
            
            # Acciones específicas
            'cambiar': '#16A085',
            'mantener': '#16A085',
            'cerrar': '#D35400',
            'reiniciar': '#D35400',
            
            # Comandos de juego
            'nueva': '#27AE60',
            
            # Terminales (palabras finales)
            'a': '#BDC3C7',
            'b': '#BDC3C7', 
            'c': '#BDC3C7',
            'puerta': '#BDC3C7',
            'otra': '#BDC3C7',
            'vez': '#BDC3C7',
            'nueva': '#BDC3C7',
            # Símbolos especiales
            'ε': '#BDC3C7',
        }
        return colores.get(simbolo, '#BDC3C7')

    def _obtener_color_texto(self, simbolo):
        # Terminales y símbolos claros usan texto negro
        terminales_claros = ['a', 'b', 'c', 'puerta', 'otra', 'vez', 'nueva', 'partida', 'ε']
        if simbolo in terminales_claros:
            return 'black'
        return 'white'

    def _obtener_forma_nodo(self, simbolo):
        # No terminales (símbolos de la gramática) son círculos
        no_terminales = ['S', 'comando', 'movimiento', 'monty', 'juego', 'puerta', 'puerta_a', 'puerta_b', 'puerta_c', 'accion', 'control', 'nueva']
        if simbolo in no_terminales:
            return 'circle'
        # Terminales son cajas
        if simbolo == 'ε':
            return 'ellipse'
        return 'box'

    def generar_archivo_js(self, arbol):
        self.contador_nodos = 0
        self.nodos_js = []
        self.edges_js = []
        self.generar_nodos_edges(arbol)

        with open(self.url_js, 'w', encoding='utf-8') as f:
            f.write("var nodes = new vis.DataSet([\n")
            for i, nodo in enumerate(self.nodos_js):
                f.write(f"  {{ id: {nodo['id']}, label: '{nodo['label']}', color: '{nodo['color']}', font: {{ size: {nodo['font']['size']}, color: '{nodo['font']['color']}' }}, shape: '{nodo['shape']}' }}")
                if i != len(self.nodos_js) - 1:
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write("]);\n\n")

            f.write("var edges = new vis.DataSet([\n")
            for i, edge in enumerate(self.edges_js):
                f.write(f"  {{ from: {edge['from']}, to: {edge['to']}, arrows: '{edge['arrows']}', color: {{ color: '{edge['color']['color']}' }}, width: {edge['width']} }}")
                if i != len(self.edges_js) - 1:
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write("]);\n\n")

            f.write("""var container = document.getElementById('mynetwork');
var data = { nodes: nodes, edges: edges };
var options = {
  layout: { hierarchical: { direction: 'UD', sortMethod: 'directed', levelSeparation: 100 } },
  physics: { enabled: false },
  nodes: { borderWidth: 2, shadow: true },
  edges: { smooth: true, arrows: { to: { enabled: true, scaleFactor: 1 } } }
};
var network = new vis.Network(container, data, options);
""")

    def visualizar_arbol(self, arbol):
        try:
            self.generar_archivo_js(arbol)
            return True
        except Exception as e:
            print(f"Error al generar el archivo de visualización: {e}")
            return False
