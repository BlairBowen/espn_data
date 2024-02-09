import time
import random

import endpoints.basketball.ncaam as ncaam
import utilities.api as utils
import config

if __name__ == "__main__":
    start = time.time()
    ncaam.iterate_conferences("convert_stats", wait=False)
    end = time.time()
    print(start - end)
    pass
