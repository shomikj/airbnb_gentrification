# File: classification_map -- Visualization of Real and Predicted Gentrification Labels
# Author: Shomik Jain
# Date: 2/02/2020

# install.packages("devtools")
# library(devtools)
# install_github('arilamstein/choroplethrZip@v1.5.0')

library(choroplethr)
library(choroplethrZip)
library(ggplot2)

real = read.csv("clustering_real.csv",header = TRUE,colClasses=c("character", "numeric"))
pred = read.csv("clustering_pred.csv",header = TRUE,colClasses=c("character", "numeric"))

nyc_fips = c(36005, 36047, 36061, 36081, 36085)

zip_choropleth(real,
               county_zoom = nyc_fips,
               num_colors=1) + scale_fill_continuous(low="#3895D3", high="#072F5F", na.value="#DCDCDC")

zip_choropleth(pred,
               county_zoom = nyc_fips,
               num_colors=1) + scale_fill_continuous(low="#3895D3", high="#072F5F", na.value="#DCDCDC")
