import time
import random

import config
import utilities.api as utils


def get_teams():
    utils.save_local_data(
        utils.fetch_data(config.mens_college_basketball_url),
        "data\\basketball\\ncaam\mens_college_basketball_teams.json",
    )
    pass


def get_team_stats(team_id):
    response = utils.fetch_data(
        config.mens_college_basketball_team_stats_url.replace("*", team_id)
    )
    team_name = response["team"]["displayName"].lower().replace(" ", "_")
    utils.save_local_data(
        response, f"data\\basketball\\ncaam\\team_stats\\{team_name}_team_stats.json"
    )
    time.sleep(random.uniform(0.75, 1.3))
    pass
