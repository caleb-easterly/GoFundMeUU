urls <- read.delim("C:/Users/caleb/OneDrive - University of North Carolina at Chapel Hill/Documents/Projects/Cancer care crowdfunding/GoFundMeUU/data/urls.txt",
                   header=FALSE)

# deduplicate
library(dplyr)
urls_dedup <- urls %>% distinct()

library(stringr)

urls_dedup$campaign <- str_detect(urls_dedup$V1, "https:\\/\\/www.gofundme.com\\/f\\/")
summary(urls_dedup)
colnames(urls_dedup) <- c("URL", "Is_Campaign")


