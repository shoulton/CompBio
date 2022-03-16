library('getopt')

spec <- matrix(c(
  'input','i',1,"string",
  'output','o',1, "string"
), byrow=TRUE, ncol=4)

opt = getopt(spec)
print(opt)

data <- read.table(file='p05pvalues.tsv', sep = '\t', header = TRUE, fill = TRUE)
ordered <- data[order('pvalue'),]
