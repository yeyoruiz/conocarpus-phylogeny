"""
Descarga secuencias NCBI para filogenia Combretaceae - VERSIÓN FINAL
═══════════════════════════════════════════════════════════════════
Proyecto: Test de monofilia Laguncularia-Conocarpus
Base científica: Gere et al. (2015), Tan et al. (2002), SciSpace review

ESPECIES: 20 (4 manglares + 12 terrestres Combretaceae + 4 outgroup)
MARCADORES: 5 confirmados por literatura
- ITS (nuclear)
- matK, rbcL (cloroplasto conservado)
- psaA-ycf3, trnH-psbA (cloroplasto variable)

REFERENCIA:
Gere et al. (2015). African continent a likely origin of family 
combretaceae. Annual Research & Review in Biology 9(1): 1-13.
Tan et al. (2002). Phylogenetic relationships of Combretoideae 
inferred from plastid and nuclear sequences. J Plant Res 115: 67-76.
"""

from Bio import Entrez
import time, os, re, csv
from datetime import datetime

# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════

Entrez.email = "tu_correo@ecosur.mx"  # ← CAMBIAR OBLIGATORIO
NCBI_API_KEY = None  # ← OPCIONAL pero recomendado

# ── Lista de especies basada en literatura ────────────────────
# Grupos funcionales:
# A = Manglares (target taxa)
# B = Terrestres Neotropical (posibles ancestros Laguncularia/Conocarpus)
# C = Terrestres Paleotropical (posibles ancestros Lumnitzera)
# D = Outgroup (Lythraceae - familia hermana)

ESPECIES = {
    # ── GRUPO A: MANGLARES (4) ────────────────────────────────
    "Laguncularia racemosa": {
        "sinonimos": [],
        "grupo": "A",
        "notas": "Mangle blanco neotropical - especie focal"
    },
    "Conocarpus erectus": {
        "sinonimos": ["Conocarpus erectus var. sericeus"],
        "grupo": "A",
        "notas": "Mangle botón - test de monofilia con Laguncularia"
    },
    "Lumnitzera racemosa": {
        "sinonimos": [],
        "grupo": "A",
        "notas": "Indo-Pacífico - potencial hermana de Laguncularia (Tan 2002)"
    },
    "Lumnitzera littorea": {
        "sinonimos": [],
        "grupo": "A",
        "notas": "Indo-Pacífico - congenérico de L. racemosa"
    },
    
    # ── GRUPO B: TERRESTRES NEOTROPICALES (6) ─────────────────
    "Terminalia catappa": {
        "sinonimos": [],
        "grupo": "B",
        "notas": "Almendro tropical - abundante en GenBank"
    },
    "Terminalia amazonia": {
        "sinonimos": ["Terminalia oblonga"],
        "grupo": "B",
        "notas": "Amazonia - hermano cercano T. catappa"
    },
    "Buchenavia tetraphylla": {
        "sinonimos": [],
        "grupo": "B",
        "notas": "Brasil - género hermano de Terminalia"
    },
    "Bucida buceras": {
        "sinonimos": ["Terminalia buceras"],
        "grupo": "B",
        "notas": "Caribe - transición manglar-terrestre"
    },
    "Combretum fruticosum": {
        "sinonimos": [],
        "grupo": "B",
        "notas": "Mesoamérica - liana"
    },
    "Combretum laxum": {
        "sinonimos": [],
        "grupo": "B",
        "notas": "Sudamérica - hermano C. fruticosum"
    },
    
    # ── GRUPO C: TERRESTRES PALEOTROPICALES (6) ───────────────
    "Terminalia superba": {
        "sinonimos": [],
        "grupo": "C",
        "notas": "África occidental - origen Combretaceae (Gere 2015)"
    },
    "Terminalia mantaly": {
        "sinonimos": [],
        "grupo": "C",
        "notas": "Madagascar - evidencia Gondwana"
    },
    "Combretum imberbe": {
        "sinonimos": [],
        "grupo": "C",
        "notas": "África austral"
    },
    "Combretum molle": {
        "sinonimos": [],
        "grupo": "C",
        "notas": "África tropical"
    },
    "Quisqualis indica": {
        "sinonimos": [],
        "grupo": "C",
        "notas": "Asia - basal en Combretaceae (Tan 2002)"
    },
    "Calycopteris floribunda": {
        "sinonimos": [],
        "grupo": "C",
        "notas": "India - hermano Quisqualis"
    },
    
    # ── GRUPO D: OUTGROUP LYTHRACEAE (4) ──────────────────────
    "Lagerstroemia indica": {
        "sinonimos": [],
        "grupo": "D",
        "notas": "Lythraceae - ornamental común, datos abundantes"
    },
    "Punica granatum": {
        "sinonimos": [],
        "grupo": "D",
        "notas": "Lythraceae - granado, genoma secuenciado"
    },
    "Trapa natans": {
        "sinonimos": [],
        "grupo": "D",
        "notas": "Lythraceae - acuática, convergencia ecológica"
    },
    "Lawsonia inermis": {
        "sinonimos": [],
        "grupo": "D",
        "notas": "Lythraceae - henna"
    },
}

# ── Marcadores confirmados por literatura ─────────────────────
# Basado en: Gere 2015, Tan 2002, Zhang 2020, Gere 2013

MARCADORES = {
    "ITS": {
        "queries": [
            '"internal transcribed spacer"[Title]',
            '"ITS"[Gene Name] AND "ribosomal"[All Fields]',
            'ITS1[All Fields] OR ITS2[All Fields]',
        ],
        "tipo": "nuclear",
        "referencia": "Gere 2015, Tan 2002"
    },
    "matK": {
        "queries": [
            '"matK"[Gene Name]',
            '"maturase K"[All Fields]',
        ],
        "tipo": "plastid_conservado",
        "referencia": "Gere 2015, Tan 2002, Zhang 2020"
    },
    "rbcL": {
        "queries": [
            '"rbcL"[Gene Name]',
            '"ribulose bisphosphate carboxylase"[All Fields]',
        ],
        "tipo": "plastid_conservado",
        "referencia": "Gere 2015, Tan 2002"
    },
    "psaA-ycf3": {
        "queries": [
            '"psaA"[Gene Name] AND "ycf3"[Gene Name]',
            '"psaA-ycf3"[All Fields]',
            '"PY-IGS"[All Fields]',  # Nombre alternativo usado por Tan 2002
        ],
        "tipo": "plastid_variable",
        "referencia": "Gere 2015, Tan 2002 (PY-IGS)"
    },
    "trnH-psbA": {
        "queries": [
            '"trnH-psbA"[Gene Name]',
            '"trnH"[Gene Name] AND "psbA"[Gene Name]',
            '"psbA-trnH"[All Fields]',
        ],
        "tipo": "plastid_variable",
        "referencia": "Gere 2015, Gere 2013 (barcoding)"
    },
}

CARPETA_SALIDA = "combretaceae_sequences_final"
PAUSA = 0.35 if NCBI_API_KEY else 0.5

# ══════════════════════════════════════════════════════════════
# FUNCIONES
# ══════════════════════════════════════════════════════════════

def sanitize(texto):
    """Limpia nombre para filesystem"""
    return re.sub(r'[^\w\-.]', '_', texto)


def construir_queries(especie, marcador_queries):
    """Genera queries organism + marcador"""
    return [f'("{especie}"[Organism]) AND ({mq})' for mq in marcador_queries]


def buscar_ids(queries, retmax=100):
    """Prueba queries hasta encontrar hits"""
    for query in queries:
        try:
            handle = Entrez.esearch(
                db="nucleotide",
                term=query,
                retmax=retmax,
                api_key=NCBI_API_KEY,
            )
            record = Entrez.read(handle)
            handle.close()
            
            ids = record["IdList"]
            total = int(record["Count"])
            
            if ids:
                return ids, total, query
            
            time.sleep(PAUSA)
        except Exception as e:
            print(f"      [ERROR búsqueda] {e}")
            continue
    
    return [], 0, queries[-1]


def descargar_fasta(ids):
    """Descarga FASTA desde lista de IDs"""
    if not ids:
        return ""
    
    try:
        handle = Entrez.efetch(
            db="nucleotide",
            id=ids,
            rettype="fasta",
            retmode="text",
            api_key=NCBI_API_KEY,
        )
        fasta_text = handle.read()
        handle.close()
        return fasta_text
    except Exception as e:
        print(f"      [ERROR descarga] {e}")
        return ""


def main():
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    
    # Timestamp
    inicio = datetime.now()
    
    print("\n" + "═" * 80)
    print("  COMBRETACEAE PHYLOGENY SEQUENCE DOWNLOAD")
    print("  Test de monofilia Laguncularia-Conocarpus")
    print("  Basado en: Gere et al. (2015), Tan et al. (2002)")
    print("═" * 80)
    print(f"  Especies: {len(ESPECIES)}")
    print(f"  Marcadores: {len(MARCADORES)}")
    print(f"  Total combinaciones: {len(ESPECIES) * len(MARCADORES)}")
    print(f"  Inicio: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 80 + "\n")
    
    resumen = []
    
    for especie_principal, info in ESPECIES.items():
        sinonimos = info["sinonimos"]
        grupo = info["grupo"]
        nombres_a_intentar = [especie_principal] + sinonimos
        
        print(f"\n{'─' * 80}")
        print(f"  {especie_principal} (Grupo {grupo})")
        print(f"  Nota: {info['notas']}")
        print(f"{'─' * 80}")
        
        for marcador_key, marcador_info in MARCADORES.items():
            marcador_queries = marcador_info["queries"]
            
            print(f"\n    [{marcador_key}] ({marcador_info['tipo']})")
            print(f"    Ref: {marcador_info['referencia']}")
            
            encontrado = False
            
            for nombre in nombres_a_intentar:
                if nombre != especie_principal:
                    print(f"      → Intentando sinónimo: {nombre}")
                
                queries = construir_queries(nombre, marcador_queries)
                
                try:
                    ids, total, query_ok = buscar_ids(queries)
                except Exception as e:
                    print(f"      [ERROR] {e}")
                    continue
                
                if not ids:
                    print(f"      ✗ Sin resultados para: {nombre}")
                    time.sleep(PAUSA)
                    continue
                
                # ── HIT ──
                print(f"      ✓ Encontrados: {total} | Descargando: {len(ids)}")
                
                time.sleep(PAUSA)
                fasta_text = descargar_fasta(ids)
                
                if not fasta_text:
                    resumen.append({
                        "especie": especie_principal,
                        "grupo": grupo,
                        "marcador": marcador_key,
                        "n_seqs": 0,
                        "estado": "ERROR descarga",
                        "nombre_usado": nombre
                    })
                    encontrado = True
                    break
                
                # Guardar
                nombre_archivo = f"{sanitize(especie_principal)}_{marcador_key}.fasta"
                ruta = os.path.join(CARPETA_SALIDA, nombre_archivo)
                
                with open(ruta, "w") as f:
                    f.write(fasta_text)
                
                n_seqs = fasta_text.count(">")
                estado = "OK" if nombre == especie_principal else f"Sinónimo: {nombre}"
                
                print(f"      💾 {nombre_archivo} ({n_seqs} seqs)")
                
                resumen.append({
                    "especie": especie_principal,
                    "grupo": grupo,
                    "marcador": marcador_key,
                    "n_seqs": n_seqs,
                    "estado": estado,
                    "nombre_usado": nombre
                })
                encontrado = True
                break
            
            if not encontrado:
                resumen.append({
                    "especie": especie_principal,
                    "grupo": grupo,
                    "marcador": marcador_key,
                    "n_seqs": 0,
                    "estado": "Sin datos",
                    "nombre_usado": especie_principal
                })
            
            time.sleep(PAUSA)
    
    # ══════════════════════════════════════════════════════════
    # RESUMEN Y ESTADÍSTICAS
    # ══════════════════════════════════════════════════════════
    
    fin = datetime.now()
    duracion = (fin - inicio).total_seconds() / 60
    
    print("\n" + "═" * 80)
    print("  RESUMEN FINAL")
    print("═" * 80)
    
    # Tabla resumen
    print(f"\n{'Especie':<32} {'Grupo':<6} {'Marc.':<10} {'Seqs':<6} Estado")
    print("─" * 80)
    
    for r in resumen:
        print(f"{r['especie']:<32} {r['grupo']:<6} {r['marcador']:<10} "
              f"{r['n_seqs']:<6} {r['estado']}")
    
    # Estadísticas globales
    total_seqs = sum(r["n_seqs"] for r in resumen)
    archivos_ok = sum(1 for r in resumen if r["n_seqs"] > 0)
    sin_datos = sum(1 for r in resumen if r["n_seqs"] == 0)
    total_combinaciones = len(ESPECIES) * len(MARCADORES)
    
    print("─" * 80)
    print(f"  Archivos generados: {archivos_ok}/{total_combinaciones}")
    print(f"  Secuencias totales: {total_seqs}")
    print(f"  Combinaciones sin datos: {sin_datos}")
    print(f"  Cobertura: {(archivos_ok/total_combinaciones)*100:.1f}%")
    print(f"  Duración: {duracion:.1f} minutos")
    print(f"\n  📁 Carpeta: ./{CARPETA_SALIDA}/\n")
    
    # Estadísticas por grupo
    print("\n" + "─" * 80)
    print("  COBERTURA POR GRUPO")
    print("─" * 80)
    
    for grupo_id in ["A", "B", "C", "D"]:
        grupo_data = [r for r in resumen if r["grupo"] == grupo_id]
        grupo_ok = sum(1 for r in grupo_data if r["n_seqs"] > 0)
        grupo_total = len(grupo_data)
        
        grupo_nombre = {
            "A": "Manglares",
            "B": "Terrestres Neotropical",
            "C": "Terrestres Paleotropical",
            "D": "Outgroup Lythraceae"
        }[grupo_id]
        
        print(f"  Grupo {grupo_id} ({grupo_nombre}): "
              f"{grupo_ok}/{grupo_total} ({(grupo_ok/grupo_total)*100:.1f}%)")
    
    # Especies problemáticas
    especies_sin_datos = {}
    for r in resumen:
        if r["n_seqs"] == 0:
            if r["especie"] not in especies_sin_datos:
                especies_sin_datos[r["especie"]] = []
            especies_sin_datos[r["especie"]].append(r["marcador"])
    
    if especies_sin_datos:
        print("\n" + "─" * 80)
        print("  ⚠️  ESPECIES CON DATOS FALTANTES")
        print("─" * 80)
        for esp, marcadores in especies_sin_datos.items():
            print(f"  {esp}: {', '.join(marcadores)}")
        print("\n  → Estas especies pueden requerir búsqueda manual")
        print("  → O considerar excluirlas del análisis final")
    
    # ── EXPORTAR CSV DETALLADO ───────────────────────────────
    csv_path = os.path.join(CARPETA_SALIDA, "resumen_descarga.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["especie", "grupo", "marcador", "n_seqs", "estado", "nombre_usado"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(resumen)
    
    print(f"\n  📊 Resumen CSV: {csv_path}")
    
    # ── METADATA ──────────────────────────────────────────────
    metadata_path = os.path.join(CARPETA_SALIDA, "metadata.txt")
    with open(metadata_path, "w") as f:
        f.write("COMBRETACEAE PHYLOGENY - METADATA\n")
        f.write("═" * 80 + "\n\n")
        f.write(f"Fecha: {inicio.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Usuario: {Entrez.email}\n")
        f.write(f"Especies: {len(ESPECIES)}\n")
        f.write(f"Marcadores: {len(MARCADORES)}\n\n")
        
        f.write("REFERENCIAS:\n")
        f.write("  Gere et al. (2015). African continent a likely origin of\n")
        f.write("    family Combretaceae. Ann Res Rev Biol 9(1): 1-13.\n")
        f.write("  Tan et al. (2002). Phylogenetic relationships of Combretoideae\n")
        f.write("    inferred from plastid and nuclear sequences. J Plant Res 115: 67-76.\n\n")
        
        f.write("MARCADORES:\n")
        for m, info in MARCADORES.items():
            f.write(f"  {m}: {info['tipo']} ({info['referencia']})\n")
        
        f.write("\n" + "─" * 80 + "\n")
        f.write("NOTAS ESPECIES:\n")
        for esp, info in ESPECIES.items():
            f.write(f"  {esp} (Grupo {info['grupo']}): {info['notas']}\n")
    
    print(f"  📝 Metadata: {metadata_path}\n")
    print("═" * 80 + "\n")


if __name__ == "__main__":
    main()
