library(ROCR)
library(klaR)
library(e1071)

data(iris)

testidx <- which(1:length(iris[,1])%%5 == 0)
iristrain <- iris[-testidx,]
iristest <- iris[testidx,]

nbmodel <- NaiveBayes(Species~., data=iristrain)
nbprediction <- predict(nbmodel, iristest[,-5], type= 'raw')
score <- nbprediction$posterior[, c("virginica")]
actual_class <- iristest$Species == 'virginica'
pred <- prediction(score, actual_class)
nberr <- performance(pred, "err")
nbperf <- performance(pred, "tpr", "fpr")
nbauc <- performance(pred, "auc")
nbauc <- unlist(slot(nbauc, "y.values"))
plot(nberr)
plot(nbperf, colorize=TRUE)
legend(0.6,0.3,c(c(paste('AUC is', nbauc)),"\n"), 
       border="white",cex=1.0, box.col = "white")
