var nodes = new vis.DataSet([
  {"id": 0, "label": "inicio", "color": "#2ECC71", "font": {"size": 16, "color": "white"}, "shape": "diamond", "title": ""},
  {"id": 1, "label": "esperando_movimiento", "color": "#BDC3C7", "font": {"size": 16, "color": "black"}, "shape": "ellipse", "title": ""}
]);

var edges = new vis.DataSet([
  {"from": 0, "to": 1, "label": "comenzar", "arrows": "to", "color": {"color": "#2B7CE9"}, "width": 2, "font": {"size": 14, "align": "middle"}}
]);

var container = document.getElementById('afn-network');
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
