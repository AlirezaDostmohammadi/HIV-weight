# HIV-weight

## PICRUSt2 Pipeline with Nextflow
The pipeline consists of two workflows to preprocess an ASV/OTU table and sequencing file (FASTA file) and to predict functional abundances based on ASVs/OTUs:

1. QIIME2 Preprocessing Workflow
   - Filters features and samples based on total frequency thresholds (default: min_feature_abundance=15, min_samples_abundance=1500).

2. PICRUSt2 Workflow
   - Maps ASVs/OTUs onto a reference phylogenetic tree.
   - Predicts hidden states for gene families, including:
     - Predicted 16S rRNA gene copy number for each ASV/OTU
     - Predicted copy numbers for KEGG Orthology (KO) numbers
     - Predicted copy numbers for Enzyme Classification (EC) numbers
3. Produces metagenome functional prediction
4. Performs pathway-level inference and annotates with detailed functional descriptions (EC numbers to MetaCyc pathways)

### Requirements
To execute the pipeline, the following tools are required:
- <a href='https://www.nextflow.io/'> Nextflow</a>
- <a href='https://qiime2.org/'>QIIME2</a>
- <a href='https://github.com/picrust/picrust2'>PICRUSt2</a>
- Python
- Python (with the <a href='https://pypi.org/project/biom-format/'>biom-format</a> package installed)

### How to Run the Pipeline
1. Run the preprocessing workflow:</br>
Use the <a href='/PICRUSt2.pipeline/preprocessing.nf'>preprocessing.nf</a> script to prepare the input files:
```
nextflow run preprocessing.nf --biom_table /path/to/{ASV|OTU}.biom --seq /path/to/sequences.fasta --min_feature_abundance 15 --min_samples_abundance 1500
```
2. Run the PICRUSt2 workflow: </br>
Use the <a href='PICRUSt2.pipeline/picrust2_pipeline.nf'>picrust2_pipeline.nf</a> script to perform functional prediction:
```
nextflow run picrust2_pipeline.nf --biom_table /path/to/{ASV|OTU}.filtered_samples_based_total.frequency.biom --seq /path/to/sequences.filtered.fasta --cpu 10
```

## Post-Processing Steps
PICRUSt2 generates predicted functional profiles in terms of KEGG Orthology (KO) numbers, but it does not directly provide pathway-level abundances. To obtain pathway abundances, you need to follow these steps:

### Map KO Numbers to KEGG Pathways
The <a href='kegg_mapping/map_ko_to_kegg_pathways.py'>map_ko_to_kegg_pathways.py</a> maps KEGG Orthology (KO) numbers to KEGG pathways using the KEGG API. This step generates a mapping file (<a href='kegg_mapping/ko_to_kegg_mapping.csv'>ko_to_kegg_mapping.csv</a>) required for pathway-level abundance aggregation.

### Calculating KEGG Pathway Abundances
The <a href='kegg_mapping/calculate_kegg_pathway_abundance.py'>calculate_kegg_pathway_abundance.py</a> aggregates KO abundances at the KEGG pathway level using the mapping file created in the previous step. The output file name is `KEGG_path_abun_unstrat.csv`

### Required python packages:
- bioservices
- pandas

### How to run the Post-Processing Steps:
1. Mapping KO Numbers to KEGG Pathways:
```

python map_ko_to_kegg_pathways.py --input /path/to/KO_pred_metagenome_unstrat.tsv.gz
```
2. Calculating KEGG Pathway Abundances
```
python calculate_kegg_pathway_abundance.py --ko_abundance /path/to/KO_pred_metagenome_unstrat.tsv.gz --mapping_file /path/to/ko_to_kegg_mapping.csv
```

## Differential Abundance Analysis using ALDEx2
This pipeline performs differential abundance analysis of KEGG pathways using <a href='https://www.bioconductor.org/packages/release/bioc/html/ALDEx2.html'>ALDEx2</a>.</br>
To run the pipeline, provide the metadata file and KEGG pathways abundance file as inputs in the <a href='differential_abundance_analysis/differential_abundance_analysis_aldex.R'>differential_abundance_analysis_aldex.R</a> script.

### Required R Packages:
- ALDEx2
- dplyr
