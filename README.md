# Phylogenetic Analysis of Combretaceae: Monophyly of Mangrove Lineages

## Overview

Phylogenetic reconstruction of **Combretaceae** (Myrtales) using parsimony (TNT) and Bayesian inference (BEAST 2), with emphasis on testing the monophyly of the mangrove genera *Conocarpus* and *Laguncularia* relative to their terrestrial relatives.

## Objectives

1. Test the monophyly of the mangrove clade (*Laguncularia racemosa* + *Conocarpus erectus*) within Combretaceae.
2. Evaluate the phylogenetic placement of Neotropical vs. Paleotropical lineages.
3. Estimate divergence times using fossil-calibrated Bayesian analysis.
4. Assess species delineation boundaries using ASAP.

## Taxon Sampling

**20 species** in 4 functional groups:

| Group | Species | Ecology |
|-------|---------|---------|
| **A - Mangroves** | *Laguncularia racemosa*, *Conocarpus erectus*, *Lumnitzera racemosa*, *L. littorea* | Manglar |
| **B - Neotropical terrestrial** | *Terminalia catappa*, *T. amazonia*, *Buchenavia tetraphylla*, *Bucida buceras*, *Combretum fruticosum*, *C. laxum* | Terrestre Neotropical |
| **C - Paleotropical terrestrial** | *Terminalia superba*, *T. mantaly*, *Combretum imberbe*, *C. molle*, *Quisqualis indica*, *Calycopteris floribunda* | Terrestre Paleotropical |
| **D - Outgroup (Lythraceae)** | *Lagerstroemia indica*, *Punica granatum*, *Trapa natans*, *Lawsonia inermis* | Outgroup |

## Molecular Markers (5)

| Marker | Genome | Type | Reference |
|--------|--------|------|-----------|
| **ITS** | Nuclear | Variable | Gere et al. 2015; Tan et al. 2002 |
| **matK** | Chloroplast | Conserved | Gere et al. 2015; Zhang 2020 |
| **rbcL** | Chloroplast | Conserved | Gere et al. 2015; Tan et al. 2002 |
| **psaA-ycf3** | Chloroplast | Variable | Gere et al. 2015 |
| **trnH-psbA** | Chloroplast | Variable | Gere et al. 2015 |

**Supermatrix:** 20 taxa x 2,819 bp (concatenated)

## Methods

### Substitution Model Selection
- **Software:** jModelTest 2.1.10
- **Candidates:** 88 models evaluated (11 substitution schemes x F x I x G)
- **Best model:** GTR+I+G (-lnL = 12,844.81)
- **Criteria:** AIC, AICc, BIC, DT

### Parsimony Analysis (TNT)
- **Software:** TNT (Tree Analysis Using New Technology)
- **Search:** 1,000 heuristic replicates, TBR branch swapping, 10 trees held per replicate
- **Outgroup:** *Punica granatum*
- **Support:** Bootstrap (2,000 replicates), Poisson resampling (1,000 replicates), Symmetric resampling (1,000 replicates)
- **Consensus:** Strict and majority-rule

### Bayesian Analysis (MrBayes 3.2.7a)
- **Substitution model:** GTR+I+G (nst=6, rates=invgamma)
- **MCMC:** 5,000,000 generations, 2 independent runs, 4 chains each
- **Sampling:** Every 1,000 generations
- **Burn-in:** 25%

### Bayesian Divergence Dating (BEAST 2.7.7)
- **Substitution model:** GTR
- **Clock model:** Relaxed Clock Log-Normal (heterogeneous rates)
- **Tree prior:** Birth-Death (speciation/extinction)
- **Fossil calibration:** *Dilcherocarpon* (offset 93.5 Ma; LogNormal M=1.5, S=0.3; Gilles et al. 2019)
- **MCMC:** 50,000,000 iterations, sampling every 50,000
- **Trees sampled:** 1,001

### Species Delineation (ASAP)
- **Software:** ASAP (Puillandre et al. 2021)
- **Input:** Supermatrix (2,819 bp)
- **Replicates:** 1,000

## Repository Structure

```
conocarpus-phylogeny/
├── README.md
├── RESULTS.md                      # Detailed results report
├── data/
│   ├── alignments/                 # Individual marker alignments (FASTA)
│   └── supermatrix/                # Concatenated supermatrix (FASTA, NEXUS, TNT)
├── analyses/
│   ├── tnt/                        # TNT scripts and configuration
│   ├── mrbayes/                    # MrBayes NEXUS commands and results
│   ├── beast/                      # BEAST XML and Python generators
│   ├── jmodeltest/                 # Model selection results
│   └── asap/                       # Species delineation results
├── results/
│   ├── trees/
│   │   ├── parsimony/              # TNT tree files
│   │   └── bayesian/               # BEAST tree files
│   ├── logs/                       # BEAST MCMC logs
│   └── figures/                    # ASAP SVG visualizations
└── scripts/                        # Utility scripts (download, conversion)
```

## Key References

- Gere, J. et al. (2015). African continent a likely origin of family Combretaceae. *Ann Res Rev Biol* 9(1): 1-13.
- Tan, F. et al. (2002). Phylogenetic relationships of Combretoideae inferred from plastid and nuclear sequences. *J Plant Res* 115: 67-76.
- Gilles, A. et al. (2019). *Dilcherocarpon* fossil calibration for Combretaceae.
- Drummond, A.J. et al. (2006). Relaxed phylogenetics and dating with confidence. *PLoS Biology* 4(5): e88.

## Software

| Tool | Version | Purpose |
|------|---------|---------|
| TNT | - | Maximum parsimony |
| MrBayes | 3.2.7a | Bayesian phylogenetic inference |
| BEAST | 2.7.7 | Bayesian divergence dating |
| jModelTest | 2.1.10 | Substitution model selection |
| ASAP | - | Automated species delineation |
| Geneious | - | Alignment, curation, visualization |

## Author

ECOSUR (El Colegio de la Frontera Sur)

## License

This project is for academic/thesis purposes.
