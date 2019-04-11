library(rvest)
library(tidyverse)
url = 'https://www.reformagkh.ru/opendata?gid=2208161&cids=overhaul&pageSize=10&page=1'
first_page <- read_html(url)
last_page_num <-
  first_page %>% html_node('ul.pagination.fl') %>% html_node('li.last a') %>% html_attr("data-page") %>% as.numeric()
