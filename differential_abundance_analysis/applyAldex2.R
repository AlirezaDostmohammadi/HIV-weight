library(ALDEx2)

#' Apply ALDEx2 for Differential Abundance Analysis
#'
#' This function applies the ALDEx2 package to perform compositional differential abundance analysis.
#' It computes Monte Carlo instances, centered log-ratio (clr) transformations, and statistical tests 
#' to identify features that differ between experimental conditions.
#'
#' @param data A data frame or matrix containing compositional data
#'             with features as rows and samples as columns.
#' @param meta_info A factor or vector representing group labels for each sample in `data`.
#' @param output_prefix A string to prefix the output filenames for saving results.
#' @param output.dir The directory path where results should be saved.
#'
#' @return
#' This function does not return any object but saves the results to specified output files:
#' - `results_<output_prefix>.aldex2.csv`: All ALDEx2 results.
#' - `filtered_results_<output_prefix>.aldex2.csv`: Filtered results for features with significant differences.


apply_aldex2 <- function(data, meta_info, output_prefix, output.dir) {
  
  # Ensure meta_info is a factor, which represents group labels
  condition <- meta_info
  
  # Run ALDEx2: generates Monte Carlo instances and clr values
  aldex_out <- aldex.clr(data, condition, mc.samples = 1000, denom = "all", 
                         useMC=TRUE)
  
  # Perform differential abundance testing
  aldex_res <- aldex.ttest(aldex_out, paired.test = FALSE)
  
  # Calculate effect sizes
  aldex_effect <- aldex.effect(aldex_out, useMC=TRUE)
  
  # Combine results into a single data frame
  final_res <- cbind(aldex_res, aldex_effect)
  
  # Output all the results
  write.csv(final_res, file = paste0(output.dir, "/results_", output_prefix, ".aldex2.csv"))
  
  # Filter results for adjusted p-values lower than 0.05
  # Benjamini-Hochberg corrected p-value for Wilcoxon Rank Sum 
  filtered_results <- subset(final_res, wi.eBH < 0.05)
  filtered_results <- filtered_results %>% filter(abs(diff.btw) >= 0.58)
  
  if (dim(filtered_results)[1] > 0) {
    # Output filtered results
    write.csv(filtered_results, 
              file = paste0(output.dir, "/p.value.lower.than.0.05/filtered_results_",
                            output_prefix, ".aldex2.csv"))
    
  }
}
