# File: regression.R -- Linear Regression w/Airbnb data + gentrification score
# Author: Shomik Jain
# Date: 2/02/2020

install.packages("stargazer")
library("stargazer")

# Load data
setwd("../data/")
zip_data = read.csv("regression.csv",header = TRUE)

# Setting year fixed effects
zip_data$year<-as.factor(zip_data$year)

# Regression (year fixed effects) for gentrification_score
# (can be adapted for other socio-economic measures: age, race, income, crime, education)

# Reg 1: All Features
reg1 = lm(zip_data$gentrification_score~zip_data$year+zip_data$listings_count_log+zip_data$agg_count_log+zip_data$price_log+zip_data$person_capacity+zip_data$square_feet+zip_data$review_rating_location+zip_data$review_length_log+zip_data$crime_words_perc_old+zip_data$sentiment_neg_avg+zip_data$lda_pca1+zip_data$lda_pca2+zip_data$d2v_pca1+zip_data$d2v_pca2)
# Reg 2: Structured Features (Metadata)
reg2 = lm(zip_data$gentrification_score~zip_data$year+zip_data$listings_count_log+zip_data$agg_count_log+zip_data$price_log+zip_data$person_capacity+zip_data$square_feet+zip_data$review_rating_location)
# Reg 3: Unstructured Features (Text)
reg3 = lm(zip_data$gentrification_score~zip_data$year+zip_data$review_length_log+zip_data$crime_words_perc_old+zip_data$sentiment_neg_avg+zip_data$lda_pca1+zip_data$lda_pca2+zip_data$d2v_pca1+zip_data$d2v_pca2)

# Calculate RMSE
rmse <- function(sm) 
  sqrt(mean(sm$residuals^2))

mse1 = rmse(summary(reg1))
mse2 = rmse(summary(reg2))
mse3 = rmse(summary(reg3))

# Output Regression
stargazer(reg3, reg2, reg1, 
          add.lines = list(c("Year Fixed Effects", "Yes","Yes", "Yes", "Yes", "Yes", "Yes", "Yes")), 
          omit=c("year","zipcode"), 
          covariate.labels=c("Reviews Length (Log)", "Crime Words", "Sentiment", "LDA Component 1", "LDA Component 2", "D2V Component 1", "D2V Component 2", "Listings Count (Log)", "Reviews Count (Log)", "Price (Log)", "Person Capacity (Log)", "Square Feet", "Location Rating"),
          no.space=TRUE, 
          out = "gentrification_regression.txt")
