import time
import random

import endpoints.basketball.ncaam as ncaam
import utilities.api as utils
import config

if __name__ == "__main__":
    json_data = utils.load_local_data(
        "data\\basketball\\ncaam\\mens_college_basketball_conference_list.json"
    )

    for teams in json_data:
        for team_id in json_data[teams]:
            ncaam.get_team_stats(team_id)
        time.sleep(30)
