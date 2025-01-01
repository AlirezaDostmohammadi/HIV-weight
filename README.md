# HIV-weight

## PICRUSt2 Pipeline with Nextflow
The pipeline consists of two key workflows:

1. QIIME2 Preprocessing Workflow
   - Filters features and samples based on total frequency thresholds (default: min_feature_abundance=15, min_samples_abundance=1500).

2. PICRUSt2 Workflow
   - Places ASVs into a reference tree.
   - Predicts hidden states of gene families (e.g., KO, EC).
   - Generates metagenome predictions.
   - Performs pathway-level inference and adds functional descriptions.

### Requirements
The pipeline requires the following tools and environments:
- Nextflow
- QIIME2
- PICRUSt2
- Python
- biom-format package

### How to Run the Pipeline
1. Run the preprocessing workflow (preprocessing.nextflow)
   ```
nextflow run preprocessing.nextflow --biom_table /path/to/biom --seq /path/to/sequences --min_feature_abundance 15 --min_samples_abundance 1500
   ```
2. Run the PICRUSt2 workflow
```
nextflow run picrust.nextflow --biom_table /path/to/biom --seq /path/to/sequences --cpu 10
```
