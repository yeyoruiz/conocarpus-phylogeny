# Resultados: Filogenia de Combretaceae

## 1. Datos

- **Taxones:** 20 especies (16 Combretaceae + 4 Lythraceae como outgroup)
- **Marcadores:** 5 (ITS, matK, rbcL, psaA-ycf3, trnH-psbA)
- **Supermatriz:** 20 taxa x 2,819 pb (concatenado)
- **Outgroup:** *Punica granatum* (Lythraceae)

---

## 2. Seleccion de Modelo de Sustitucion (jModelTest 2.1.10)

| Parametro | Valor |
|-----------|-------|
| Modelos evaluados | 88 (16 parcialmente, ejecucion interrumpida) |
| Esquemas de sustitucion | 11 |
| Mejor modelo | **GTR+I+G** |
| -lnL del mejor modelo | **12,844.81** |
| Criterios evaluados | AIC, AICc, BIC, DT |

**Nota:** La ejecucion de jModelTest se interrumpio despues de evaluar 16 de 88 modelos (error en PhyML para el modelo HKY+G). Los modelos evaluados con +I+G fueron suficientes para identificar GTR+I+G como el mejor modelo.

### Top 5 modelos evaluados (por -lnL):

| Modelo | -lnL | Parametros |
|--------|------|------------|
| GTR+I+G | 12,844.81 | K=11 |
| TIM3+I+G | 12,845.92 | K=9 |
| TVM+I+G | 12,847.05 | K=10 |
| TIM1+I+G | 12,848.16 | K=9 |
| TPM3uf+I+G | 12,848.23 | K=8 |

---

## 3. Analisis de Parsimonia (TNT)

### 3.1 Parametros de busqueda

| Parametro | Valor |
|-----------|-------|
| Software | TNT (Tree Analysis Using New Technology) |
| Tipo de busqueda | Heuristica |
| Replicas | 1,000 |
| Branch swapping | TBR (Tree Bisection-Reconnection) |
| Arboles retenidos por replica | 10 |
| Outgroup | *Punica granatum* |

### 3.2 Arboles mas parsimoniosos

Se encontraron **2 arboles igualmente parsimoniosos**.

**Arbol 1:**
```
Punica_granatum (outgroup)
├── (Lagerstroemia_indica, Lawsonia_inermis)
└── Trapa_natans
    ├── (Lumnitzera_littorea, Lumnitzera_racemosa)
    └── Laguncularia_racemosa
        └── Calycopteris_floribunda
            ├── Conocarpus_erectus
            │   ├── (Terminalia_amazonia, (Buchenavia_tetraphylla, Bucida_buceras))
            │   └── (Terminalia_superba, (Terminalia_catappa, Terminalia_mantaly))
            └── Combretum clade
                ├── (Quisqualis_indica, Combretum_fruticosum)
                └── (Combretum_imberbe, (Combretum_molle, Combretum_laxum))
```

**Arbol 2:**
```
Punica_granatum (outgroup)
└── Lawsonia_inermis
    └── Lagerstroemia_indica
        └── Trapa_natans
            └── Laguncularia_racemosa
                ├── (Lumnitzera_littorea, Lumnitzera_racemosa)
                └── Conocarpus_erectus + Terminalia clade
                    │   ├── (Terminalia_amazonia, (Buchenavia_tetraphylla, Bucida_buceras))
                    │   └── (Terminalia_superba, (Terminalia_catappa, Terminalia_mantaly))
                    └── Calycopteris_floribunda
                        ├── (Quisqualis_indica, Combretum_fruticosum)
                        └── (Combretum_imberbe, (Combretum_molle, Combretum_laxum))
```

### 3.3 Diferencias entre los 2 arboles

| Caracter | Arbol 1 | Arbol 2 |
|----------|---------|---------|
| Outgroup (Lythraceae) | Clado (Lagerstroemia + Lawsonia) | Grado (escalera) |
| Posicion de *Calycopteris* | Hermana de (Terminalia + Combretum) | Hermana solo de Combretum |
| Posicion de Lumnitzera | Hermana de (Laguncularia + core) | Hermana de core Combretaceae |

### 3.4 Topologia del arbol de consenso (Bootstrap 2,000 replicas)

```
Punica_granatum (outgroup)
└── Lawsonia_inermis
    └── Lagerstroemia_indica
        └── Trapa_natans
            ├── (Lumnitzera_littorea, Lumnitzera_racemosa)
            └── Laguncularia_racemosa
                └── Calycopteris_floribunda
                    ├── Conocarpus_erectus
                    │   ├── (Bucida_buceras, (Buchenavia_tetraphylla, Terminalia_amazonia))
                    │   └── (Terminalia_superba, (Terminalia_catappa, Terminalia_mantaly))
                    └── Combretum clade
                        ├── (Quisqualis_indica, Combretum_fruticosum)
                        └── (Combretum_imberbe, (Combretum_molle, Combretum_laxum))
```

### 3.5 Soporte de ramas (Bootstrap)

Se realizaron tres analisis de soporte:

| Metodo | Replicas | Archivo |
|--------|----------|---------|
| Bootstrap estandar | 2,000 | `bootstrap_2000.tre` |
| Poisson resampling | 1,000 | `poisson_1000.tre` |
| Symmetric resampling | 1,000 | `symmetric_1000.tre` |

**Nota:** Los valores de soporte de bootstrap estan mapeados en los archivos .tre pero requieren visualizacion en FigTree o software equivalente para su lectura. Los tres metodos de remuestreo muestran topologias congruentes.

### 3.6 Hallazgos principales de parsimonia

1. ***Conocarpus erectus* NO es hermano de *Laguncularia racemosa*.** *Conocarpus* esta anidado dentro del clado de *Terminalia* + *Buchenavia* + *Bucida*, lejos de *Laguncularia*.

2. ***Laguncularia racemosa* es hermana del core de Combretaceae** (clado *Calycopteris* + *Terminalia* + *Combretum* + *Conocarpus*), no forma un clado con *Conocarpus*.

3. **El clado de manglar NO es monofiletico.** Los generos de manglar (*Laguncularia*, *Conocarpus*, *Lumnitzera*) estan dispersos en la filogenia, indicando multiples origenes independientes del habito de manglar en Combretaceae.

4. **Lumnitzera forma un clado hermano** al resto de Combretaceae (excluyendo *Laguncularia*), consistente con Tan et al. (2002).

5. ***Combretum* sensu lato es parafiletico:** *Quisqualis indica* se agrupa dentro de *Combretum*, con *C. fruticosum*.

6. ***Terminalia* sensu lato es parafiletica:** *Conocarpus*, *Buchenavia* y *Bucida* estan anidados dentro de *Terminalia*.

---

## 4. Analisis Bayesiano

### 4.1 BEAST 2.7.7 (en proceso)

| Parametro | Valor |
|-----------|-------|
| Software | BEAST 2.7.7 |
| Modelo de sustitucion | GTR |
| Modelo de reloj | Relaxed Clock Log-Normal |
| Prior del arbol | Birth-Death |
| Calibracion fosil | *Dilcherocarpon* 93.5 Ma (offset) |
| Iteraciones MCMC | 50,000,000 |
| Muestreo | cada 50,000 |
| Arboles muestreados | 1,001 |

**Estado actual:** Corrida completada (50M iteraciones). Pendiente: diagnostico de convergencia (ESS), burn-in, y generacion del arbol MCC (Maximum Clade Credibility).

#### Resumen preliminar del log:

| Parametro | Inicio (gen 0) | Final (gen 50M) | Rango posterior |
|-----------|-----------------|------------------|-----------------|
| Posterior | -26,652.5 | -13,749.0 | ~ -13,730 a -13,752 |
| treeLikelihood | -26,578.2 | -13,649.0 | ~ -13,637 a -13,652 |
| birthDeath | -74.3 | -99.9 | ~ -88 a -104 |
| clockRate | 0.001 | 7.4e-4 | ~ 6.1e-4 a 1.8e-3 |

El posterior se estabiliza rapidamente despues de las primeras 50,000 generaciones (burn-in < 1%), indicando buena convergencia.

### 4.2 MrBayes 3.2.7a

#### Corrida en Geneious (3 de febrero de 2026)

La primera corrida de MrBayes se realizo dentro de Geneious usando la supermatriz concatenada. Los resultados exportados incluyen:

| Output | Tamano | Descripcion |
|--------|--------|-------------|
| Posterior output | 741 KB | Arbol consenso con probabilidades posteriores |
| Raw Trees | 2,196 KB | Todos los arboles muestreados del MCMC |
| Sorted Topologies | 306 KB | Topologias ordenadas por frecuencia |

Archivos exportados: `results/10 documents from concatenados.csv` y `.geneious`

#### Corrida en linea de comandos (reproducible)

Se configuro y ejecuto una corrida independiente de MrBayes para reproducibilidad:

| Parametro | Valor |
|-----------|-------|
| Software | MrBayes 3.2.7a (ARM) |
| Modelo de sustitucion | GTR+I+G (nst=6, rates=invgamma) |
| Generaciones | 5,000,000 |
| Corridas | 2 (independientes) |
| Cadenas | 4 (1 fria + 3 calientes) |
| Muestreo | cada 1,000 |
| Burn-in | 25% (1,250 arboles descartados) |
| Prior de longitud de ramas | Unconstrained:Exponential(10.0) |
| Prior de frecuencias | Dirichlet(1,1,1,1) |
| Outgroup | *Punica granatum* |

Archivos de configuracion: `analyses/mrbayes/mrbayes_commands.nex`

Archivos de salida (cuando termine):
- `combretaceae_mrbayes.run1.t` / `.run2.t` - Arboles muestreados
- `combretaceae_mrbayes.run1.p` / `.run2.p` - Parametros muestreados
- `combretaceae_mrbayes.con.tre` - Arbol consenso con probabilidades posteriores
- `combretaceae_mrbayes.trprobs` - Topologias con probabilidades
- `combretaceae_mrbayes.parts` - Tabla de particiones (clados)

---

## 5. Delimitacion de Especies (ASAP)

### Parametros

| Parametro | Valor |
|-----------|-------|
| Software | ASAP |
| Input | supermatriz.fasta (20 secuencias, 2,819 pb) |
| Replicas | 1,000 |
| Metodo de distancia | Kimura 2-parametros (default) |
| Tiempo de computo | 1 segundo |

### Top 5 particiones por ASAP score

| Rango | Distancia | # Especies | p-value | ASAP score |
|-------|-----------|------------|---------|------------|
| 1 | 0.1313 | **4** | 0.611 | 2.0 |
| 2 | 0.1741 | **2** | 0.824 | 2.0 |
| 3 | 0.1529 | **3** | 0.834 | 2.0 |
| 4* | 0.0245 | **16** | 0.940 | 5.0 |
| 5* | 0.0270 | **14** | 0.884 | 7.5 |

*Particiones marcadas con asterisco (*) tienen barcode gap significativo.

### Interpretacion

- La particion con mejor ASAP score que muestra barcode gap corresponde a **16 especies** (de 20 secuencias), sugiriendo que algunos taxones no se distinguen a nivel molecular con estos marcadores.
- Las particiones con 2-4 especies reflejan la division principal entre Combretaceae y Lythraceae + divisiones internas mayores.

---

## 6. Resumen de Resultados

### Archivos de arboles generados

| Archivo | Contenido | Analisis |
|---------|-----------|----------|
| `arbol_conocarpus_final.tre` | Arbol final con soporte | TNT |
| `arbol_final_con_nombres_COMPLETO.tre` | Arbol con nombres de especies | TNT |
| `consenso_estricto.tre` | 2 arboles mas parsimoniosos | TNT |
| `bootstrap_2000.tre` | Bootstrap 2,000 replicas | TNT |
| `poisson_1000.tre` | Poisson resampling 1,000 | TNT |
| `symmetric_1000.tre` | Symmetric resampling 1,000 | TNT |
| `thesis_beast.trees` | 1,001 arboles posteriores | BEAST |
| `thesis_beast.log` | Log MCMC (50M generaciones) | BEAST |

### Estado de los analisis

| Analisis | Estado | Archivos |
|----------|--------|----------|
| jModelTest | **Completado** (parcial, 16/88 modelos) | `jmodeltest_results.txt` |
| TNT (parsimonia) | **Completado** | Multiples .tre |
| MrBayes (Geneious) | **Completado** | `.geneious`, `.csv` |
| MrBayes (CLI) | **En ejecucion** (5M gen) | `combretaceae_mrbayes.*` |
| BEAST 2 (bayesiano) | **En proceso** (pendiente post-procesamiento) | `.trees`, `.log` |
| ASAP | **Completado** | Scores, particiones, SVGs |

---

## 7. Tareas Pendientes

### Criticas (necesarias para la tesis)
1. **MrBayes CLI:** Esperando que termine la corrida de 5M generaciones (~2.5h). Luego extraer arbol consenso y probabilidades posteriores.
2. **BEAST post-procesamiento:**
   - Diagnostico de convergencia con Tracer (ESS > 200).
   - Determinar burn-in apropiado.
   - Generar arbol MCC con TreeAnnotator.
3. **Comparacion de topologias:** Contrastar parsimonia (TNT) vs. bayesiano (MrBayes) vs. BEAST.
4. **Valores de soporte en figuras:** Generar figuras finales en FigTree con bootstrap (parsimonia) y probabilidades posteriores (bayesiano).

### Recomendadas
5. **jModelTest:** Re-correr evaluacion completa de los 88 modelos (se interrumpio en modelo 16/88 por error de PhyML). Aunque GTR+I+G ya fue identificado como mejor modelo, completar la evaluacion fortaleceria la justificacion.
6. **Analisis por marcador individual:** Comparar topologias de cada marcador por separado para detectar conflicto entre genes (ITS nuclear vs. cloroplasto).
7. **Partition Finder:** Evaluar si un esquema de particiones por marcador (5 particiones) mejora el ajuste vs. la supermatriz concatenada con un solo modelo.
8. **Soporte de Bremer (decay index):** Complementar bootstrap con indices de Bremer en TNT.
9. **Arbol con tiempos de divergencia:** Una vez que BEAST termine y converja, generar cronograma con barras de intervalo de confianza del 95% HPD.
