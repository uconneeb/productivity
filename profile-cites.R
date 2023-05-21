library(scholar)

df <- read.table(file="profiles.txt", header=TRUE)

total_ncites <- 0
sum_hindex <- 0
sum_i10index <- 0
count <- 0
cat(sprintf("%12s %15s %12s %12s %12s %12s\n", "first", "last", "hindex", "i10index", "ncites", "cum"))
for (i in 1:nrow(df)) {
    row <- df[i,]
    if (row$include) {
        count <- count + 1
        id  <- row$profile_id
        l   <- get_profile(id)
        ct  <- get_citation_history(id)
        h   <- l$h_index
        sum_hindex <- sum_hindex + h
        i10 <- l$i10_index
        sum_i10index <- sum_i10index + i10
        ncites <- 0
        for (j in 1:nrow(ct)) {
            ctrow <- ct[j,]
            year <- ctrow$year
            if (year >= row$startyear && year <= row$endyear) {
                cites <- ctrow$cites
                ncites <- ncites + cites
            }
        }
        total_ncites = total_ncites + ncites
        cat(sprintf("%12s %15s %12.1f %12.1f %12d %12d\n", row$first, row$last, h, i10, ncites, total_ncites))
    }
}

avg_hindex <- sum_hindex/count
avg_i10index <- sum_i10index/count
cat(sprintf("count = %d\n", count))
cat(sprintf("average h-index   = %.5f\n", avg_hindex))
cat(sprintf("average i10-index = %.5f\n", avg_i10index))
