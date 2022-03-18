library('getopt')

spec <- matrix(c(
  'input','i',2,"character",
  'output','o',2, "character"
), byrow=TRUE, ncol=4)

#input <- "p05pvalues.tsv"
#output <- "pvalues.corrected.tsv"

opt = getopt(spec)
input <- opt$input
output <- opt$output

data <- read.table(file=input, sep = '\t', header = TRUE, fill = TRUE)
ordered <- data[order(data$pvalue),]

m <- nrow(ordered)
i <- 1

q_val <- vector("list", m)

for (j in rownames(ordered)) {
  row <- ordered[i,]
  ratio <- m/i
  p_val <- row$pvalue
  q_val[[i]] <- (p_val*ratio)
  i <- i+1
}

ordered$qvalue <- q_val

ordered[sapply(ordered, is.list)] <-
  sapply(ordered[sapply(ordered, is.list)], 
         function(x)sapply(x, function(y) paste(unlist(y),collapse=", ") ) )

write.table(ordered, output, quote=FALSE, sep="\t", row.names = FALSE)
