import os
import json


class VisualizadorAFN:
    def __init__(self):
        self.url_js = os.path.join("frontend", "static","js", "automata.js")
        self.contador_nodos = 0
        self.nodos_js = []
        self.edges_js = []

    def generar_nodos_edges(self, nodo, padre_id=None):
        """Recorre el árbol de decisiones del AFN y genera nodos y edges para vis.js"""
        nodo_id = self.contador_nodos
        self.contador_nodos += 1

        # Configuración del nodo según su tipo
        nodo_info = self._configurar_nodo(nodo)

        nodo_js = {
            'id': nodo_id,
            'label': nodo_info['label'],
            'color': nodo_info['color'],
            'font': {'size': 16, 'color': nodo_info['font_color']},
            'shape': nodo_info['shape'],
            'title': nodo_info['title']
        }
        self.nodos_js.append(nodo_js)

        # Conectar con el padre si existe
        if padre_id is not None:
            edge_js = {
                'from': padre_id,
                'to': nodo_id,
                'label': nodo.entrada if nodo.entrada else '',
                'arrows': 'to',
                'color': {'color': self._obtener_color_transicion(nodo.entrada)},
                'width': 2,
                'font': {'size': 14, 'align': 'middle'}
            }
            self.edges_js.append(edge_js)

        # Procesar hijos recursivamente
        for hijo in nodo.hijos:
            self.generar_nodos_edges(hijo, nodo_id)

    def _configurar_nodo(self, nodo):
        """Configura las propiedades visuales de cada nodo según su tipo"""
        config = {
            'label': nodo.estado,
            'title': '',
            'color': '#BDC3C7',  # Color por defecto
            'font_color': 'black',
            'shape': 'ellipse'
        }

        # Configuración según el tipo de estado
        if nodo.estado == 'inicio':
            config.update({
                'color': '#2ECC71',  # Verde
                'font_color': 'white',
                'shape': 'diamond'
            })
        elif nodo.estado in ['ganar', 'perder']:
            config.update({
                'color': '#E74C3C' if nodo.estado == 'perder' else '#27AE60',  # Rojo/Verde
                'font_color': 'white',
                'shape': 'box',
                'title': f"Resultado: {'éxito' if nodo.estado == 'ganar' else 'fracaso'}\nPuerta premiada: {nodo.puerta_premiada}"
            })
        elif nodo.estado.startswith('puerta_'):
            config.update({
                'color': '#3498DB',  # Azul
                'font_color': 'white',
                'shape': 'circle',
                'title': f"Puerta {nodo.estado.split('_')[1]}\nPremio: {nodo.puerta_premiada}"
            })
        elif nodo.estado == 'esperando_decision':
            config.update({
                'color': '#F39C12',  # Naranja
                'font_color': 'black',
                'shape': 'box'
            })
        elif nodo.estado == 'continuar':
            config.update({
                'color': '#9B59B6',  # Morado
                'font_color': 'white',
                'shape': 'box'
            })

        return config

    def _obtener_color_transicion(self, entrada):
        """Asigna colores a las transiciones según el tipo de entrada"""
        colores = {
            'derecha': '#1ABC9C',
            'izquierda': '#1ABC9C',
            'seleccionar': '#E74C3C',
            'continuar': '#3498DB',
            'avanzar': '#9B59B6',
            'reset': '#F39C12'
        }
        return colores.get(entrada, '#2B7CE9')  # Azul por defecto

    def generar_archivo_js(self, arbol_afn):
        """Genera el archivo JavaScript con la visualización del árbol"""
        self.contador_nodos = 0
        self.nodos_js = []
        self.edges_js = []

        # Generar nodos y edges a partir del árbol
        self.generar_nodos_edges(arbol_afn)

        # Crear el archivo JS
        with open(self.url_js, 'w', encoding='utf-8') as f:
            f.write("var nodes = new vis.DataSet([\n")
            for i, nodo in enumerate(self.nodos_js):
                nodo_str = json.dumps(nodo, ensure_ascii=False)
                f.write(f"  {nodo_str}")
                if i != len(self.nodos_js) - 1:
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write("]);\n\n")

            f.write("var edges = new vis.DataSet([\n")
            for i, edge in enumerate(self.edges_js):
                edge_str = json.dumps(edge, ensure_ascii=False)
                f.write(f"  {edge_str}")
                if i != len(self.edges_js) - 1:
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write("]);\n\n")

            f.write("""var container = document.getElementById('afn-network');
var data = { nodes: nodes, edges: edges };
var options = {
  layout: { 
    hierarchical: {
      direction: 'UD',
      sortMethod: 'directed',
      levelSeparation: 100,
      nodeSpacing: 120,
      treeSpacing: 100
    }
  },
  physics: { enabled: false },
  nodes: { 
    borderWidth: 2,
    shadow: true,
    margin: 10,
    size: 30
  },
  edges: { 
    smooth: true,
    arrows: { to: { enabled: true, scaleFactor: 0.8 } },
    font: { size: 14, align: 'middle', strokeWidth: 0 }
  },
  interaction: { hover: true }
};
var network = new vis.Network(container, data, options);

// Manejar clics en nodos
network.on("click", function(params) {
  if (params.nodes.length > 0) {
    var nodeId = params.nodes[0];
    var node = nodes.get(nodeId);
    alert(node.title || "No hay información adicional");
  }
});
""")

    def visualizar_arbol(self, arbol_afn):
        """Genera la visualización del árbol del AFN"""
        try:
            self.generar_archivo_js(arbol_afn)
            return True
        except Exception as e:
            print(f"Error al generar la visualización del AFN: {e}")
            return False