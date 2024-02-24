import random
import time

import pandas as pd

import config
import endpoints.basketball.ncaam as ncaam
import utilities.api as utils
import utilities.basketball.ncaam.api as ncaam_api

df = pd.DataFrame(columns=ncaam_api.stats_column_headers)
years = [2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024]

if __name__ == "__main__":
    # start = time.time()
    # ncaam_api.iterate_conferences(ncaam.get_team_stats, conference_selector=["sec"])
    # end = time.time()
    # print(end - start)
    print(ncaam.get_teams())
    print(ncaam.get_team_stats(True))
    print(ncaam.get_conferences())
    # for year in years:
    #     print(ncaam.get_team_stats(True, year))
    #     print(ncaam.get_teams(True, year))
    # print(ncaam.get_conferences(True))

    pass
