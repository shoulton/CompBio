library('getopt')

spec <- matrix(c(
  'input','i',2,"character",
  'output','o',2, "character"
), byrow=TRUE, ncol=4)

input <- "p05pvalues.tsv"
output <- "pvalues.corrected.tsv"

#opt = getopt(spec)
#input <- opt$input
#output <- opt$output

data <- read.table(file=input, sep = '\t', header = TRUE, fill = TRUE)
ordered <- data[order(data$pvalue),]

m <- nrow(ordered)
i <- 1

q_vals <- vector("list", m)
num_qval <- 0

for (j in rownames(ordered)) {
  row <- ordered[j,]
  ratio <- m/i
  p_val <- row$pvalue
  q_val <- round(p_val*ratio, digits=6)
  q_vals[[i]] <- q_val
  row$pvalue <- round(row$pvalue, digits=6)
  if(q_val <= 0.05){
    num_qval <- num_qval + 1
  }
  i <- i+1
}

ordered$qvalue <- q_vals

ordered[sapply(ordered, is.list)] <-
  sapply(ordered[sapply(ordered, is.list)], 
         function(x)sapply(x, function(y) paste(unlist(y),collapse=", ") ) )

write.table(ordered, output, quote=FALSE, sep="\t", row.names = FALSE)
print(paste("Number of discoveries: ", num_qval))