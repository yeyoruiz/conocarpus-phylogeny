#!/usr/bin/env python3
"""
CONSOLIDADOR DE FASTAS - PROYECTO MANGLARES COMBRETACEAE 2026
==============================================================
Propósito: Tomar los ~100 archivos individuales generados por limpiar_fastas
          y consolidarlos en 5 archivos multi-FASTA (uno por marcador)
          listos para alineamiento con MAFFT.

Input:  fastas_individuales_curados/*.fasta (~100 archivos)
Output: alineamiento_input/*.fasta (5 archivos multi-FASTA)
"""

from pathlib import Path
from collections import defaultdict

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

MARCADORES = ['ITS', 'matK', 'rbcL', 'psaA-ycf3', 'trnH-psbA']

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    input_dir = Path("fastas_individuales_curados")
    output_dir = Path("alineamiento_input")
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 80)
    print("📦 CONSOLIDACIÓN DE FASTAS PARA MAFFT")
    print("=" * 80)
    print(f"\n📁 Entrada:  {input_dir}")
    print(f"📁 Salida:   {output_dir}\n")
    
    if not input_dir.exists():
        print(f"❌ ERROR: Directorio {input_dir} no existe")
        print("   Ejecuta primero: python limpiar_fastas_v3_CORREGIDO.py")
        return
    
    # Agrupar archivos por marcador
    archivos_por_marcador = defaultdict(list)
    
    for archivo in sorted(input_dir.glob("*.fasta")):
        # Formato: Especie_nombre_marcador.fasta
        marcador = archivo.stem.split('_')[-1]
        
        if marcador in MARCADORES:
            archivos_por_marcador[marcador].append(archivo)
    
    # Consolidar cada marcador en un multi-FASTA
    for marcador in MARCADORES:
        archivos = archivos_por_marcador[marcador]
        
        if not archivos:
            print(f"⚠️  {marcador:12} → Sin archivos encontrados")
            continue
        
        output_file = output_dir / f"{marcador}_all.fasta"
        n_secuencias = 0
        longitudes = []
        
        with open(output_file, 'w') as out_f:
            for archivo in sorted(archivos):
                # Leer contenido completo del archivo
                with open(archivo, 'r') as in_f:
                    contenido = in_f.read()
                    
                    # Escribir al archivo consolidado
                    out_f.write(contenido)
                    
                    # Contar secuencias (cada header es una secuencia)
                    n_secuencias += contenido.count('>')
                    
                    # Extraer longitud (líneas que no empiezan con '>')
                    seq_lines = [line.strip() for line in contenido.split('\n') 
                                 if line.strip() and not line.startswith('>')]
                    if seq_lines:
                        longitud = sum(len(line) for line in seq_lines)
                        longitudes.append(longitud)
        
        # Estadísticas
        if longitudes:
            min_len = min(longitudes)
            max_len = max(longitudes)
            avg_len = sum(longitudes) / len(longitudes)
            
            print(f"✅ {marcador:12} → {n_secuencias:2} secuencias "
                  f"(long: {min_len:4}-{max_len:4} bp, avg: {avg_len:6.1f} bp)")
        else:
            print(f"⚠️  {marcador:12} → Archivo vacío")
    
    print("\n" + "=" * 80)
    print("✅ CONSOLIDACIÓN COMPLETADA")
    print("=" * 80)
    print(f"\n📁 Archivos generados en: {output_dir}/\n")
    
    # Instrucciones para siguiente paso
    print("🔬 SIGUIENTE PASO - ALINEAMIENTO CON MAFFT:")
    print("-" * 80)
    print("cd alineamiento_input/\n")
    
    for marcador in MARCADORES:
        if archivos_por_marcador[marcador]:
            print(f"mafft --maxiterate 1000 --localpair {marcador}_all.fasta > {marcador}_aligned.fasta")
    
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
