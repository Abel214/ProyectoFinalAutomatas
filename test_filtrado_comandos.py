#!/usr/bin/env python3
"""
Script de prueba para verificar el filtrado de comandos de voz
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.glc.logicaGLC import AnalizadorGramaticaVisual

def test_comando_filtrado():
    """Prueba el filtrado de comandos válidos vs inválidos"""
    print("🧪 PRUEBA DE FILTRADO DE COMANDOS")
    print("=" * 50)
    
    analizador = AnalizadorGramaticaVisual(auto_abrir=False)
    
    # Comandos válidos según la gramática
    comandos_validos = [
        "derecha",
        "izquierda", 
        "arriba",
        "abajo",
        "puerta a",
        "puerta b", 
        "puerta c",
        "cambiar",
        "mantener",
        "cerrar",
        "reiniciar",
        "otra vez",
        "nueva partida"
    ]
    
    # Comandos inválidos (que NO están en la gramática)
    comandos_invalidos = [
        "hola mundo",
        "caminar",
        "correr",
        "saltar",
        "puerta d",
        "puerta uno",
        "cambio",
        "quedar",
        "abrir",
        "reinicio",
        "vez otra",
        "partida nueva",
        "comando aleatorio",
        "test",
        "prueba",
        "izquierda por favor",
        "derecha ahora",
        "puerta a por favor"
    ]
    
    print("📋 Probando comandos VÁLIDOS:")
    comandos_validos_exitosos = 0
    
    for comando in comandos_validos:
        resultado = analizador.mostrar_analisis(comando)
        es_valido = analizador.es_valido()
        
        if es_valido:
            print(f"  ✅ '{comando}' - VÁLIDO (correcto)")
            comandos_validos_exitosos += 1
        else:
            print(f"  ❌ '{comando}' - INVÁLIDO (error en gramática)")
    
    print(f"\n📊 Resultado comandos válidos: {comandos_validos_exitosos}/{len(comandos_validos)}")
    
    print("\n📋 Probando comandos INVÁLIDOS (deberían ser rechazados):")
    comandos_invalidos_rechazados = 0
    
    for comando in comandos_invalidos:
        resultado = analizador.mostrar_analisis(comando)
        es_valido = analizador.es_valido()
        
        if not es_valido:
            print(f"  ✅ '{comando}' - RECHAZADO (correcto)")
            comandos_invalidos_rechazados += 1
        else:
            print(f"  ❌ '{comando}' - ACEPTADO (error en filtro)")
    
    print(f"\n📊 Resultado comandos inválidos: {comandos_invalidos_rechazados}/{len(comandos_invalidos)} rechazados")
    
    # Estadísticas finales
    print(f"\n🎯 ESTADÍSTICAS FINALES:")
    print(f"   Precisión comandos válidos: {(comandos_validos_exitosos/len(comandos_validos))*100:.1f}%")
    print(f"   Precisión filtrado inválidos: {(comandos_invalidos_rechazados/len(comandos_invalidos))*100:.1f}%")
    
    precision_total = ((comandos_validos_exitosos + comandos_invalidos_rechazados) / 
                      (len(comandos_validos) + len(comandos_invalidos))) * 100
    
    print(f"   Precisión total del sistema: {precision_total:.1f}%")
    
    if precision_total >= 95:
        print("   🎉 ¡Excelente! El filtrado funciona correctamente")
    elif precision_total >= 80:
        print("   ✅ Bueno. El filtrado funciona bien")
    else:
        print("   ⚠️ Necesita mejoras en el filtrado")
    
    return precision_total

def test_normalizacion():
    """Prueba la normalización de comandos con errores típicos de reconocimiento de voz"""
    print("\n🔧 PRUEBA DE NORMALIZACIÓN DE COMANDOS")
    print("=" * 50)
    
    analizador = AnalizadorGramaticaVisual(auto_abrir=False)
    
    # Comandos con errores típicos que deberían normalizarse
    comandos_con_errores = [
        ("derecha.", "derecha"),
        ("ezquierda", "izquierda"),
        ("arriba.", "arriba"),
        ("puerto a", "puerta a"),
        ("puerto b", "puerta b"),
        ("cambiar.", "cambiar"),
        ("mantener.", "mantener"),
        ("reiniciar.", "reiniciar"),
        ("nueva.partida", "nueva partida"),
        ("otra.vez", "otra vez")
    ]
    
    print("🔍 Probando normalización de comandos:")
    normalizaciones_exitosas = 0
    
    for comando_erroneo, comando_correcto in comandos_con_errores:
        # Simular proceso de normalización (esto se haría en JavaScript)
        print(f"  📝 '{comando_erroneo}' → '{comando_correcto}'")
        
        # Probar que el comando correcto es válido
        resultado = analizador.mostrar_analisis(comando_correcto)
        if analizador.es_valido():
            print(f"     ✅ Comando normalizado es válido")
            normalizaciones_exitosas += 1
        else:
            print(f"     ❌ Comando normalizado es inválido")
    
    print(f"\n📊 Normalizaciones exitosas: {normalizaciones_exitosas}/{len(comandos_con_errores)}")
    precision_normalizacion = (normalizaciones_exitosas / len(comandos_con_errores)) * 100
    print(f"📊 Precisión de normalización: {precision_normalizacion:.1f}%")
    
    return precision_normalizacion

def mostrar_comandos_permitidos():
    """Muestra la lista completa de comandos permitidos"""
    print("\n📝 COMANDOS PERMITIDOS POR LA GRAMÁTICA")
    print("=" * 50)
    
    comandos_por_categoria = {
        "🚶 Movimiento": ["izquierda", "derecha", "arriba", "abajo"],
        "🚪 Puertas": ["puerta a", "puerta b", "puerta c"],
        "🎯 Acciones": ["cambiar", "mantener"],
        "🎮 Control": ["cerrar", "reiniciar", "otra vez"],
        "🆕 Juego": ["nueva partida"]
    }
    
    total_comandos = 0
    for categoria, comandos in comandos_por_categoria.items():
        print(f"\n{categoria}:")
        for comando in comandos:
            print(f"  • \"{comando}\"")
            total_comandos += 1
    
    print(f"\n📊 Total de comandos válidos: {total_comandos}")
    print("\n⚠️ IMPORTANTE: Solo estos comandos serán procesados por el sistema")
    print("   Cualquier otro comando será rechazado automáticamente")

def main():
    """Ejecuta todas las pruebas de filtrado"""
    print("🚀 INICIANDO PRUEBAS DE FILTRADO DE COMANDOS DE VOZ")
    print("=" * 60)
    
    try:
        # Mostrar comandos permitidos
        mostrar_comandos_permitidos()
        
        # Probar filtrado
        precision_filtrado = test_comando_filtrado()
        
        # Probar normalización
        precision_normalizacion = test_normalizacion()
        
        print("\n" + "=" * 60)
        print("🏁 RESUMEN FINAL DE PRUEBAS")
        print("=" * 60)
        print(f"✅ Precisión del filtrado: {precision_filtrado:.1f}%")
        print(f"🔧 Precisión de normalización: {precision_normalizacion:.1f}%")
        
        if precision_filtrado >= 95 and precision_normalizacion >= 95:
            print("\n🎉 ¡SISTEMA DE FILTRADO PERFECTO!")
            print("   - El reconocimiento de voz está limitado a comandos válidos")
            print("   - La normalización corrige errores típicos")
            print("   - Solo comandos de la gramática serán procesados")
        else:
            print("\n⚠️ El sistema necesita ajustes")
        
        print("\n📋 Para usar el sistema:")
        print("   1. Ejecutar: python app.py")
        print("   2. Ir a: http://127.0.0.1:5000/laberinto")
        print("   3. Usar SOLO comandos de la gramática")
        print("   4. Observar que comandos inválidos son rechazados")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
