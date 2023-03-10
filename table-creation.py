# Method 1: Pandas only

import pandas as pd

covid_table = pd.DataFrame(data = covid_table, columns = ["id", "country", "total_cases", "new_cases",
                                                          "total_deaths", "new_deaths", "total_recovered",
                                                          "new_recovered", "active_cases", "active_critical_cases", 
                                                          "total_cases_per_mill", "deaths_per_mill", "total_tests",
                                                          "tests_per_mill", "population", "continent",
                                                          "1_case_per_X_ppl", "1_death_per_X_ppl", "1_test_per_X_ppl",
                                                          "new_cases_per_mill", "new_deaths_per_mill", "active_cases_per_mill"])
covid_table = covid_table.iloc[9:]
covid_table.index = [""] * len(covid_table)
covid_table = (
        covid_table
        .drop(columns = list(covid_table.filter(regex = "new|X")))
        .replace(['', "N/A"], pd.NA)
        .dropna()
        .apply(lambda x: x.str.replace(',', ''))
    )
numeric_cols = covid_table.drop(columns = ["country", "continent"]).columns
for i in numeric_cols:
    covid_table[i] = covid_table[i].astype(float)
    
# Method 2: Using pandas

import pandas as pd
import re

covid_df = pl.DataFrame(covid_table[1:], columns = ["id", "country", "total_cases", "new_cases",
                                                    "total_deaths", "new_deaths", "total_recovered",
                                                    "new_recovered", "active_cases", "active_critical_cases", 
                                                    "total_cases_per_mill", "deaths_per_mill", "total_tests",
                                                    "tests_per_mill", "population", "continent",
                                                    "1_case_per_X_ppl", "1_death_per_X_ppl", "1_test_per_X_ppl",
                                                    "new_cases_per_mill", "new_deaths_per_mill", "active_cases_per_mill"], 
                        orient = "row")

covid_df = (
    covid_df
    .select(
        pl.when(pl.col(pl.Utf8).is_in(["N/A", ""])).then(None).otherwise(pl.col(pl.Utf8)).keep_name()
    )
    .drop(columns = list(filter(re.compile("new.*|.*X.*").match, covid_df.columns)))
    .drop_nulls()
    .with_column(pl.col(pl.Utf8).str.replace_all(",", ""))
)

numeric_col = covid_df.drop(columns = ["country", "continent"]).columns

covid_df = (
    covid_df
    .with_column(pl.col(numeric_col).cast(pl.Float64))
)
