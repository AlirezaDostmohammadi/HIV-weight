library(readr)
library(dplyr)
source("applyAldex2.R")


mapping.file <- read.csv('Mapping.csv')
abundance.file <- read.csv('KEGG_path_abun_unstrat.csv')

output.dir <- "result_aldex/"

sel.col.vect <- c('dominating_genus')


row.names(abundance.file) = abundance.file$Pathway
abundance.file$Pathway <- NULL


for (col_idx in 1:length(sel.col.vect)) {
  
  sel.col <- sel.col.vect[col_idx]
  
  # filter metadata file
  filter.mapping.file <- 
    mapping.file[!(is.na(mapping.file[[sel.col]]) | 
                     mapping.file[[sel.col]] == "" | 
                     mapping.file[[sel.col]] == " "), ]
  
  unique.values.in.sel.col <- unique(filter.mapping.file[[sel.col]])
  
  pairs.unique.values <- combn(unique.values.in.sel.col, 2, simplify = FALSE)
  
  for (elm_idx in 1:length(pairs.unique.values)) {
    
    sel.pairs.unique.values <- pairs.unique.values[[elm_idx]]
    print(sel.col)
    print(sel.pairs.unique.values)
    
    sel.filter.mapping.file <- 
      filter.mapping.file %>% filter(!!sym(sel.col) %in% sel.pairs.unique.values)
    
    # better to be vector
    meta.info <- sel.filter.mapping.file[, sel.col]
    
    samples.id <- sel.filter.mapping.file$X.SampleID
    
    # type: matrix (only positive integer)
    # columns: samples
    # rows: pathways
    sel.abundance.df <- round(abundance.file[, samples.id])
    
    apply_aldex2(sel.abundance.df, meta.info, 
                 paste0(sel.col, '.', sel.pairs.unique.values[1], '.', 
                        sel.pairs.unique.values[2]), output.dir)
    
  }
}

  