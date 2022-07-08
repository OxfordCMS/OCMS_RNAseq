#' Calculate the log2 counts per million on expression matrix
#'
#' Calculate the log2 counts per million on expression matrix
#' @param counts expression counts with genes as rows and samples as columns
#' @examples
#' log2cpm(counts)
#' @export

log2cpm <- function(counts){

	cpm <- log2(sweep(counts, 2, colSums(counts)/1000000, "/") + 1)
	return(cpm)
	}
