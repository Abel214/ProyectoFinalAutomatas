from backend.glc.logicaGLC import AnalizadorGramaticaVisual
import json
import os

class IntegracionAFND:
    def __init__(self):
        self.analizador = AnalizadorGramaticaVisual(auto_abrir=False)
        self.comandos_sesion = []
    
    def procesar_comando_voz(self, comando):
        """Procesa un comando de voz y actualiza el AFND"""
        print(f"🎤 Procesando comando: '{comando}'")
        
        # Analizar el comando con la gramática
        resultado = self.analizador.mostrar_analisis(comando)
        
        # Guardar en el historial de la sesión
        self.comandos_sesion.append({
            'comando': comando,
            'valido': self.analizador.es_valido(),
            'tokens': self.analizador.tokens.copy() if hasattr(self.analizador, 'tokens') else []
        })
        
        return {
            'exito': resultado,
            'valido': self.analizador.es_valido(),
            'estado_automata': self.analizador.obtener_estado_automata()
        }
    
    def generar_automata_html(self):
        """Genera el archivo HTML del autómata y retorna la ruta"""
        return self.analizador.generar_automata_html("automata_juego.html")
    
    def obtener_datos_automata(self):
        """Obtiene los datos del autómata para API"""
        return self.analizador.obtener_estado_automata()
    
    def obtener_historial_sesion(self):
        """Obtiene el historial de comandos de la sesión actual"""
        return {
            'comandos': self.comandos_sesion,
            'total_comandos': len(self.comandos_sesion),
            'automata': self.analizador.exportar_automata_json()
        }
    
    def reiniciar_sesion(self):
        """Reinicia la sesión y el autómata"""
        self.comandos_sesion = []
        self.analizador = AnalizadorGramaticaVisual(auto_abrir=False)
        return True
    
    def exportar_sesion(self, archivo="sesion_automata.json"):
        """Exporta la sesión completa a un archivo JSON"""
        datos_sesion = self.obtener_historial_sesion()
        
        try:
            ruta_completa = os.path.join(os.path.dirname(__file__), '..', 'data', archivo)
            os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
            
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                json.dump(datos_sesion, f, indent=4, ensure_ascii=False)
            
            return True, ruta_completa
        except Exception as e:
            print(f"❌ Error al exportar sesión: {e}")
            return False, None

# Funciones de utilidad para la integración
def simular_sesion_ejemplo():
    """Simula una sesión de ejemplo con varios comandos"""
    integracion = IntegracionAFND()
    
    comandos_ejemplo = [
        "derecha",
        "derecha", 
        "arriba",
        "puerta a",
        "mantener",
        "reiniciar",
        "puerta b",
        "cambiar",
        "nueva partida"
    ]
    
    print("🎮 Simulando sesión de ejemplo...")
    print("=" * 50)
    
    for i, comando in enumerate(comandos_ejemplo, 1):
        print(f"\n--- Comando {i}: '{comando}' ---")
        resultado = integracion.procesar_comando_voz(comando)
        print(f"✅ Procesado exitosamente: {resultado['exito']}")
        print(f"📋 Comando válido: {resultado['valido']}")
    
    # Generar autómata final
    ruta_automata = integracion.generar_automata_html()
    print(f"\n🤖 Autómata generado en: {ruta_automata}")
    
    # Exportar sesión
    exito, ruta_sesion = integracion.exportar_sesion("ejemplo_sesion.json")
    if exito:
        print(f"💾 Sesión exportada en: {ruta_sesion}")
    
    return integracion

if __name__ == "__main__":
    # Ejecutar simulación de ejemplo
    integracion = simular_sesion_ejemplo()
    
    # Mostrar estadísticas finales
    historial = integracion.obtener_historial_sesion()
    print(f"\n📊 Estadísticas finales:")
    print(f"   Total comandos procesados: {historial['total_comandos']}")
    print(f"   Estados en autómata: {len(historial['automata']['estados'])}")
    print(f"   Transiciones: {len(historial['automata']['transiciones'])}")
