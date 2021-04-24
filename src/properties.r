install.packages("protr",repos = "http://cran.us.r-project.org")
install.packages("Peptides",repos = "http://cran.us.r-project.org")

library(protr)
library(Peptides)

args <- commandArgs(trailingOnly = TRUE)
input <- args[1]
output <- args[2]

proteinseq <- read.csv(input)
pureseq <- proteinseq$sequence


properties <- function(proteins){
  df <- data.frame( 1:length(pureseq),
                    pI(proteins,  pKscale = "EMBOSS"), lengthpep(proteins), hydrophobicity(proteins, scale = "KyteDoolittle"),
                    mw(proteins, monoisotopic = FALSE, label = "none", aaShift = NULL), aIndex(proteins) )
  
  names(df) <- c('ID', 'isoelectricity', 'length', 'hydrophobicity', 'weight', 'aliphatic')
  
  return(df)
}

prop <- properties(pureseq)
write.csv(properties(pureseq), args[2])
