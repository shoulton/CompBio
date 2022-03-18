library('getopt')

spec <- matrix(c(
  'input','i',2,"character",
  'output','o',2, "character"
), byrow=TRUE, ncol=4)

opt = getopt(spec)
input <- opt$input
output <- opt$output

data <- read.table(file='p05pvalues.tsv', sep = '\t', header = TRUE, fill = TRUE)
ordered <- data[order('pvalue'),]
