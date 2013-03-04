## EXAMPLE RUN:
## $ Rscript txt_to_RData.R mydcor.tab
print.eval = TRUE
argv <- commandArgs(trailingOnly = TRUE)
fname <- argv[1]
fname.out <- paste0(fname,".RData")
M <- read.table(fname, header=TRUE, sep="\t", row.names=1);
save(M, file=fname.out)
print(paste("Saved" fname.out))
