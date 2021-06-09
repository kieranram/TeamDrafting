library(tidyverse)

posandround <- read_csv('posandround.csv')

actualposition <- function(row) {pos <- row[7]
     if (pos %in% c('ILB', 'LB', 'OLB')) {pos <- 'LB'} 
     if (pos %in% c('C', 'OT', 'OG', 'T', 'G', 'OL')) {pos <- 'OL'}
     if (pos %in% c('DT', 'DE', 'NT', 'DL')) {pos <- 'DL'}
     if (pos %in% c('CB', 'S', 'DB')) {pos <- 'DB'}
     return(as.character(pos))}


posandround$New <- apply(posandround, MARGIN = 1, FUN = actualposition)
expposround <- posandround %>% filter(Year > 1980, Year < 2010) %>% group_by(Round, New) %>% summarize(expectav = mean(AV), expectg = mean(G), count = n())

avagainstexp <- function(row) {
  pos <- row[9]
  round <- row[8]
  expected <- expposround[expposround$Round == as.integer(round) & expposround$New == pos, 'expectav']
  return(as.numeric(as.integer(row[3]) - expected))
}

gagainstexp <- function(row) {
  pos <- row[9]
  expected <- expposround[expposround$Round == as.integer(round) & expposround$New == pos, 'expectg']
  return(as.numeric(as.integer(row[4]) - expected))
}

posandround$return <- apply(posandround, 1, avagainstexp)
posandround$returng <- apply(posandround, 1, gagainstexp)

