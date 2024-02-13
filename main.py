import random
import time

import pandas as pd

import config
import endpoints.basketball.ncaam as ncaam
import utilities.api as utils
import utilities.basketball.ncaam.api as ncaam_api

df = pd.DataFrame(columns=ncaam_api.stats_column_headers)

if __name__ == "__main__":
    start = time.time()
    ncaam_api.iterate_conferences(ncaam.get_team_stats, conference_selector=["sec"])
    end = time.time()
    print(end - start)
    pass