#!/usr/bin/env python3
"""
Script para convertir archivos FASTA a formato TNT
Versión corregida - sin errores de taxnames
"""

def fasta_to_tnt(input_fasta, output_tnt):
    """
    Convierte un archivo FASTA a formato TNT para análisis filogenético
    
    Args:
        input_fasta: ruta al archivo FASTA de entrada
        output_tnt: ruta al archivo TNT de salida
    """
    taxa = []
    current_seq = ""
    
    # Leer el archivo FASTA
    with open(input_fasta, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                # Guardar la secuencia anterior si existe
                if current_seq:
                    taxa[-1] = (taxa[-1][0], current_seq)
                
                # Procesar el nombre del taxón
                # Solo toma la primera palabra (nombre del taxón)
                # y elimina espacios o texto adicional
                name = line[1:].split()[0].replace(" ", "_")
                taxa.append((name, ""))
                current_seq = ""
            else:
                # Acumular la secuencia
                current_seq += line
        
        # Guardar la última secuencia
        if current_seq:
            taxa[-1] = (taxa[-1][0], current_seq)

    # Escribir el archivo TNT
    with open(output_tnt, 'w') as f:
        # Definir el tipo de datos
        f.write("nstates dna;\n")
        
        # Inicio del bloque de lectura
        f.write("xread\n")
        
        # Dimensiones de la matriz (caracteres taxones)
        f.write(f"{len(taxa[0][1])} {len(taxa)}\n")
        
        # Escribir cada taxón con su secuencia
        for name, seq in taxa:
            f.write(f"{name} {seq}\n")
        
        # Cerrar bloque de lectura y procesar
        f.write(";\n")
        f.write("proc/;\n")
    
    # Imprimir resumen
    print(f"✓ Conversión completada exitosamente")
    print(f"  Archivo de entrada: {input_fasta}")
    print(f"  Archivo de salida: {output_tnt}")
    print(f"  Número de taxones: {len(taxa)}")
    print(f"  Longitud de secuencia: {len(taxa[0][1])}")
    print(f"\nTaxones procesados:")
    for i, (name, seq) in enumerate(taxa, 1):
        print(f"  {i}. {name}")

# Ejecutar la conversión
if __name__ == "__main__":
    fasta_to_tnt('supermatriz.fasta', 'supermatriz.tnt')
