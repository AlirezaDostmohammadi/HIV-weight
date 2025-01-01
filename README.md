# HIV-weight

## PICRUSt2 Pipeline with Nextflow
The pipeline consists of two key workflows to preprocess ASV/OTU table and sequencing file (FASTA file) to filter rare ASVs and low depth samples, to to predict functional abundances based on ASVs/OTUs :

1. QIIME2 Preprocessing Workflow
   - Filters features and samples based on total frequency thresholds (default: min_feature_abundance=15, min_samples_abundance=1500).

2. PICRUSt2 Workflow
   - Places ASVs into a reference tree.
   - Predicts hidden states of gene families (e.g., KO, EC).
   - Generates metagenome predictions.
   - Performs pathway-level inference and adds functional descriptions.

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
