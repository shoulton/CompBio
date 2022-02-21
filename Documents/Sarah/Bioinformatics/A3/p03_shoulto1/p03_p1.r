library(klaR)
library(e1071)
library(ROCR)
library(kernlab)
data(spam)

set.seed(3)

sample <- sample.int(n=nrow(spam), size = floor(.8*nrow(spam)), replace = F)
train <- spam[sample,]
test <- spam[-sample,]

trainSVM <- svm(type ~ ., data = train, kernel = "linear", probability=TRUE)


predictions <- predict(trainSVM, test, probability=TRUE, type = 'raw')
table(predictions, test$type)
actual_class <- test$type == 'spam'
score <- attr(predictions, "probabilities")[,c("spam")]

pred <- prediction(score, actual_class)

perf <- performance(pred, "tpr", "fpr")
auc <- performance(pred, "auc")
auc <- unlist(slot(auc, "y.values"))
pdf('p01 no cross-validation.pdf')
plot(perf, colorize=TRUE)
legend(0.6, 0.3,c(c(paste('AUC is', auc)), "\n"),
       border="white", cex=1.0, box.col="white")
dev.off()

folds <- function(x,n) split(x, sort(rep(1:n, len=length(x))))

partitions <- folds(spam, 10)

fold_predictions <- list()
fold_labels <- list()
count = 1
all_counts = list(1,2,3,4,5,6,7,8,9,10)
for (partition in partitions)
{
  test <- partition
  train <- setdiff(spam, test)
  
  trainSVM <- svm(type ~ ., data = train, kernel = "linear", probability=TRUE)
  predictions <- predict(trainSVM, test, probability=TRUE, type = 'raw')
  actual_class <- test$type == 'spam'
  score <- attr(predictions, "probabilities")[,c("spam")]
  score_numbers <- unname(score)
  fold_predictions[count] <- list(score_numbers)
  fold_labels[count] <- list(actual_class)

  count <- count + 1
  
}

pdf('p01 10-fold cross-validation.pdf')
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

