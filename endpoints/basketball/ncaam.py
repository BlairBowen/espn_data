import time
import random
import requests
import urllib.request

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
    pass


def get_team_photos(team_id):
    picture = requests.get(config.mens_college_basketball_team_picture_url.replace("*", team_id))
    response = utils.fetch_data(
        config.mens_college_basketball_team_stats_url.replace("*", team_id)
    )
    team_name = response["team"]["displayName"].lower().replace(" ", "_")
    with open(
        f"data\\basketball\\ncaam\\team_logos\\{team_name}_logo.png", "wb"
    ) as f:
        f.write(picture.content)
        print(f"Saved logo for {team_name}")
