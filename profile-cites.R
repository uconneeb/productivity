library(scholar)

df <- read.table(file="profiles.txt", header=TRUE)

# 2015
# 2016
# 2017
# 2018 *
# 2019 *
# 2020 *
# 2021 *
# 2022 *
after_year <- 2017

total_ncites <- 0
sum_hindex <- 0
sum_hcalc <- 0
sum_i10index <- 0
sum_i10calc <- 0
count <- 0
cat(sprintf("%12s %15s %12s %12s %12s %12s %12s %12s %12s %12s %12s %12s\n", "first", "last", "hindex", "hcalc", "i10index", "n10", "n50", "n100", "n500", "n1000", "ncites", "cum"))
nrows <- nrow(df)
for (i in 6:nrows) {
    row <- df[i,]
    if (row$include) {
        count <- count + 1
        id  <- row$profile_id
        l   <- get_profile(id)
        
        h   <- l$h_index
        sum_hindex <- sum_hindex + h
        
        i10 <- l$i10_index
        sum_i10index <- sum_i10index + i10
        
        ct  <- get_citation_history(id)
        ncites <- 0
        for (j in 1:nrow(ct)) {
            ctrow <- ct[j,]
            year <- ctrow$year
            if (year > after_year && year >= row$startyear && year <= row$endyear) {
                cites <- ctrow$cites
                ncites <- ncites + cites
            }
        }
        
        pubs <- get_publications(id)
        npubs <- nrow(pubs)
        n10 <- 0
        n50 <- 0
        n100 <- 0
        n500 <- 0
        n1000 <- 0
        # pubcounts[3] = number of pubs with at least 3 citations
        pubcounts <- rep(0,npubs)
        for (j in 1:npubs) {
            pubrow <- pubs[j,]
            pubid <- pubrow$pubid
            pubcites <- pubrow$cites
            if (after_year > 2014) {
                citehistory <- get_article_cite_history(id, pubid)
                chrows <- nrow(citehistory)
                pubcites <- 0
                if (chrows > 0) {
                    for (m in 1:chrows) {
                        chrow = citehistory[m,]
                        chyear <- chrow$year
                        chcites <- chrow$cites
                        if (chrow$year > after_year) {
                            pubcites <- pubcites + chrow$cites
                        }
                    }
                }
            }
            for (k in 1:npubs) {
                if (pubcites >= k) {
                    pubcounts[k] = pubcounts[k] + 1
                }
            }
            if (pubcites >= 10)
                n10 <- n10 + 1
            if (pubcites >= 50)
                n50 <- n50 + 1
            if (pubcites >= 100)
                n100 <- n100 + 1
            if (pubcites >= 500)
                n500 <- n500 + 1
            if (pubcites >= 1000)
                n1000 <- n1000 + 1
        }

        hcalc <- 0
        for (k in 1:npubs) {
            if (pubcounts[k] >= k)
                hcalc = k
        }
        sum_hcalc <- sum_hcalc + hcalc      
        sum_i10calc <- sum_i10calc + n10      
        
        total_ncites = total_ncites + ncites
        cat(sprintf("%12s %15s %12.1f %12.1f %12d %12d %12d %12d %12d %12d %12d %12d\n", row$first, row$last, h, hcalc, i10, n10, n50, n100, n500, n1000, ncites, total_ncites))
        #Sys.sleep(20)    # to prevent "Response code 429. Google is rate limiting you for making too many requests too quickly." 
    }
}

#avg_hindex <- sum_hindex/count
#avg_hcalc <- sum_hcalc/count
#avg_i10index <- sum_i10index/count
#avg_i10calc <- sum_i10calc/count
#cat(sprintf("count = %d\n", count))
#cat(sprintf("\nsum h-index     = %.5f\n", sum_hindex))
#cat(sprintf("average h-index   = %.5f\n", avg_hindex))
#cat(sprintf("\nsum hcalc       = %.5f\n", sum_hcalc))
#cat(sprintf("average hcalc     = %.5f\n", avg_hcalc))
#cat(sprintf("\nsum i10-index   = %.5f\n", sum_i10index))
#cat(sprintf("average i10-index = %.5f\n", avg_i10index))
#cat(sprintf("\nsum i10calc     = %.5f\n", sum_i10calc))
#cat(sprintf("average i10calc   = %.5f\n", avg_i10calc))
#