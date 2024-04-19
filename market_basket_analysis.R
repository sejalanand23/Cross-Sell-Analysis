# Load necessary libraries
library(tidyverse)
library(arules)

# Read the dataset
df <- read.csv("Groceries_dataset.csv", header = TRUE, stringsAsFactors = FALSE)

# Display first few rows of each dataset
head(df)

# Convert dataframe to transactions
trans_list <- split(df$itemDescription, df$Member_number)
trans_list <- lapply(trans_list, unique)
trans_list <- as(trans_list, "transactions")

# Adjusted Apriori parameters
rules <- apriori(trans_list, parameter = list(supp = 0.001, conf = 0.7, minlen = 2, target = "rules"))

#convert rules to df
rules_df <- as(rules, "data.frame")

# Save rules_df to CSV file
write.csv(rules_df, "rules.csv", row.names = FALSE)
