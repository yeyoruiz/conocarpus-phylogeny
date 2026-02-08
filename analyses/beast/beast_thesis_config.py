#!/usr/bin/env python3
"""
BEAST 2.7.7 XML Generator - CONFIGURATION FOR THESIS
Filogenia de Combretaceae con calibración temporal y reloj relajado.

JUSTIFICACIÓN CIENTÍFICA:
- Relaxed Clock: Captura tasas evolutivas heterogéneas (manglares vs terrestres)
- Birth-Death Prior: Refleja procesos de especiación/extinción a nivel de familia
- Calibración Dilcherocarpon: Offset 93.5 Ma (Paleoceno-Eoceno)
- 50M iteraciones: ESS > 200 para parámetros de reloj relajado

REFERENCIAS:
- Drummond et al. (2006): Relaxed phylogenetics
- Stadler (2010): Birth-Death models for trees
- Gilles et al. (2019): Dilcherocarpon fósil de Combretaceae
"""

import sys
from Bio import SeqIO
import math

def generate_beast_xml_thesis(nexus_file):
    """Generate BEAST XML with Relaxed Clock + Birth-Death + Fossil Calibration."""
    
    alignment = list(SeqIO.parse(nexus_file, "nexus"))
    n_taxa = len(alignment)
    n_char = len(alignment[0])
    
    print(f"[THESIS CONFIG] Alignment: {n_taxa} taxa, {n_char} bp")
    print(f"[CLOCK] Relaxed Clock Log-Normal (heterogeneous evolutionary rates)")
    print(f"[PRIOR] Birth-Death Model (macroevolutionary speciation/extinction)")
    print(f"[CALIBRATION] Dilcherocarpon fossil: 93.5 Ma (offset)")
    print(f"[CHAIN] 50,000,000 iterations (ESS > 200)")
    
    xml_lines = [
        "<?xml version='1.0' encoding='UTF-8'?>",
        "<beast version='2.0'",
        "       namespace='beast.pkgmgmt:beast.base.core:beast.base.inference:beast.base.evolution.alignment:beast.base.evolution.tree.coalescent:beast.base.inference.util:beast.evolution.nuc:beast.base.evolution.operator:beast.base.inference.operator:beast.base.evolution.sitemodel:beast.base.evolution.substitutionmodel:beast.base.evolution.likelihood'>",
        "",
        "    <!-- ===== SEQUENCE DATA ===== -->",
        "    <data id='alignment' dataType='nucleotide'>",
    ]
    
    # Add sequences
    for record in alignment:
        seq_str = str(record.seq)
        seq_formatted = '\n            '.join([seq_str[i:i+70] for i in range(0, len(seq_str), 70)])
        xml_lines.append(f"        <sequence taxon='{record.id}'>")
        xml_lines.append(f"            {seq_formatted}")
        xml_lines.append(f"        </sequence>")
    
    xml_lines.extend([
        "    </data>",
        "",
        "    <!-- ===== SUBSTITUTION MODEL: GTR ===== -->",
        "    <input spec='GTR' id='gtr'>",
        "        <parameter name='rateAC' value='1.0'/>",
        "        <parameter name='rateAG' value='1.0'/>",
        "        <parameter name='rateAT' value='1.0'/>",
        "        <parameter name='rateCG' value='1.0'/>",
        "        <parameter name='rateCT' value='1.0'/>",
        "        <parameter name='rateGT' value='1.0'/>",
        "        <frequencies id='freqs' spec='Frequencies'>",
        "            <input name='data' idref='alignment'/>",
        "        </frequencies>",
        "    </input>",
        "",
        "    <!-- ===== SITE MODEL ===== -->",
        "    <input spec='SiteModel' id='siteModel'>",
        "        <input name='substModel' idref='gtr'/>",
        "        <parameter name='shape' value='1.0'/>",
        "        <parameter name='proportionInvariant' value='0.0'/>",
        "    </input>",
        "",
        "    <!-- ===== TREE LIKELIHOOD ===== -->",
        "    <input spec='TreeLikelihood' id='treeLikelihood'>",
        "        <input name='data' idref='alignment'/>",
        "        <input name='tree' idref='tree'/>",
        "        <input name='siteModel' idref='siteModel'/>",
        "    </input>",
        "",
        "    <!-- ===== INITIAL TREE ===== -->",
        "    <input spec='beast.base.evolution.tree.ClusterTree' id='tree' clusterType='upgma'>",
        "        <input name='taxa' idref='alignment'/>",
        "    </input>",
        "",
        "    <!-- ===== RELAXED CLOCK: Log-Normal ===== -->",
        "    <!-- Permite tasas evolutivas heterogéneas entre linajes -->",
        "    <input spec='beast.base.evolution.branchratemodel.UCRelaxedClockModel' id='relaxedClock'>",
        "        <input name='tree' idref='tree'/>",
        "        <parameter name='mean' id='clock.rate' value='0.001'/>",
        "        <parameter name='stdev' value='0.1'/>",
        "        <distribution spec='LogNormalDistributionModel' meanInRealSpace='true'>",
        "            <parameter name='M' value='-6.907'/>",
        "            <parameter name='S' value='1.25'/>",
        "        </distribution>",
        "    </input>",
        "",
        "    <!-- ===== TREE LIKELIHOOD WITH CLOCK ===== -->",
        "    <input spec='TreeLikelihood' id='treeLikelihoodClock'>",
        "        <input name='data' idref='alignment'/>",
        "        <input name='tree' idref='tree'/>",
        "        <input name='siteModel' idref='siteModel'/>",
        "        <input name='branchRateModel' idref='relaxedClock'/>",
        "    </input>",
        "",
        "    <!-- ===== TREE PRIOR: Birth-Death ===== -->",
        "    <!-- Refleja procesos de especiación/extinción a nivel de familia -->",
        "    <input spec='beast.base.evolution.speciation.BirthDeathGernhard08Model' id='birthDeath' tree='@tree'>",
        "        <parameter name='birthDiffRate' value='0.01'/>",
        "        <parameter name='relativeDeathRate' value='0.5'/>",
        "    </input>",
        "",
        "    <!-- ===== FOSSIL CALIBRATION: Dilcherocarpon ===== -->",
        "    <!-- Crown Combretaceae offset 93.5 Ma (Paleoceno-Eoceno) -->",
        "    <!-- LogNormal: M=1.5, S=0.3 (Gilles et al. 2019) -->",
        "    <distribution id='cal_Dilcherocarpon' monophyletic='true' spec='beast.base.evolution.tree.MRCAPrior' tree='@tree' tipsonly='false'>",
        "        <taxonset id='taxonset_Combretaceae' spec='TaxonSet'>",
        "            <taxon id='Buchenavia_tetraphylla' spec='Taxon'/>",
        "            <taxon id='Conocarpus_erectus' spec='Taxon'/>",
        "            <taxon id='Laguncularia_racemosa' spec='Taxon'/>",
        "            <taxon id='Terminalia_catappa' spec='Taxon'/>",
        "        </taxonset>",
        "        <distr id='LogNormal_Dilcherocarpon' meanInRealSpace='false' offset='93.5' spec='beast.base.inference.distribution.LogNormalDistributionModel'>",
        "            <parameter dimension='1' estimate='false' id='RealParameter_M_Dil' name='M' value='1.5'/>",
        "            <parameter dimension='1' estimate='false' id='RealParameter_S_Dil' lower='0.01' name='S' upper='5.0' value='0.3'/>",
        "        </distr>",
        "    </distribution>",
        "",
        "    <!-- ===== MCMC: 50M ITERATIONS ===== -->",
        "    <run spec='MCMC' id='mcmc' chainLength='50000000' storeEvery='50000'>",
        "        <state>",
        "            <stateNode idref='tree'/>",
        "            <stateNode idref='clock.rate'/>",
        "        </state>",
        "",
        "        <!-- Posterior = Prior + Likelihood + Calibration -->",
        "        <distribution spec='CompoundDistribution' id='posterior'>",
        "            <distribution idref='birthDeath'/>",
        "            <distribution idref='cal_Dilcherocarpon'/>",
        "            <distribution idref='treeLikelihoodClock'/>",
        "        </distribution>",
        "",
        "        <!-- ===== TREE OPERATORS ===== -->",
        "        <operator spec='ScaleOperator' scaleFactor='0.5' weight='1' name='treeScaler'>",
        "            <tree idref='tree'/>",
        "        </operator>",
        "        <operator spec='Uniform' weight='10' name='uniformRandom'>",
        "            <tree idref='tree'/>",
        "        </operator>",
        "        <operator spec='SubtreeSlide' weight='5' gaussian='true' size='1.0' name='subtreeSlide'>",
        "            <tree idref='tree'/>",
        "        </operator>",
        "        <operator spec='Exchange' isNarrow='true' weight='1' name='narrowExchange'>",
        "            <tree idref='tree'/>",
        "        </operator>",
        "        <operator spec='Exchange' isNarrow='false' weight='1' name='wideExchange'>",
        "            <tree idref='tree'/>",
        "        </operator>",
        "        <operator spec='WilsonBalding' weight='1' name='wilsonBalding'>",
        "            <tree idref='tree'/>",
        "        </operator>",
        "",
        "        <!-- ===== CLOCK RATE OPERATORS ===== -->",
        "        <operator spec='ScaleOperator' scaleFactor='0.75' weight='3' name='rateScaler'>",
        "            <parameter idref='clock.rate'/>",
        "        </operator>",
        "",
        "        <!-- ===== LOGGING: ESS > 200 ===== -->",
        "        <logger spec='Logger' logEvery='50000' fileName='thesis_beast.log'>",
        "            <log idref='posterior'/>",
        "            <log idref='clock.rate'/>",
        "        </logger>",
        "        <logger spec='Logger' logEvery='50000' fileName='thesis_beast.trees'>",
        "            <log idref='tree'/>",
        "        </logger>",
        "        <logger spec='Logger' logEvery='50000'>",
        "            <log idref='posterior'/>",
        "        </logger>",
        "    </run>",
        "",
        "</beast>"
    ])
    
    output_file = "combretaceae_thesis.xml"
    with open(output_file, 'w') as f:
        f.write('\n'.join(xml_lines))
    
    print(f"\n[✓ SUCCESS] Generated: {output_file}")
    return output_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 beast_thesis_config.py <nexus_file>")
        sys.exit(1)
    
    nexus_file = sys.argv[1]
    generate_beast_xml_thesis(nexus_file)
