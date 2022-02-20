library(klaR)
library(e1071)
library(ROCR)

#install.packages('kernlab')
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
pdf('p01 no cross-validation')
plot(perf, colorize=TRUE)
legend(0.6, 0.3,c(c(paste('AUC is', auc)), "\n"),
       border="white", cex=1.0, box.col="white")
dev.off()

folds <- function(x,n) split(x, sort(rep(1:n, len=length(x))))

partitions <- folds(spam, 10)

fold_predictions <- list()
fold_values <- list()
count = 1
all_counts = list(1,2,3,4,5,6,7,8,9,10)
for (partition in partitions)
{
  test <- partition
  train_counts <- all_counts[-count]
  train <- partitions[train_counts[[1]]]
  train_counts <- train_counts[-train_counts[[1]]]
  for (tc in train_counts)
  {
    train <- merge.data.frame(train, partitions[tc], all=TRUE)
  }
  
  count <- count + 1
  
}

x <- subset(spam, select = -c(type))
my_spam <- spam
my_spam[,c("type")] <- sapply(my_spam[,c("type")], function(x) {ifelse(x=='spam', 1, -1)})
#my_spam[,c("type")] <- sapply(my_spam[,c("type")], as.numeric)
my_spam[,c("type")] <- sapply(my_spam[,c("type")], as.factor)
y <- subset(my_spam, select = c(type))
obj <- tune(method = svm, train.x = x, train.y = y, type='C-classification', kernel="linear", probability=TRUE)



