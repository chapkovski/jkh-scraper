library(rvest)
library(tidyverse)
library(glue)
library(xml2)
library(httr)
setwd('~/jkh/data')
url = 'https://www.reformagkh.ru/opendata?gid=2208161&cids=overhaul&pageSize=10&page={i}'

get_page <- function(i = 1) {
  return (glue(url))
}
get_full_path <- function(x) {
  base = 'https://www.reformagkh.ru'
  return (url_absolute(x, base))
}

get_file <- function(link) {
  # this one gets the link, retrieve original file name from content disposition and saves it
  fil <- GET(link, write_disk("tmp.fil", overwrite = T))
  get_disposition_filename <- function(x) {
    t <- sub(".*filename=", "", headers(x)$`content-disposition`)
    str_match(t, "\"(.*)\";")[, 2]
    
  }
  fname <- get_disposition_filename(fil)
  file.rename("tmp.fil", fname)
  print(glue('File {fname} downloaded successfully'))
}


get_page_data <- function(url) {
  # this function reads all divs and retrieve export links and feed them into downloader
  print(glue('Getting page {url}'))
  page <- read_html(url)
  export_links <-
    page %>% html_nodes('div.opendata') %>% html_node('li.opendata-action-export a') %>% html_attr('href') -> export_links
  export_links <- sapply(export_links, get_full_path)
  sapply(export_links, get_file)
  
}
# we get the first page
first_page <- read_html(get_page())
# get the number of total pages
last_page_num <-
  first_page %>% html_node('ul.pagination.fl') %>% html_node('li.last a') %>% html_attr("data-page") %>% as.numeric()
# build links to each page
sapply(seq(1, last_page_num), get_page) -> pages
# loop through each page to download data
sapply(pages, get_page_data)


