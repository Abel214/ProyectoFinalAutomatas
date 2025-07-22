// Árbol de derivación para reconocimiento de voz - Ejemplo con "puerta a"
var nodes = new vis.DataSet([
  // Nodo raíz
  { id: 0, label: 'S', color: '#E74C3C', font: { size: 16, color: 'white' }, shape: 'circle' },
  
  // Comando principal
  { id: 1, label: 'comando', color: '#3498DB', font: { size: 16, color: 'white' }, shape: 'circle' },
  
  // Tipo de comando Monty Hall
  { id: 2, label: 'monty', color: '#F39C12', font: { size: 16, color: 'white' }, shape: 'circle' },
  
  // Selección de puerta
  { id: 3, label: 'puerta', color: '#E67E22', font: { size: 16, color: 'white' }, shape: 'circle' },
  
  // Puerta específica A
  { id: 4, label: 'puerta_a', color: '#34495E', font: { size: 16, color: 'white' }, shape: 'circle' },
  
  // Terminales
  { id: 5, label: 'puerta', color: '#BDC3C7', font: { size: 16, color: 'black' }, shape: 'box' },
  { id: 6, label: 'a', color: '#BDC3C7', font: { size: 16, color: 'black' }, shape: 'box' }
]);

var edges = new vis.DataSet([
  { from: 0, to: 1, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 },
  { from: 1, to: 2, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 },
  { from: 2, to: 3, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 },
  { from: 3, to: 4, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 },
  { from: 4, to: 5, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 },
  { from: 4, to: 6, arrows: 'to', color: { color: '#2B7CE9' }, width: 2 }
]);

var container = document.getElementById('mynetworkid');
var data = {
    nodes: nodes,
    edges: edges
};

var options = {
    layout: {
        hierarchical: {
            direction: 'UD',
            sortMethod: 'directed'
        }
    },
    interaction: {
        dragNodes: true,
        dragView: true,
        zoomView: true
    },
    physics: {
        enabled: false
    },
    nodes: {
        borderWidth: 2,
        shadow: true,
        font: {
            size: 16,
            face: 'Arial'
        }
    },
    edges: {
        shadow: true,
        smooth: {
            type: 'cubicBezier',
            forceDirection: 'vertical',
            roundness: 0.4
        }
    }
};

var network = new vis.Network(container, data, options);

// Configuración adicional para mejorar la visualización
network.on("stabilizationIterationsDone", function () {
    network.setOptions({ physics: false });
});

// Función para exportar el árbol como imagen
function exportarArbol() {
    const canvas = document.querySelector('#mynetworkid canvas');
    const link = document.createElement('a');
    link.download = 'arbol_reconocimiento_voz.png';
    link.href = canvas.toDataURL();
    link.click();
}

// Función para mostrar estadísticas del árbol
function mostrarEstadisticas() {
    const totalNodos = nodes.length;
    const totalAristas = edges.length;
    const noTerminales = nodes.get().filter(n => n.shape === 'circle').length;
    const terminales = nodes.get().filter(n => n.shape === 'box').length;
    
    alert(`
    📊 Estadísticas del Árbol de Reconocimiento de Voz:
    
    • Total de nodos: ${totalNodos}
    • Total de aristas: ${totalAristas}
    • No terminales: ${noTerminales}
    • Terminales: ${terminales}
    
    🎯 Comando reconocido: "puerta a"
    🔄 Derivación: S → comando → monty → puerta → puerta_a → "puerta" "a"
    `);
}
