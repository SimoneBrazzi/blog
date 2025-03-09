# make a tibble for each result of summary

# make a tibble summary for each column in the dataset as a separate tibble
summary_tibbles <- map(names(df), ~{
  df %>%
    select(.x) %>%
    summary() %>%
    as_tibble() %>%
    mutate(column = .x) %>%
    select(column, everything())
})
