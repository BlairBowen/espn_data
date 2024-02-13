import requests

import config
import utilities.api as utils
import utilities.basketball.ncaam as ncaam_utils


def get_teams():
    utils.save_local_data(
        utils.fetch_data(config.mens_college_basketball_standings_url),
        "data\\basketball\\ncaam\mens_college_basketball_data.json",
    )


def get_conferences():
    conference_list = utils.load_local_data(
        "data\\basketball\\ncaam\mens_college_basketball_data.json"
    )

    conference_dict = {}

    for conference in conference_list["children"]:
        team_list = []
        for team in conference["standings"]["entries"]:
            team_list.append(team["team"]["id"])
        conference_dict[conference["abbreviation"]] = team_list

    utils.save_local_data(
        conference_dict,
        "data\\basketball\\ncaam\\mens_college_basketball_conference_list.json",
    )


def get_team_stats(team_id):
    response = utils.fetch_data(
        config.mens_college_basketball_team_stats_url.replace("*", team_id)
    )
    team_name = response["team"]["displayName"].lower().replace(" ", "_")
    utils.save_local_data(
        response, f"data\\basketball\\ncaam\\team_stats\\{team_name}_team_stats.json"
    )


def get_team_photos(team_id):
    picture = requests.get(
        config.mens_college_basketball_team_picture_url.replace("*", team_id)
    )
    team = ncaam_utils.locate_team_entry(team_id)
    team_name = team["displayName"].lower().replace(" ", "_")

    output_file = f"data\\basketball\\ncaam\\team_logos\\{team_name}_logo.png"

    utils.save_local_logo(picture.content, output_file)