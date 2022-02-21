library(klaR)
library(e1071)
library(ROCR)


P53 <- read.table("p03_Kato_P53_mutants_200.txt", sep = "\t", header = TRUE)
P53 <- subset(P53, select = -c(MUT))
P53[,c("CLASS")] <- sapply(P53[,c("CLASS")], function(x) {as.factor(x)})

folds <- function(x,n) split(x, sort(rep(1:n, len=length(x))))

partitions <- folds(P53, 3)

fold_labels <- list()
fold_predictions <- list()
count = 1
all_counts = list(1,2,3)
for (partition in partitions)
{
  test <- partition
  train <- setdiff(P53, test)
  
  trainSVM <- svm(CLASS ~ ., data = train, kernel = "linear", probability=TRUE, type = 'C')
  predictions <- predict(trainSVM, test, probability=TRUE, type = 'raw')
  
  actual_class <- test$CLASS == 'D'
  score <- attr(predictions, "probabilities")[,c('D')]
  score_numbers <- unname(score)
  
  fold_predictions[count] <- list(score_numbers)
  fold_labels[count] <- list(actual_class)
  
  count <- count + 1
  
}

pdf('p02 3-fold cross-validation.pdf')
pred <- prediction(fold_predictions, fold_labels)
perf <- performance(pred,"tpr","fpr")
auc <- performance(pred, "auc")
auc <- unlist(slot(auc, "y.values"))
mean_auc <- mean(auc)
plot(perf,col="grey82",lty=3)
plot(perf, lwd=3,avg="vertical",spread.estimate="boxplot",add=T)
legend(0.6, 0.3,c(c(paste('AUC is', mean_auc)), "\n"),
       border="white", cex=1.0, box.col="white")
dev.off()
