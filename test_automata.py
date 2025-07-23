#!/usr/bin/env python3
"""
Script de prueba para el sistema AFND de reconocimiento de voz
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.glc.logicaGLC import AnalizadorGramaticaVisual
from integracion_afnd import IntegracionAFND
import webbrowser

def test_automata_basic():
    """Prueba básica del funcionamiento del autómata"""
    print("🧪 PRUEBA BÁSICA DEL AUTÓMATA")
    print("=" * 50)
    
    integracion = IntegracionAFND()
    
    # Comandos de prueba simulando una partida
    comandos_prueba = [
        "derecha",        # Movimiento inicial
        "derecha",        # Continuar derecha
        "arriba",         # Movimiento hacia arriba (zona Monty Hall)
        "puerta a",       # Seleccionar puerta A
        "mantener",       # Mantener decisión (podría perder)
        "reiniciar",      # Reiniciar desde Monty Hall
        "puerta b",       # Seleccionar puerta B
        "cambiar",        # Cambiar decisión (mayor probabilidad de ganar)
        "nueva partida"   # Nueva partida completa
    ]
    
    print("Procesando comandos de prueba...")
    for i, comando in enumerate(comandos_prueba, 1):
        print(f"\n--- Comando {i}: '{comando}' ---")
        resultado = integracion.procesar_comando_voz(comando)
        
        if resultado['exito']:
            print(f"✅ Procesado exitosamente")
            print(f"📋 Válido: {resultado['valido']}")
            estado = resultado['estado_automata']
            print(f"🤖 Estados: {estado['estadisticas']['total_estados']}")
            print(f"🔗 Transiciones: {estado['estadisticas']['total_transiciones']}")
        else:
            print(f"❌ Error al procesar comando")
    
    return integracion

def test_html_generation():
    """Prueba la generación del HTML del autómata"""
    print("\n🌐 PRUEBA DE GENERACIÓN HTML")
    print("=" * 50)
    
    integracion = IntegracionAFND()
    
    # Agregar algunos comandos
    comandos = ["derecha", "puerta a", "cambiar", "izquierda"]
    for comando in comandos:
        integracion.procesar_comando_voz(comando)
    
    # Generar HTML
    ruta_html = integracion.generar_automata_html()
    print(f"📄 HTML generado en: {ruta_html}")
    
    if ruta_html and os.path.exists(ruta_html):
        print("✅ Archivo HTML creado exitosamente")
        
        # Preguntar si abrir en navegador
        respuesta = input("¿Abrir en navegador? (s/n): ").lower().strip()
        if respuesta == 's':
            webbrowser.open(f'file://{os.path.abspath(ruta_html)}')
            print("🚀 Autómata abierto en navegador")
    else:
        print("❌ Error al crear archivo HTML")
    
    return ruta_html

def test_json_export():
    """Prueba la exportación a JSON"""
    print("\n💾 PRUEBA DE EXPORTACIÓN JSON")
    print("=" * 50)
    
    integracion = IntegracionAFND()
    
    # Simular una sesión completa
    sesion_completa = [
        "derecha", "derecha", "arriba", "puerta b", 
        "mantener", "reiniciar", "puerta c", "cambiar"
    ]
    
    for comando in sesion_completa:
        integracion.procesar_comando_voz(comando)
    
    # Exportar sesión
    exito, ruta_json = integracion.exportar_sesion("test_automata.json")
    
    if exito:
        print(f"✅ Sesión exportada a: {ruta_json}")
        
        # Leer y mostrar estadísticas
        historial = integracion.obtener_historial_sesion()
        print(f"📊 Estadísticas:")
        print(f"   - Comandos procesados: {historial['total_comandos']}")
        print(f"   - Estados en autómata: {len(historial['automata']['estados'])}")
        print(f"   - Transiciones: {len(historial['automata']['transiciones'])}")
    else:
        print("❌ Error al exportar sesión")
    
    return exito

def test_integration_complete():
    """Prueba de integración completa"""
    print("\n🎮 PRUEBA DE INTEGRACIÓN COMPLETA")
    print("=" * 50)
    
    # Usar el analizador completo
    analizador = AnalizadorGramaticaVisual(auto_abrir=False)
    
    # Comandos que simulan una partida real
    comandos_partida = [
        "derecha",
        "arriba", 
        "derecha",
        "puerta a",
        "mantener",
        "reiniciar",
        "puerta b", 
        "cambiar",
        "izquierda",
        "abajo",
        "nueva partida"
    ]
    
    print("Simulando partida completa...")
    comandos_validos = 0
    
    for comando in comandos_partida:
        resultado = analizador.mostrar_analisis(comando)
        if analizador.es_valido():
            comandos_validos += 1
    
    print(f"\n📈 Resumen de la partida:")
    print(f"   - Comandos totales: {len(comandos_partida)}")
    print(f"   - Comandos válidos: {comandos_validos}")
    print(f"   - Tasa de éxito: {(comandos_validos/len(comandos_partida))*100:.1f}%")
    
    # Generar visualizaciones
    print("\n🎨 Generando visualizaciones...")
    
    # Generar autómata
    ruta_automata = analizador.generar_automata_html("test_complete.html")
    print(f"🤖 Autómata: {ruta_automata}")
    
    # Obtener estado final
    estado_final = analizador.obtener_estado_automata()
    print(f"🎯 Estado final del autómata:")
    print(f"   - Estados: {estado_final['estadisticas']['total_estados']}")
    print(f"   - Transiciones: {estado_final['estadisticas']['total_transiciones']}")
    print(f"   - Estado actual: {estado_final['estado_actual']}")
    
    return analizador

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA AFND")
    print("=" * 60)
    
    try:
        # Prueba básica
        integracion1 = test_automata_basic()
        
        # Prueba de generación HTML
        test_html_generation()
        
        # Prueba de exportación JSON
        test_json_export()
        
        # Prueba de integración completa
        analizador = test_integration_complete()
        
        print("\n🎉 TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 60)
        
        # Preguntar qué visualizar
        print("\nOpciones disponibles:")
        print("1. Abrir autómata de prueba básica")
        print("2. Abrir autómata de integración completa")
        print("3. Salir")
        
        opcion = input("Seleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            integracion1.generar_automata_html()
            ruta = os.path.join(os.path.dirname(__file__), 'frontend', 'templates', 'automata_juego.html')
            webbrowser.open(f'file://{os.path.abspath(ruta)}')
        elif opcion == "2":
            analizador.mostrar_automata()
        
        print("✅ Pruebas finalizadas")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
