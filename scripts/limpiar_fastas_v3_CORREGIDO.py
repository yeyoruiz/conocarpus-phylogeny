#!/usr/bin/env python3
"""
LIMPIEZA DE FASTA CORREGIDA - PROYECTO MANGLARES COMBRETACEAE 2026
===================================================================
Propósito: Seleccionar la mejor secuencia por especie/marcador y generar
          archivos INDIVIDUALES (un FASTA por especie-marcador).
          
PROBLEMA ANTERIOR: Generaba 5 archivos consolidados (uno por marcador).
SOLUCIÓN: Genera ~100 archivos individuales (20 especies × 5 marcadores).
"""

import os
from pathlib import Path
from collections import defaultdict

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

LONGITUD_CONFIG = {
    'ITS':       {'min': 300,  'max': 1000,  'optimo': 650},
    'trnH-psbA': {'min': 200,  'max': 1200,  'optimo': 550},
    'matK':      {'min': 400,  'max': 1500,  'optimo': 850},
    'rbcL':      {'min': 500,  'max': 2000,  'optimo': 1400},
    'psaA-ycf3': {'min': 300,  'max': 1200,  'optimo': 750}
}

EXCLUIR_KEYWORDS = ['complete genome', 'whole genome', 'scaffold', 'chloroplast genome']
PREFERIR_KEYWORDS = ['gene', 'spacer', 'internal transcribed spacer', 'partial']

# ============================================================================
# FUNCIONES
# ============================================================================

def leer_fasta(archivo):
    """Lee archivo FASTA y retorna lista de diccionarios con header, seq, length"""
    secuencias = []
    header_actual = None
    seq_actual = []
    
    try:
        with open(archivo, 'r', encoding='utf-8', errors='replace') as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                    
                if linea.startswith('>'):
                    # Guardar secuencia anterior
                    if header_actual:
                        seq_str = ''.join(seq_actual).upper().replace(' ', '')
                        # Filtrar secuencias con >20% bases ambiguas
                        n_ambiguous = sum(seq_str.count(base) for base in 'NYRSWKMBDHV')
                        prop_ambiguous = n_ambiguous / len(seq_str) if len(seq_str) > 0 else 1.0
                        
                        if prop_ambiguous <= 0.20:  # Máximo 20% ambiguas
                            secuencias.append({
                                'header': header_actual,
                                'seq': seq_str,
                                'length': len(seq_str)
                            })
                    
                    header_actual = linea[1:]  # Remover '>'
                    seq_actual = []
                else:
                    seq_actual.append(linea)
            
            # Última secuencia
            if header_actual:
                seq_str = ''.join(seq_actual).upper().replace(' ', '')
                n_ambiguous = sum(seq_str.count(base) for base in 'NYRSWKMBDHV')
                prop_ambiguous = n_ambiguous / len(seq_str) if len(seq_str) > 0 else 1.0
                
                if prop_ambiguous <= 0.20:
                    secuencias.append({
                        'header': header_actual,
                        'seq': seq_str,
                        'length': len(seq_str)
                    })
                    
    except Exception as e:
        print(f"⚠️  Error leyendo {archivo}: {e}")
        return []
    
    return secuencias


def calcular_score(seq_info, marcador):
    """Calcula score de calidad para una secuencia"""
    score = 0
    header = seq_info['header'].lower()
    length = seq_info['length']
    config = LONGITUD_CONFIG.get(marcador, {'min': 300, 'optimo': 600, 'max': 1500})
    
    # PENALIZACIÓN FUERTE: Genomas completos
    if any(kw in header for kw in EXCLUIR_KEYWORDS):
        if length > 5000:
            return -10000  # Descartar completamente
        else:
            score -= 500  # Penalizar pero no descartar
    
    # FILTRO: Longitud dentro de rango permitido
    if length < config['min']:
        return -5000  # Muy corto, descartar
    if length > config['max']:
        return -3000  # Muy largo, probablemente genoma
    
    # SCORE PRINCIPAL: Cercanía al óptimo
    distancia = abs(length - config['optimo'])
    score += max(0, 1000 - distancia)
    
    # BONOS: Palabras clave de calidad
    if any(kw in header for kw in PREFERIR_KEYWORDS):
        score += 200
    
    # BONO: Longitud casi exacta al óptimo (±50 bp)
    if distancia <= 50:
        score += 300
    
    return score


def main():
    input_dir = Path("combretaceae_sequences_final")
    output_dir = Path("fastas_individuales_curados")
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 80)
    print("🧬 LIMPIEZA DE FASTAS - VERSIÓN CORREGIDA")
    print("=" * 80)
    print(f"\n📁 Entrada:  {input_dir}")
    print(f"📁 Salida:   {output_dir}\n")
    
    if not input_dir.exists():
        print(f"❌ ERROR: Directorio {input_dir} no existe")
        return
    
    archivos_procesados = 0
    archivos_generados = 0
    especies_por_marcador = defaultdict(int)
    
    # Procesar cada archivo FASTA de entrada
    for archivo in sorted(input_dir.glob("*.fasta")):
        archivos_procesados += 1
        
        # Extraer especie y marcador del nombre del archivo
        # Formato esperado: "Especie_nombre_marcador.fasta"
        partes = archivo.stem.split('_')
        if len(partes) < 2:
            print(f"⚠️  Saltando {archivo.name} (formato no reconocido)")
            continue
        
        marcador = partes[-1]
        especie = "_".join(partes[:-1])
        
        # Verificar que el marcador sea válido
        if marcador not in LONGITUD_CONFIG:
            print(f"⚠️  Saltando {archivo.name} (marcador '{marcador}' no reconocido)")
            continue
        
        # Leer todas las secuencias del archivo
        secuencias = leer_fasta(archivo)
        
        if not secuencias:
            print(f"⚠️  {especie} × {marcador}: Sin secuencias válidas")
            continue
        
        # Calcular scores para todas las secuencias
        scores = [(seq, calcular_score(seq, marcador)) for seq in secuencias]
        scores_positivos = [(seq, sc) for seq, sc in scores if sc > 0]
        
        if not scores_positivos:
            print(f"❌ {especie} × {marcador}: Todas las secuencias descartadas (baja calidad)")
            continue
        
        # Seleccionar la MEJOR secuencia (score más alto)
        mejor_seq, mejor_score = max(scores_positivos, key=lambda x: x[1])
        
        # Generar archivo individual para esta especie-marcador
        output_file = output_dir / f"{especie}_{marcador}.fasta"
        
        with open(output_file, 'w') as f:
            # Header simplificado: solo especie y marcador
            f.write(f">{especie}\n")
            
            # Escribir secuencia en líneas de 80 caracteres (estándar FASTA)
            seq = mejor_seq['seq']
            for i in range(0, len(seq), 80):
                f.write(seq[i:i+80] + '\n')
        
        archivos_generados += 1
        especies_por_marcador[marcador] += 1
        
        print(f"✅ {especie:40} × {marcador:10} → {mejor_seq['length']:4} bp (score: {mejor_score:4})")
    
    # RESUMEN FINAL
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE LIMPIEZA")
    print("=" * 80)
    print(f"Archivos procesados:  {archivos_procesados}")
    print(f"Archivos generados:   {archivos_generados}")
    print(f"\n📈 COBERTURA POR MARCADOR:")
    print("-" * 80)
    
    for marcador in sorted(LONGITUD_CONFIG.keys()):
        n_especies = especies_por_marcador.get(marcador, 0)
        porcentaje = (n_especies / 20) * 100  # Asumiendo 20 especies objetivo
        barra = "█" * int(porcentaje / 5) + "░" * (20 - int(porcentaje / 5))
        print(f"{marcador:12} │ {barra} │ {n_especies:2}/20 especies ({porcentaje:5.1f}%)")
    
    print("\n" + "=" * 80)
    print(f"✅ COMPLETADO - {archivos_generados} archivos listos para alineamiento")
    print(f"📁 Ver: {output_dir}/")
    print("=" * 80 + "\n")
    
    # SIGUIENTE PASO
    print("🔬 PRÓXIMO PASO:")
    print("   Alinear cada marcador con:")
    print("   mafft --maxiterate 1000 --localpair ITS_*.fasta > ITS_aligned.fasta")
    print()


if __name__ == "__main__":
    main()
